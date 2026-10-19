"""Sweep constellation designs and write one CSV row per run, for picking the best size and shape.

Built for a big machine: every core runs a scenario, each finished row is appended to the CSV
immediately, and re-running the same command skips rows already in the file (safe to stop/resume).

    python sweep.py --dry-run                         # how many runs the default grid is
    python sweep.py                                   # default grid, 24 h at 10 s steps
    python sweep.py --planes 3 4 6 --spp 8 10 12 --inc 60 65 70 --hours 6   # smaller grid
    python sweep.py --workers 64 --out results/sweep_big.csv
"""
from __future__ import annotations

import argparse
import csv
import itertools
import os
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

from ntnpulse import config as cfg
from ntnpulse.engine import run

PATTERNS = {"star": 180.0, "delta": 360.0}
STAR_MIN_INC_DEG = 80.0   # a Walker star only makes sense for near-polar planes

PARAM_COLUMNS = ["planes", "sats_per_plane", "altitude_km", "inclination_deg", "pattern", "phasing",
                 "mode", "blocked", "load", "seed"]


def _key(row: dict) -> tuple:
    return tuple(str(row[c]) for c in PARAM_COLUMNS)


def _one(job: dict) -> dict:
    c = cfg.Constellation(
        f"{job['planes']}x{job['sats_per_plane']}-{job['inclination_deg']:g}-{job['pattern']}",
        planes=job["planes"], sats_per_plane=job["sats_per_plane"], altitude_km=job["altitude_km"],
        inclination_deg=job["inclination_deg"], raan_spread_deg=PATTERNS[job["pattern"]],
        phasing=job["phasing"])
    sc = cfg.Scenario(constellation=c, mode=job["mode"], load=job["load"], seed=job["seed"],
                      blocked_gateways=frozenset(job["blocked"].split(",")) if job["blocked"] != "-" else frozenset(),
                      terminals=job["terminals"], duration_s=job["hours"] * 3600, step_s=job["step"])
    t0 = time.time()
    r = run(sc)
    row = {k: job[k] for k in PARAM_COLUMNS}
    row.update(r.summary())
    crit = r.by_class().set_index("cls").loc["critical"]
    row.update(critical_within_150ms=crit.within_150ms, critical_via_isl=crit.via_isl,
               critical_store_forward=crit.store_forward, hours=job["hours"], step_s=job["step"],
               runtime_s=round(time.time() - t0, 1))
    return row


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--planes", type=int, nargs="+", default=[2, 3, 4, 5, 6, 8])
    ap.add_argument("--spp", type=int, nargs="+", default=[6, 8, 10, 12, 15], help="satellites per plane")
    ap.add_argument("--alt", type=float, nargs="+", default=[500.0, 550.0, 600.0])
    ap.add_argument("--inc", type=float, nargs="+", default=[53.0, 60.0, 65.0, 70.0, 75.0, 85.0, 97.6])
    ap.add_argument("--patterns", nargs="+", default=["star", "delta"], choices=list(PATTERNS))
    ap.add_argument("--phasing", type=int, nargs="+", default=[1])
    ap.add_argument("--modes", nargs="+", default=["regen_isl"], choices=cfg.MODES)
    ap.add_argument("--block", nargs="*", default=[], help="also run each design with these gateway(s) offline")
    ap.add_argument("--loads", type=float, nargs="+", default=[1.0])
    ap.add_argument("--seeds", type=int, nargs="+", default=[7])
    ap.add_argument("--hours", type=float, default=24)
    ap.add_argument("--step", type=float, default=10)
    ap.add_argument("--terminals", type=int, default=300)
    ap.add_argument("--workers", type=int, default=os.cpu_count())
    ap.add_argument("--out", type=Path, default=Path(__file__).parent / "results" / "sweep.csv")
    ap.add_argument("--dry-run", action="store_true", help="print the number of runs and exit")
    a = ap.parse_args()

    blocked = ["-"] + ([",".join(sorted(a.block))] if a.block else [])
    jobs = [
        dict(planes=p, sats_per_plane=s, altitude_km=alt, inclination_deg=inc, pattern=pat, phasing=f,
             mode=m, blocked=b, load=l, seed=seed, hours=a.hours, step=a.step, terminals=a.terminals)
        for p, s, alt, inc, pat, f, m, b, l, seed in itertools.product(
            a.planes, a.spp, a.alt, a.inc, a.patterns, a.phasing, a.modes, blocked, a.loads, a.seeds)
        if not (pat == "star" and inc < STAR_MIN_INC_DEG)
    ]

    done = set()
    if a.out.exists():
        with a.out.open() as f:
            done = {_key(r) for r in csv.DictReader(f)}
    todo = [j for j in jobs if _key(j) not in done]
    print(f"{len(jobs)} runs in grid, {len(jobs) - len(todo)} already in {a.out}, {len(todo)} to go "
          f"({a.hours:g} h at {a.step:g} s steps, {a.workers} workers)")
    if a.dry_run or not todo:
        return

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
            j = futures[fut]
            print(f"[{n}/{len(todo)}] {j['planes']}x{j['sats_per_plane']} {j['altitude_km']:g} km "
                  f"{j['inclination_deg']:g}deg {j['pattern']} {j['mode']} {j['blocked']} x{j['load']:g}  max_gap={row['max_gap_min']:.1f} min  "
                  f"crit_p95={row['critical_p95_s']:.3g} s  eta {eta / 60:.0f} min", flush=True)
    print(f"Done in {(time.time() - t0) / 60:.1f} min -> {a.out}")


if __name__ == "__main__":
    main()
