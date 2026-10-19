"""Find the cheapest constellation that covers the whole Earth, and the cheapest one for each latency target.

sweep.py evaluates a fixed grid of designs. This script searches instead: for every family (altitude x
inclination x pattern x number of planes) it starts at the smallest satellites-per-plane that can geometrically
close the ring, and adds satellites until the design both covers every grid point at every step and meets the
tightest latency target (or hits --max-spp). Searching is done at a coarse "screen" fidelity, then the winners
are re-checked at full fidelity (24 h, 60 s, 2,000+ points), and the next candidate is tried if one fails.

Latency target = p99 of the alarm latency over every place and time on Earth (--metric worst_point_p95_ms
uses the p95 at the worst place instead). Cost = satellites x --sat-cost + planes x --plane-cost, in M EUR.
Defaults: EUR 0.75 M per satellite built and launched by rideshare, plus EUR 0.78 M for the four optical ISL
terminals (01-research/08-OUR-PROPOSAL.md: ~EUR 70 M to put optical terminals on 90 satellites), no extra cost
per plane. Pass --plane-cost if each orbital plane needs its own launch.

    python optimize.py                               # default search (~10-20 min on 8 cores)
    python optimize.py --targets 120 100 90          # p99 targets in ms
    python optimize.py --alt 550 800 --planes 6 8 10 12 --plane-cost 5
    python optimize.py --alt 500 600 --base-shell 5x11@1200/87/star   # low shell on top of a sparse high one
    python optimize.py --report                      # only print the answer from results/optimize_*.csv
"""
from __future__ import annotations

import os

os.environ.setdefault("OMP_NUM_THREADS", "1")       # one process per core; keep numpy single-threaded
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")

import argparse
import math
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

import pandas as pd

from globalnet import config as cfg
from globalnet.model import evaluate

STAR_MIN_INC_DEG = 80.0


def coverage_half_angle_rad(alt_km: float, min_el_deg: float = cfg.TERMINAL_MIN_EL_DEG) -> float:
    """Earth central angle from the sub-satellite point to the edge of the footprint at the terminal mask."""
    e = math.radians(min_el_deg)
    return math.acos(cfg.RE_KM * math.cos(e) / (cfg.RE_KM + alt_km)) - e


def min_spp(alt_km: float) -> int:
    """Fewest satellites per plane whose footprints still touch along the orbit: 2 pi / S <= 2 lambda."""
    return max(2, math.ceil(math.pi / coverage_half_angle_rad(alt_km)))


def min_planes(alt_km: float, inc_deg: float) -> int:
    """Planes needed so the 2P street crossings of the equator (each at most 2 lambda / sin i wide) span it."""
    return max(1, math.ceil(math.pi * math.sin(math.radians(inc_deg)) / (2 * coverage_half_angle_rad(alt_km))))


def _shell(f: dict, spp: int) -> cfg.Shell:
    return cfg.Shell(f["planes"], spp, f["altitude_km"], f["inclination_deg"], f["pattern"], 1)


def _evaluate(shell: cfg.Shell, isl: str, hours: float, step: float, grid: int,
              base: tuple[cfg.Shell, ...] = ()) -> dict:
    """One design: the searched shell, plus any fixed base shells flown with it (a hybrid)."""
    t0 = time.time()
    design = cfg.Design(" + ".join(x.label for x in (shell,) + base), (shell,) + base, isl)
    s = evaluate(design, hours=hours, step_s=step, grid_points=grid).summary()
    return dict(planes=shell.planes, sats_per_plane=shell.sats_per_plane, altitude_km=shell.altitude_km,
                inclination_deg=shell.inclination_deg, pattern=shell.pattern,
                base_shell=" + ".join(x.label for x in base) or "none",
                total_planes=shell.planes + sum(x.planes for x in base), **s,
                hours=hours, step_s=step, runtime_s=round(time.time() - t0, 1))


def search_family(f: dict) -> list[dict]:
    """Add satellites per plane until the design is gap-free and meets the tightest target, or --max-spp."""
    rows, base = [], tuple(cfg.Shell.parse(x) for x in f.get("base", ()))
    # with a base shell carrying coverage, the searched shell may be sparser than a gap-free shell of its own
    first = min_spp(f["altitude_km"]) // (2 if base else 1)
    for spp in range(max(f["spp_from"], first), f["max_spp"] + 1):
        r = _evaluate(_shell(f, spp), f["isl"], f["hours"], f["step"], f["grid"], base)
        rows.append(r)
        if r["full_coverage"] and r["min_sats_in_view"] >= f["min_in_view"] and r[f["metric"]] <= f["stop_ms"]:
            break
    return rows


def cost(df: pd.DataFrame, sat_cost: float, plane_cost: float) -> pd.Series:
    planes = df.total_planes if "total_planes" in df else df.planes
    return df.sats * sat_cost + planes * plane_cost


