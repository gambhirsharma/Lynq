"""Run the Phase 2 scenario matrix and write results/summary.csv + results/by_class.csv.

    python run.py                       # full matrix, 24 h at 10 s steps
    python run.py --hours 6 --sats 30   # quicker subset
"""
from __future__ import annotations

import argparse
import itertools
import time
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import pandas as pd

from ntnpulse import config as cfg
from ntnpulse.engine import run

KEY_COLUMNS = [
    "sats", "mode", "blocked", "load", "delivery_ratio", "critical_p50_s", "critical_p95_s",
    "critical_within_250ms", "all_within_90min", "max_gap_min", "max_onboard_queue_kb",
    "routing_compliance", "policy_redirects",
]


def _one(sc: cfg.Scenario):
    r = run(sc)
    by_class = r.by_class().assign(scenario=sc.label, sats=sc.constellation.size, mode=sc.mode,
                                   blocked=",".join(sorted(sc.blocked_gateways)) or "-", load=sc.load)
    return r.summary(), by_class


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--sats", type=int, nargs="+", default=[12, 30], choices=sorted(cfg.CONSTELLATIONS))
    ap.add_argument("--modes", nargs="+", default=list(cfg.MODES), choices=cfg.MODES)
    ap.add_argument("--block", nargs="*", default=["Stavanger"],
                    help="gateway(s) to take offline in the restricted variant (empty = skip it)")
    ap.add_argument("--loads", type=float, nargs="+", default=[1.0, 5.0])
    ap.add_argument("--hours", type=float, default=24)
    ap.add_argument("--step", type=float, default=10)
    ap.add_argument("--terminals", type=int, default=300)
    ap.add_argument("--out", type=Path, default=Path(__file__).parent / "results")
    a = ap.parse_args()

    blocked = [frozenset()] + ([frozenset(a.block)] if a.block else [])
    scenarios = [
        cfg.Scenario(constellation=cfg.CONSTELLATIONS[n], mode=m, blocked_gateways=b, load=l,
                     terminals=a.terminals, duration_s=a.hours * 3600, step_s=a.step)
        for n, m, b, l in itertools.product(a.sats, a.modes, blocked, a.loads)
    ]
    print(f"Running {len(scenarios)} scenarios ({a.hours:g} h, {a.step:g} s steps)...")
    t0 = time.time()
    with ProcessPoolExecutor() as pool:
        out = list(pool.map(_one, scenarios))
    a.out.mkdir(parents=True, exist_ok=True)
    summary = pd.DataFrame([s for s, _ in out])
    pd.concat([c for _, c in out]).to_csv(a.out / "by_class.csv", index=False)
    summary.to_csv(a.out / "summary.csv", index=False)
    print(f"Done in {time.time() - t0:.0f} s -> {a.out}/summary.csv, by_class.csv\n")
    print(summary[KEY_COLUMNS].to_markdown(index=False, floatfmt=".3g"))


if __name__ == "__main__":
    main()
