"""Sweep constellation designs for full-Earth coverage and low latency. Satellite count is left free.

Every combination of planes x satellites per plane x altitude x inclination x star/delta (optionally on top
of an extra fixed shell, e.g. a polar cap) is evaluated over the whole globe. Each finished row is appended
to the CSV at once, and re-running the same command skips rows already in the file (safe to stop/resume).
At the end it prints the smallest designs that meet the targets, and the latency Pareto front.

    python sweep.py --dry-run                                  # size of the grid
    python sweep.py                                            # default grid, all cores
    python sweep.py --report                                   # only print the ranking from the CSV
    python sweep.py --inc 53 --extra-shell none --extra-shell 6x20@560/97.6/star   # inclined + polar hybrids
"""
from __future__ import annotations

import argparse
import csv
import itertools
import os
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

import pandas as pd

from globalnet import config as cfg
from globalnet.model import evaluate

STAR_MIN_INC_DEG = 80.0   # a Walker star only makes sense for near-polar planes
PARAM_COLUMNS = ["planes", "sats_per_plane", "altitude_km", "inclination_deg", "pattern", "phasing", "extra_shell",
                 "isl", "blocked"]


def _key(row: dict) -> tuple:
    return tuple(str(row[c]) for c in PARAM_COLUMNS)


def _design(job: dict) -> cfg.Design:
    shells = (cfg.Shell(job["planes"], job["sats_per_plane"], job["altitude_km"], job["inclination_deg"],
                        job["pattern"], job["phasing"]),)
    if job["extra_shell"] != "none":
        shells += (cfg.Shell.parse(job["extra_shell"]),)
    return cfg.Design(" + ".join(s.label for s in shells), shells, job["isl"])


def _one(job: dict) -> dict:
    t0 = time.time()
    r = evaluate(_design(job), hours=job["hours"], step_s=job["step"], grid_points=job["grid"],
                 blocked=frozenset(job["blocked"].split(",")) if job["blocked"] != "-" else frozenset())
    row = {k: job[k] for k in PARAM_COLUMNS}
    row.update(r.summary())
    row.update(hours=job["hours"], step_s=job["step"], runtime_s=round(time.time() - t0, 1))
    return row


