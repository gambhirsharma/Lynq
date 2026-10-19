"""The optimisation problem: decision variables <-> constellation design, repair, constraints and objectives.

A genome is a tuple of integer indices into the choice lists below: one block of SHELL_GENES per shell (up to
--max-shells), then one design-wide gene (inter-shell links). Every variable is discrete, so every evaluation
is cached on the repaired genome.

Objectives (all minimised):  f1 = 10-year TCO (M EUR),  f2 = alarm latency p99 (ms),  f3 = 1 - coverage_mean.
Constraint: coverage_mean >= floor (default 0.90); optional budget on capex. Violation 0 = feasible.
"""
from __future__ import annotations

import math
import sys
import time
from dataclasses import dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "05-global-coverage"))

from globalnet import config as cfg          # noqa: E402
from globalnet.model import evaluate, link_rate_bps   # noqa: E402
from optimize import coverage_half_angle_rad, min_spp   # noqa: E402

import costmodel as cm                       # noqa: E402

ALTS = (450, 500, 550, 600, 700, 800, 1000, 1200)
FAMILIES = ((53.0, "delta"), (70.0, "delta"), (87.0, "delta"), (87.0, "star"), (97.6, "star"))
PLANES = tuple(range(2, 25))
SPP = tuple(range(2, 41))
PHASING = ("0", "1", "2", "half")            # Walker F; "half" = P // 2
TECHS = cfg.ISL_TECHS                        # none, rf, optical
CROSS = (0, 1, 2)                            # cross-plane terminals per carrying satellite
RELAY = (1, 2, 4)                            # every n-th satellite carries them

SHELL_GENES = ("active", "alt", "family", "planes", "spp", "phasing", "tech_in", "tech_x", "cross", "relay")
CHOICES = dict(active=(0, 1), alt=ALTS, family=FAMILIES, planes=PLANES, spp=SPP, phasing=PHASING,
               tech_in=TECHS, tech_x=TECHS, cross=CROSS, relay=RELAY)
ORDINAL = {"alt", "planes", "spp", "phasing"}   # mutate by small steps; the rest reset at random
INACTIVE = (0, 2, 3, 4, 8, 1, 2, 0, 0, 0)      # canonical genes of a switched-off shell


def n_genes(max_shells: int) -> int:
    return len(SHELL_GENES) * max_shells + 1


def gene_sizes(max_shells: int) -> list[int]:
    return [len(CHOICES[g]) for g in SHELL_GENES] * max_shells + [2]


def gene_names(max_shells: int) -> list[str]:
    return [f"s{k}_{g}" for k in range(max_shells) for g in SHELL_GENES] + ["inter_shell"]


def _max_range_km(tech: str) -> float:
    """Longest crosslink that still closes, by bisection on the link budget."""
    lo, hi = 1.0, cfg.ISL_TECH[tech].max_km
    if link_rate_bps(tech, hi) > 0:
        return hi
    for _ in range(50):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if link_rate_bps(tech, mid) > 0 else (lo, mid)
    return lo


MAX_RANGE_KM = {t: _max_range_km(t) for t in ("rf", "optical")}


def repair(g: tuple, max_shells: int, max_sats: int) -> tuple:
    """Make a genome consistent and canonical, so equal designs share one cache entry."""
    g, L = list(g), len(SHELL_GENES)
    blocks = [g[k * L:(k + 1) * L] for k in range(max_shells)]
    blocks[0][0] = 1
    for b in blocks:
        if not b[0]:
            b[:] = INACTIVE
            continue
        _, alt, _, p, s, _, t_in, t_x, cross, relay = b
        h, S = ALTS[alt], SPP[s]
        if TECHS[t_x] == "none" or CROSS[cross] == 0 or PLANES[p] < 2:
            b[7], b[8], b[9] = 0, 0, 0
        # in-plane spacing is fixed by S: terminals that can never close their link are dropped
        if TECHS[t_in] != "none" and 2 * (cfg.RE_KM + h) * math.sin(math.pi / S) > MAX_RANGE_KM[TECHS[t_in]]:
            b[6] = 0
    active = [b for b in blocks if b[0]]
    while sum(PLANES[b[3]] * SPP[b[4]] for b in active) > max_sats:   # trim the largest shell
        big = max(active, key=lambda b: PLANES[b[3]] * SPP[b[4]])
        if big[4] == 0:
            break
        big[4] -= 1
    inter = g[-1] if len(active) > 1 else 0
    return tuple(x for b in blocks for x in b) + (inter,)