def candidates(screen: pd.DataFrame, metric: str, target_ms: float | None, min_in_view: int = 1) -> pd.DataFrame:
    ok = screen[(screen.full_coverage.astype(str) == "True") & (screen.min_sats_in_view >= min_in_view)]
    if target_ms is not None:
        ok = ok[ok[metric] <= target_ms]
    return ok.sort_values(["cost_meur", "sats", metric])


def report(screen: pd.DataFrame, confirmed: pd.DataFrame, a) -> None:
    for df in (screen, confirmed):   # CSVs from single-shell runs before hybrids existed
        if len(df) and "total_planes" not in df:
            df["total_planes"] = df.planes
    cols = ["target", "sats", "total_planes", "shells", "cost_meur", "min_sats_in_view", "max_gap_min",
            "latency_p50_ms", "latency_p99_ms", "worst_point_p95_ms", "within_100ms"]
    full = candidates(screen, a.metric, None, a.min_in_view)
    print(f"\nScreened {len(screen)} designs ({screen.sats.min()}-{screen.sats.max()} sats), "
          f"{len(full)} gap-free with >= {a.min_in_view} in view at screen fidelity.")
    if not len(confirmed):
        print("No design passed full-fidelity confirmation. Widen --planes / --max-spp / --alt.")
        return
    print(f"\nCheapest design per target, confirmed at {a.hours:g} h / {a.step:g} s / {a.grid} points "
          f"(cost = sats x {a.sat_cost:g} + planes x {a.plane_cost:g} M EUR, target on {a.metric}):\n")
    print(confirmed[cols].to_markdown(index=False, floatfmt=".4g"))

    # Lowest latency the searched space reaches, and the knee: the cheapest design within 5 ms of it.
    best = full[a.metric].min()
    knee = candidates(screen, a.metric, best + 5, a.min_in_view).head(1)
    if len(knee):
        k = knee.iloc[0]
        print(f"\nLowest {a.metric} reached in the search: {best:.0f} ms. Cheapest within 5 ms of that: "
              f"{k.shells} ({k.sats} sats, {k.cost_meur:.0f} M EUR, {k[a.metric]:.0f} ms at screen fidelity).")
    # Pareto front over everything screened: each row is the cheapest design reaching that latency.
    front = full.sort_values(["cost_meur", a.metric])
    front = front[front[a.metric] < front[a.metric].cummin().shift(fill_value=1e9)]
    print("\nPareto front, cost vs latency (screen fidelity):\n"
          + front[["sats", "total_planes", "shells", "cost_meur", "min_sats_in_view", a.metric]]
          .to_markdown(index=False, floatfmt=".4g"))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--targets", type=float, nargs="+", default=[150, 120, 110, 100, 95, 90],
                    help="latency targets in ms on --metric; full coverage alone is always reported too")
    ap.add_argument("--metric", default="latency_p99_ms", choices=["latency_p99_ms", "worst_point_p95_ms"])
    ap.add_argument("--alt", type=float, nargs="+", default=[550.0, 650.0, 800.0, 1000.0, 1200.0])
    ap.add_argument("--families", nargs="+", default=["87/star", "70/delta", "80/delta", "87/delta"],
                    help="INC/PATTERN pairs to search")
    ap.add_argument("--planes", type=int, nargs="+", default=list(range(4, 25)))
    ap.add_argument("--max-spp", type=int, default=40, help="give up on a family above this many sats per plane")
    ap.add_argument("--max-sats", type=int, default=600, help="skip families whose smallest design exceeds this")
    ap.add_argument("--min-in-view", type=int, default=1,
                    help="also require this many usable satellites everywhere, always (2 = survives one failure)")
    ap.add_argument("--base-shell", action="append", default=[],
                    help="fixed shell flown with every searched design, PxS@ALT/INC/PATTERN (repeatable): a hybrid")
    ap.add_argument("--isl", default="grid", choices=cfg.ISL_MODES)
    ap.add_argument("--sat-cost", type=float, default=1.53, help="M EUR per satellite incl. launch and ISL")
    ap.add_argument("--plane-cost", type=float, default=0.0, help="M EUR per orbital plane (dedicated launch)")
    ap.add_argument("--screen", type=float, nargs=3, default=[3, 120, 1000], metavar=("HOURS", "STEP_S", "GRID"),
                    help="coarse fidelity used while searching")
    ap.add_argument("--hours", type=float, default=24, help="confirmation fidelity")
    ap.add_argument("--step", type=float, default=60)
    ap.add_argument("--grid", type=int, default=2000)
    ap.add_argument("--confirm-tries", type=int, default=5, help="candidates to try per target before giving up")
    ap.add_argument("--workers", type=int, default=os.cpu_count())
    ap.add_argument("--out", type=Path, default=Path(__file__).parent / "results")
    ap.add_argument("--report", action="store_true", help="only print the answer from the saved CSVs")
    a = ap.parse_args()
    screen_csv, confirm_csv = a.out / "optimize_screen.csv", a.out / "optimize_confirmed.csv"

    if a.report:
        screen, confirmed = pd.read_csv(screen_csv), pd.read_csv(confirm_csv)
        screen["cost_meur"] = cost(screen, a.sat_cost, a.plane_cost)
        return report(screen, confirmed, a)

    # 1. Search every family at screen fidelity.
    h, st, g = a.screen
    families, base_sats = [], sum(cfg.Shell.parse(x).size for x in a.base_shell)
    for alt in a.alt:
        for fam in a.families:
            inc, pattern = fam.split("/")
            inc = float(inc)
            if pattern == "star" and inc < STAR_MIN_INC_DEG:
                continue
            for p in a.planes:
                if p < min_planes(alt, inc) // (2 if a.base_shell else 1) or p * min_spp(alt) > a.max_sats:
                    continue
                families.append(dict(altitude_km=alt, inclination_deg=inc, pattern=pattern, planes=p, isl=a.isl,
                                     spp_from=2, max_spp=min(a.max_spp, (a.max_sats - base_sats) // p), hours=h, step=st,
                                     grid=int(g), metric=a.metric, stop_ms=min(a.targets),
                                     min_in_view=a.min_in_view, base=tuple(a.base_shell)))
    print(f"Searching {len(families)} families ({len(a.alt)} altitudes x {a.families} x planes "
          f"{min(a.planes)}-{max(a.planes)}) at {h:g} h / {st:g} s / {int(g)} points on {a.workers} workers...")
    t0, rows = time.time(), []
    with ProcessPoolExecutor(max_workers=a.workers) as pool:
        futures = {pool.submit(search_family, f): f for f in families}
        for n, fut in enumerate(as_completed(futures), 1):
            try:
                fam_rows = fut.result()
            except Exception as e:   # one bad family must not kill the search
                print(f"FAILED {futures[fut]}: {e}")
                continue
            rows += fam_rows
            last = fam_rows[-1]
            first_full = next((r for r in fam_rows if r["full_coverage"]), None)
            print(f"[{n}/{len(families)}] {last['altitude_km']:>6g} km {last['inclination_deg']:>4g}deg "
                  f"{last['pattern']:<5} P={last['planes']:<2}  "
                  + (f"gap-free from {first_full['sats']} sats" if first_full else "never gap-free")
                  + f", stopped at {last['sats']} sats p99={last['latency_p99_ms']:.0f} ms", flush=True)
    if not rows:
        raise SystemExit("Nothing was evaluated: every family was pruned or failed. Widen --planes / --alt.")
    a.out.mkdir(parents=True, exist_ok=True)
    screen = pd.DataFrame(rows)
    screen.to_csv(screen_csv, index=False)
    screen["cost_meur"] = cost(screen, a.sat_cost, a.plane_cost)
    print(f"Search done in {(time.time() - t0) / 60:.1f} min -> {screen_csv}")

    # 2. Confirm the cheapest candidate per target at full fidelity; fall back to the next one if it fails.
    targets = [None] + sorted(a.targets, reverse=True)
    confirmed, cache = [], {}
    with ProcessPoolExecutor(max_workers=a.workers) as pool:
        for target in targets:
            label = "full coverage" if target is None else f"{a.metric.split('_ms')[0]} <= {target:g} ms"
            cands = candidates(screen, a.metric, target, a.min_in_view).head(a.confirm_tries)
            # confirm this target's shortlist in parallel, then take the cheapest that holds
            base = tuple(cfg.Shell.parse(x) for x in a.base_shell)
            shells = [cfg.Shell(int(c.planes), int(c.sats_per_plane), c.altitude_km, c.inclination_deg, c.pattern)
                      for c in cands.itertuples()]
            jobs = {s: pool.submit(_evaluate, s, a.isl, a.hours, a.step, a.grid, base) for s in shells
                    if s not in cache}
            for s, fut in jobs.items():
                cache[s] = fut.result()
            hit = next((cache[s] for s in shells if cache[s]["full_coverage"]
                        and cache[s]["min_sats_in_view"] >= a.min_in_view and (target is None or cache[s][a.metric] <= target)), None)
            if hit is None:
                print(f"  {label}: none of the {len(shells)} cheapest candidates held at full fidelity")
                continue
            print(f"  {label}: {hit['shells']} ({hit['sats']} sats)")
            confirmed.append(dict(target=label, **hit))
    confirmed = pd.DataFrame(confirmed)
    if len(confirmed):
        confirmed["cost_meur"] = cost(confirmed, a.sat_cost, a.plane_cost)
    confirmed.to_csv(confirm_csv, index=False)
    print(f"Done in {(time.time() - t0) / 60:.1f} min -> {confirm_csv}")
    report(screen, confirmed, a)


if __name__ == "__main__":
    main()