def report(path: Path, max_p99_ms: float, top: int = 15):
    df = pd.read_csv(path)
    cols = ["sats", "shells", "isl", "coverage_worst_point", "max_gap_min", "min_sats_in_view",
            "latency_p50_ms", "latency_p99_ms", "worst_point_p95_ms", "within_100ms"]
    full = df[df.full_coverage.astype(str) == "True"].sort_values(["sats", "latency_p99_ms"])
    print(f"\n{len(df)} designs in {path}, {len(full)} serve every grid point at every step.")
    if full.empty:
        best = df.sort_values(["coverage_worst_point", "sats"], ascending=[False, True]).head(top)
        print("None reach full coverage yet. Closest:\n" + best[cols].to_markdown(index=False, floatfmt=".3g"))
        return
    print("\nSmallest designs with full coverage:\n" + full.head(top)[cols].to_markdown(index=False, floatfmt=".3g"))
    ok = full[full.latency_p99_ms <= max_p99_ms]
    print(f"\nSmallest with full coverage and p99 <= {max_p99_ms:g} ms:")
    print(ok.head(top)[cols].to_markdown(index=False, floatfmt=".3g") if len(ok) else "  none")
    # Pareto front: each row is the cheapest design reaching that worst-place latency
    front = full.sort_values("sats").loc[lambda d: d.worst_point_p95_ms < d.worst_point_p95_ms.cummin().shift(fill_value=1e9)]
    print("\nPareto front (satellites vs latency at the worst place on Earth):\n"
          + front[cols].to_markdown(index=False, floatfmt=".3g"))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--planes", type=int, nargs="+", default=[6, 8, 10, 12, 16, 20, 24])
    ap.add_argument("--spp", type=int, nargs="+", default=[10, 12, 15, 18, 22, 26, 30], help="satellites per plane")
    ap.add_argument("--alt", type=float, nargs="+", default=[550.0, 800.0, 1200.0])
    ap.add_argument("--inc", type=float, nargs="+", default=[53.0, 70.0, 87.0, 97.6])
    ap.add_argument("--patterns", nargs="+", default=["star", "delta"], choices=list(cfg.PATTERNS))
    ap.add_argument("--phasing", type=int, nargs="+", default=[1])
    ap.add_argument("--extra-shell", action="append", default=None,
                    help="fixed shell added to every design, PxS@ALT/INC/PATTERN or 'none' (repeatable)")
    ap.add_argument("--isl", nargs="+", default=["grid"], choices=cfg.ISL_MODES)
    ap.add_argument("--block", nargs="*", default=[], help="also run each design with these gateway(s) offline")
    ap.add_argument("--hours", type=float, default=24)
    ap.add_argument("--step", type=float, default=60)
    ap.add_argument("--grid", type=int, default=2000, help="grid points over the Earth")
    ap.add_argument("--max-p99-ms", type=float, default=100, help="latency target used in the final ranking")
    ap.add_argument("--workers", type=int, default=os.cpu_count())
    ap.add_argument("--out", type=Path, default=Path(__file__).parent / "results" / "sweep.csv")
    ap.add_argument("--dry-run", action="store_true", help="print the number of runs and exit")
    ap.add_argument("--report", action="store_true", help="only print the ranking from --out")
    a = ap.parse_args()

    if a.report:
        return report(a.out, a.max_p99_ms)
    extra = a.extra_shell or ["none"]
    blocked = ["-"] + ([",".join(sorted(a.block))] if a.block else [])
    jobs = [
        dict(planes=p, sats_per_plane=s, altitude_km=alt, inclination_deg=inc, pattern=pat, phasing=f,
             extra_shell=x, isl=isl, blocked=b, hours=a.hours, step=a.step, grid=a.grid)
        for p, s, alt, inc, pat, f, x, isl, b in itertools.product(
            a.planes, a.spp, a.alt, a.inc, a.patterns, a.phasing, extra, a.isl, blocked)
        if not (pat == "star" and inc < STAR_MIN_INC_DEG)
    ]
    # biggest designs first, so the long runs do not end up alone at the tail
    jobs.sort(key=lambda j: -j["planes"] * j["sats_per_plane"])

    done = set()
    if a.out.exists():
        with a.out.open() as f:
            done = {_key(r) for r in csv.DictReader(f)}
    todo = [j for j in jobs if _key(j) not in done]
    sizes = sorted({j["planes"] * j["sats_per_plane"] for j in jobs})
    print(f"{len(jobs)} runs in grid ({sizes[0]}-{sizes[-1]} sats per shell), {len(jobs) - len(todo)} already in "
          f"{a.out}, {len(todo)} to go ({a.hours:g} h at {a.step:g} s steps, {a.grid} points, {a.workers} workers)")
    if a.dry_run:
        return
    if todo:
        a.out.parent.mkdir(parents=True, exist_ok=True)
        t0 = time.time()
        with ProcessPoolExecutor(max_workers=a.workers) as pool, a.out.open("a", newline="") as f:
            writer = None
            futures = {pool.submit(_one, j): j for j in todo}
            for n, fut in enumerate(as_completed(futures), 1):
                try:
                    row = fut.result()
                except Exception as e:   # one bad design must not kill a long sweep
                    print(f"FAILED {futures[fut]}: {e}")
                    continue
                if writer is None:
                    writer = csv.DictWriter(f, fieldnames=list(row))
                    if not done:
                        writer.writeheader()
                writer.writerow(row)
                f.flush()
                eta = (time.time() - t0) / n * (len(todo) - n)
                print(f"[{n}/{len(todo)}] {row['sats']:>5} sats  {row['shells']}  cov_worst={row['coverage_worst_point']:.3f}  "
                      f"gap={row['max_gap_min']:.0f} min  p99={row['latency_p99_ms']:.0f} ms  eta {eta / 60:.0f} min",
                      flush=True)
        print(f"Done in {(time.time() - t0) / 60:.1f} min -> {a.out}")
    report(a.out, a.max_p99_ms)


if __name__ == "__main__":
    main()