def genome(specs: list[dict], max_shells: int, inter_shell: bool = False) -> tuple:
    """Genome from readable shell specs, e.g. dict(alt=550, family=(87.0, "star"), planes=12, spp=20)."""
    out = []
    for k in range(max_shells):
        if k >= len(specs):
            out += INACTIVE
            continue
        sp = dict(active=1, phasing="1", tech_in="optical", tech_x="optical", cross=2, relay=1) | specs[k]
        out += [CHOICES[n].index(sp[n]) for n in SHELL_GENES]
    return tuple(out) + (int(inter_shell),)


def design(g: tuple, max_shells: int, polar_off_deg: float = 90.0) -> cfg.Design:
    L, shells = len(SHELL_GENES), []
    for k in range(max_shells):
        active, alt, fam, p, s, f, t_in, t_x, cross, relay = g[k * L:(k + 1) * L]
        if not active:
            continue
        P, S = PLANES[p], SPP[s]
        F = P // 2 if PHASING[f] == "half" else int(PHASING[f]) % P
        inc, pattern = FAMILIES[fam]
        isl = cfg.ShellIsl(TECHS[t_in], TECHS[t_x], CROSS[cross], RELAY[relay], polar_off_deg)
        shells.append(cfg.Shell(P, S, float(ALTS[alt]), inc, pattern, F, isl))
    shells = tuple(shells)
    return cfg.Design(label(shells, bool(g[-1])), shells, inter_shell=bool(g[-1]), acquisition=True)


def label(shells, inter_shell: bool) -> str:
    out = " + ".join(f"{s.label}/F{s.phasing} [{s.isl.label}]" for s in shells)
    return out + (" +inter-shell" if inter_shell else "")


def coverage_upper_bound(d: cfg.Design) -> float:
    """Share of Earth inside the union of all footprints can be at most the sum of the cap areas."""
    return min(1.0, sum(s.size * (1 - math.cos(coverage_half_angle_rad(s.altitude_km))) / 2 for s in d.shells))


@dataclass(frozen=True)
class Settings:
    max_shells: int = 2
    max_sats: int = 800
    floor: float = 0.90              # minimum coverage_mean
    budget_meur: float = math.inf    # optional cap on initial capex
    hours: float = 3
    step_s: float = 120
    grid: int = 1000
    polar_off_deg: float = 90.0      # robustness scenario: cross-plane lasers off near the poles


def evaluate_genome(g: tuple, st: Settings, cost: cm.CostParams = cm.CostParams(), **model_kw) -> dict:
    """One design: decode, cost, prune or simulate, objectives and constraint violation."""
    t0 = time.time()
    d = design(g, st.max_shells, st.polar_off_deg)
    c = cm.tco(d, cost)
    row = dict(key=",".join(map(str, g)), shells=d.name, sats=d.size, planes=sum(s.planes for s in d.shells),
               n_shells=len(d.shells), inter_shell=d.inter_shell,
               isl_techs="/".join(sorted({t for s in d.shells for t in (s.isl.tech_in, s.isl.tech_x) if t != "none"}))
               or "none",
               altitudes="/".join(f"{s.altitude_km:g}" for s in d.shells),
               hours=st.hours, step_s=st.step_s, grid_points=st.grid, **c)
    bound = coverage_upper_bound(d)
    if not c["feasible"] or bound < st.floor:   # stage 0: pruned without simulating
        row.update(simulated=False, coverage_mean=bound if c["feasible"] else 0.0, full_coverage=False,
                   latency_p99_ms=math.nan, violation=1.0 if not c["feasible"] else st.floor - bound)
    else:
        s = evaluate(d, hours=st.hours, step_s=st.step_s, grid_points=st.grid, **model_kw).summary()
        s.pop("design"), s.pop("shells"), s.pop("sats"), s.pop("grid_points")
        row.update(simulated=True, **s)
        row["violation"] = max(0.0, st.floor - s["coverage_mean"]) + max(0.0, c["capex_meur"] - st.budget_meur) / 100
    p99 = row["latency_p99_ms"]
    row.update(f_cost=row["tco_meur"], f_latency=p99 if p99 == p99 else 1e4, f_cov=1 - row["coverage_mean"],
               runtime_s=round(time.time() - t0, 1))
    return row
