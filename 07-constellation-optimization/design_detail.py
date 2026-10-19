"""Reproduce every number in DESIGN-7x16.md: geometry, crosslinks, satellite, cost and 24 h performance.

    .venv/bin/python design_detail.py            # 7x16 (recommended) and 7x15, ~2 min on 2 cores
    .venv/bin/python design_detail.py 16         # one design
"""
from __future__ import annotations

import os

os.environ.setdefault("OMP_NUM_THREADS", "1")

import math
import sys
from concurrent.futures import ProcessPoolExecutor

import numpy as np

import costmodel as cm
from globalnet import config as cfg
from globalnet.geometry import Fleet
from globalnet.model import evaluate, isl_edges, link_rate_bps

ALT_KM, INC_DEG, PLANES = 700.0, 87.0, 7


def design(spp: int) -> cfg.Design:
    """The report's pick: Walker star, F0, RF in-plane + 2 RF cross-plane terminals."""
    isl = cfg.ShellIsl("rf", "rf", 2, 1, 90.0)
    shell = cfg.Shell(PLANES, spp, ALT_KM, INC_DEG, "star", 0, isl)
    return cfg.Design(f"{PLANES}x{spp}", (shell,), acquisition=True)


def rf_margin_db(km: float) -> float:
    """dB above the 1 Mbps floor of the RF crosslink budget at this range (low SNR: rate ~ SNR)."""
    t = cfg.ISL_TECH["rf"]
    snr_floor = 2 ** (t.min_rate_bps / (cfg.IMPL_EFFICIENCY * t.bw_hz)) - 1
    fspl = 20 * math.log10(km) + 20 * math.log10(t.freq_ghz * 1e3) + 32.44
    snr_db = t.eirp_dbw - fspl - t.losses_db + t.gt_dbk - cfg.K_BOLTZMANN_DBW - 10 * math.log10(t.bw_hz)
    return snr_db - 10 * math.log10(snr_floor)


def report(spp: int) -> str:
    d = design(spp)
    w = Fleet(d).shells[0]
    lam = math.acos(cfg.RE_KM * math.cos(math.radians(cfg.TERMINAL_MIN_EL_DEG)) / (cfg.RE_KM + ALT_KM)) \
        - math.radians(cfg.TERMINAL_MIN_EL_DEG)
    out = [f"## {d.name}: {d.size} satellites", "", "### Geometry",
           f"plane spacing           {180 / PLANES:.1f} deg (star, 180 deg spread)",
           f"in-plane spacing        {360 / spp:.1f} deg",
           f"period                  {w.period_s / 60:.1f} min",
           f"speed                   {math.sqrt(cfg.MU_KM3_S2 / (cfg.RE_KM + ALT_KM)):.2f} km/s",
           f"coverage radius         {lam * cfg.RE_KM:,.0f} km at {cfg.TERMINAL_MIN_EL_DEG:g} deg elevation",
           f"longest pass            {2 * math.degrees(lam) / 360 * w.period_s / 60:.1f} min (overhead, Earth rotation ignored)"]

    # crosslink geometry over one day, sampled every 5 min
    f = Fleet(d)
    inp, crs, links = [], [], []
    for t in np.arange(0, 86400, 300):
        I, J, km = isl_edges(f, f.ecef(t), d)[:3]
        same = w.plane[I] == w.plane[J]
        inp += list(km[same]); crs += list(km[~same]); links.append(len(I))
    inp, crs = np.array(inp), np.array(crs)
    possible = PLANES * spp + (PLANES - 1) * spp   # ring per plane + one cross link per satellite, no seam
    rate = lambda km: float(link_rate_bps("rf", np.array([km]))[0]) / 1e6
    out += ["", "### Crosslinks (links that close)",
            f"in-plane distance       {inp.mean():,.0f} km  rate {rate(inp.mean()):.2f} Mbps  margin {rf_margin_db(inp.mean()):.2f} dB",
            f"cross-plane distance    {crs.min():,.0f} / {np.median(crs):,.0f} / {crs.max():,.0f} km (min / median / max)",
            f"widest cross link       rate {rate(crs.max()):.2f} Mbps  margin {rf_margin_db(crs.max()):.2f} dB",
            f"links up, mean          {np.mean(links):.0f} of {possible} possible ({1 - np.mean(links) / possible:.0%} down)",
            f"geometric in-plane      {2 * (cfg.RE_KM + ALT_KM) * math.sin(math.pi / spp):,.0f} km (chord), "
            f"margin {rf_margin_db(2 * (cfg.RE_KM + ALT_KM) * math.sin(math.pi / spp)):.2f} dB"]

    p = cm.CostParams()
    term = cm.terminals(d)[0]
    sat = cm.satellite(d.shells[0], term, p)
    bus = next(b for b in cm.BUSES if b.name == sat["bus"])
    c = cm.tco(d, p)
    otvs = math.ceil(spp * sat["mass_kg"] / p.otv_capacity_kg)
    out += ["", "### Satellite",
            f"bus / wet mass / power  {sat['bus']} / {sat['mass_kg']:.1f} kg / {sat['power_w']:.0f} W",
            f"delta-v / life          {sat['dv_ms']:.0f} m/s / {sat['life_yr']:g} yr",
            f"unit cost               EUR {sat['unit_meur']:.2f} M = bus {bus.cost_meur} + payload {p.payload_meur} "
            f"+ propulsion {p.prop_system_meur} + {term['rf']:g} RF x {cfg.ISL_TECH['rf'].cost_meur}",
            "", "### Cost (M EUR)",
            f"capex                   {c['capex_meur']:.1f} = build {d.size * sat['unit_meur']:.1f} "
            f"+ launch {c['launch_meur'] / 2:.1f} + OTVs {c['planes_meur'] / 2:.1f} ({otvs} per plane)",
            f"10-year TCO             {c['tco_meur']:.1f} = build {c['build_meur']:.1f} + launch {c['launch_meur']:.1f} "
            f"+ OTVs {c['planes_meur']:.1f} + ground {c['ground_meur']:.1f} + ops {c['ops_meur']:.1f}"]

    r = evaluate(d, hours=24, step_s=60, grid_points=2000)
    s = r.summary()
    out += ["", "### Performance (24 h, 60 s, 2,000 points)",
            f"coverage mean / worst   {s['coverage_mean']:.4f} / {s['coverage_worst_point']:.4f}  full={s['full_coverage']}  "
            f"max gap {s['max_gap_min']:g} min",
            f"sats in view min / mean {s['min_sats_in_view']} / {s['mean_sats_in_view']:.2f}",
            f"latency p50/p95/p99/max {s['latency_p50_ms']:.1f} / {s['latency_p95_ms']:.1f} / {s['latency_p99_ms']:.1f} / "
            f"{s['latency_max_ms']:.1f} ms",
            f"worst place p95         {s['worst_point_p95_ms']:.1f} ms",
            f"within 75 / 100 ms      {s['within_75ms']:.1%} / {s['within_100ms']:.1%}",
            "", "| Band | Coverage | Max gap | p50 ms | p95 ms |", "|---|---:|---:|---:|---:|"]
    for b in r.by_latitude(15.0).itertuples():
        out.append(f"| {b.band} | {b.coverage:.4f} | {b.max_gap_min:g} | {b.p50_ms:.1f} | {b.p95_ms:.1f} |")
    return "\n".join(out) + "\n"


if __name__ == "__main__":
    spps = [int(x) for x in sys.argv[1:]] or [16, 15]
    with ProcessPoolExecutor(len(spps)) as pool:
        for text in pool.map(report, spps):
            print(text)
