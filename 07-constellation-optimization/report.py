"""Build results/report.md from the CSVs solve.py writes, including the cost sensitivity (re-costing only)."""
from __future__ import annotations

import math
from pathlib import Path

import pandas as pd

import costmodel as cm
import problem as pb

DESIGN_COLS = ["sats", "planes", "shells", "buses", "tco_meur", "capex_meur", "coverage_mean", "coverage_worst_point",
               "max_gap_min", "min_sats_in_view", "latency_p50_ms", "latency_p99_ms", "worst_point_p95_ms"]

SENSITIVITY = {
    "baseline": {},
    "optical terminal -50%": dict(optical_terminal_scale=0.5),
    "optical terminal +50%": dict(optical_terminal_scale=1.5),
    "RF terminal -50%": dict(rf_terminal_scale=0.5),
    "RF terminal +50%": dict(rf_terminal_scale=1.5),
    "launch EUR/kg -50%": dict(launch_meur_per_kg=0.003),
    "launch EUR/kg +50%": dict(launch_meur_per_kg=0.009),
    "per-plane cost -50%": dict(plane_meur=0.75),
    "per-plane cost +50%": dict(plane_meur=2.25),
    "dedicated launch per plane (EUR 7.5M)": dict(plane_meur=7.5),
}
OPTICAL_SCALES = (0.1, 0.25, 0.5, 0.75, 1.0, 1.5, 2.0, 3.0, 5.0)


def _table(df: pd.DataFrame, cols) -> str:
    cols = [c for c in cols if c in df]
    return df[cols].to_markdown(index=False, floatfmt=".4g") if len(df) else "_none_"


def _fidelity(df: pd.DataFrame) -> str:
    if not len(df) or "hours" not in df or df.hours.isna().all():
        return "n/a"
    r = df.dropna(subset=["hours"]).iloc[0]
    return f"{r.hours:g} h / {r.step_s:g} s / {int(r.grid_points)} points"


def recost(df: pd.DataFrame, st: pb.Settings, p: cm.CostParams) -> pd.Series:
    designs = df.key.map(lambda k: pb.design(tuple(int(x) for x in k.split(",")), st.max_shells))
    return designs.map(lambda d: cm.tco(d, p)["tco_meur"])


def build(out: Path, tag: str, st: pb.Settings, headline, tiers) -> None:
    from solve import meets, tier_label, knee   # solve imports this module

    screen = pd.read_csv(out / f"evals_screen_{tag}.csv").drop_duplicates("key", keep="last")
    tier_df = pd.read_csv(out / "tiers.csv") if (out / "tiers.csv").exists() else pd.DataFrame()
    front = pd.read_csv(out / "front.csv") if (out / "front.csv").exists() else pd.DataFrame()
    rob = pd.read_csv(out / "robustness.csv") if (out / "robustness.csv").exists() else pd.DataFrame()
    md = ["# Constellation optimisation: results", "",
          f"{len(screen)} designs evaluated at screen fidelity ({st.hours:g} h / {st.step_s:g} s / {st.grid} points), "
          f"{int(screen.simulated.sum())} simulated, the rest pruned analytically (coverage bound or no bus fits). "
          f"Up to {st.max_shells} shells, coverage floor {st.floor:.0%}. Costs are 10-year TCO in M EUR.", ""]

    head = tier_df[tier_df.tier == tier_label(headline)] if len(tier_df) else tier_df
    if len(head) and not pd.isna(head.iloc[0].get("sats")):
        h = head.iloc[0]
        md += ["## Answer", "",
               f"**Cheapest design with {tier_label(headline)} (confirmed at full fidelity): "
               f"{int(h.sats)} satellites**, `{h.shells}`, 10-year TCO EUR {h.tco_meur:.0f} M "
               f"(capex EUR {h.capex_meur:.0f} M), p99 {h.latency_p99_ms:.0f} ms, "
               f"worst-place p95 {h.worst_point_p95_ms:.0f} ms, bus {h.buses}.", ""]
    if len(front):
        k = knee(front)
        md += [f"**Knee of the confirmed 3-objective front: {int(k.sats)} satellites**, `{k.shells}`, "
               f"TCO EUR {k.tco_meur:.0f} M, p99 {k.latency_p99_ms:.0f} ms, coverage {k.coverage_mean:.1%}.", ""]

    md += [f"## Cheapest design per service tier (full fidelity: {_fidelity(tier_df)})", "",
           _table(tier_df, ["tier"] + DESIGN_COLS), ""]
    md += [f"## Pareto front: cost vs latency vs coverage (full fidelity: {_fidelity(front)})", "", _table(front, DESIGN_COLS), ""]

    # RF vs optical and single vs mixed altitude, from everything screened
    ok = screen[meets(screen, headline)]
    if len(ok):
        by_tech = ok.sort_values("tco_meur").groupby("isl_techs", as_index=False).first()
        md += [f"## RF vs optical: cheapest design per ISL technology, {tier_label(headline)} (screen fidelity)", "",
               _table(by_tech.sort_values("tco_meur"), ["isl_techs"] + DESIGN_COLS), ""]
        ok = ok.assign(mix=ok.n_shells.map({1: "single shell"}).fillna("mixed altitude")
                       + ok.inter_shell.map({True: " + inter-shell ISL", False: ""}))
        by_mix = ok.sort_values("tco_meur").groupby("mix", as_index=False).first()
        md += [f"## Single vs mixed altitude, {tier_label(headline)} (screen fidelity)", "",
               _table(by_mix.sort_values("tco_meur"), ["mix", "altitudes"] + DESIGN_COLS), ""]

        # Sensitivity: re-cost every screened design that meets the headline tier
        rows = []
        for name, kw in SENSITIVITY.items():
            c = recost(ok, st, cm.CostParams().scaled(**kw))
            w = ok.loc[c.idxmin()]
            rows.append(dict(scenario=name, sats=w.sats, shells=w.shells, isl_techs=w.isl_techs, tco_meur=c.min()))
        md += [f"## Cost sensitivity of the {tier_label(headline)} answer (re-costed, no re-simulation)", "",
               pd.DataFrame(rows).to_markdown(index=False, floatfmt=".4g"), ""]
        rows = []
        for sc in OPTICAL_SCALES:
            c = recost(ok, st, cm.CostParams().scaled(optical_terminal_scale=sc))
            w = ok.loc[c.idxmin()]
            rows.append(dict(optical_eur_m_per_terminal=sc * cm.cfg.ISL_TECH["optical"].cost_meur, sats=w.sats,
                             isl_techs=w.isl_techs, shells=w.shells, tco_meur=c.min()))
        md += ["## RF / optical crossover: winner vs optical terminal price", "",
               pd.DataFrame(rows).to_markdown(index=False, floatfmt=".4g"), ""]

    if len(rob):
        md += ["## Robustness of the picks (shorter run at full grid resolution)", "",
               rob.to_markdown(index=False, floatfmt=".4g"), ""]
    (out / "report.md").write_text("\n".join(md))
    print("\n".join(md[:12]))
