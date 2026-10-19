"""Evaluate the preset designs (or any shells you give) and write results/presets.csv + results/by_latitude.csv.

    python run.py                                        # all presets, 24 h at 60 s steps
    python run.py --presets polar-66 hybrid-550-360
    python run.py --shell 6x20@560/97.6/star --shell 15x16@550/53/delta --isl grid
    python run.py --block Troll McMurdo                  # take gateways offline
"""
from __future__ import annotations

import argparse
import time
from concurrent.futures import ProcessPoolExecutor
from functools import partial
from pathlib import Path

import pandas as pd

from globalnet import config as cfg
from globalnet.model import evaluate

KEY_COLUMNS = ["design", "sats", "isl", "coverage_mean", "coverage_worst_point", "max_gap_min", "min_sats_in_view",
               "latency_p50_ms", "latency_p99_ms", "worst_point_p95_ms", "within_100ms", "within_150ms"]


def _one(d: cfg.Design, **kw):
    r = evaluate(d, **kw)
    return r.summary(), r.by_latitude().assign(design=d.name, sats=d.size)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--presets", nargs="*", default=list(cfg.PRESETS), choices=list(cfg.PRESETS))
    ap.add_argument("--shell", action="append", default=[], help="custom shell PxS@ALT/INC/PATTERN (repeatable)")
    ap.add_argument("--isl", default="grid", choices=cfg.ISL_MODES, help="ISL mode for --shell designs")
    ap.add_argument("--block", nargs="*", default=[], help="gateways to take offline")
    ap.add_argument("--hours", type=float, default=24)
    ap.add_argument("--step", type=float, default=60)
    ap.add_argument("--grid", type=int, default=2000, help="grid points over the Earth (~450 km apart at 2000)")
    ap.add_argument("--out", type=Path, default=Path(__file__).parent / "results")
    a = ap.parse_args()

    designs = [cfg.PRESETS[n] for n in a.presets]
    if a.shell:
        shells = tuple(cfg.Shell.parse(s) for s in a.shell)
        designs.append(cfg.Design("custom", shells, a.isl))
    print(f"Evaluating {len(designs)} designs ({a.hours:g} h, {a.step:g} s steps, {a.grid} grid points)...")
    t0 = time.time()
    job = partial(_one, hours=a.hours, step_s=a.step, grid_points=a.grid, blocked=frozenset(a.block))
    with ProcessPoolExecutor() as pool:
        out = list(pool.map(job, designs))
    a.out.mkdir(parents=True, exist_ok=True)
    summary = pd.DataFrame([s for s, _ in out])
    summary.to_csv(a.out / "presets.csv", index=False)
    pd.concat([b for _, b in out]).to_csv(a.out / "by_latitude.csv", index=False)
    print(f"Done in {time.time() - t0:.0f} s -> {a.out}/presets.csv, by_latitude.csv\n")
    print(summary[KEY_COLUMNS].to_markdown(index=False, floatfmt=".3g"))


if __name__ == "__main__":
    main()
