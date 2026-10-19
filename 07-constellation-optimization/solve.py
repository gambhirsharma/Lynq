"""Multi-objective constellation optimisation: cost vs latency vs coverage, mixed altitudes, RF vs optical ISL.

Stages (each resumable: every evaluation is cached in results/evals_*.csv):
  1. search   NSGA-II over the mixed-integer design space at screen fidelity (default 3 h / 120 s / 1,000 points).
  2. tiers    For each service tier (coverage + p99 target), the cheapest design found, improved by local search.
  3. confirm  Tier answers and a spread of Pareto points re-run at full fidelity (24 h / 60 s / 2,000 points);
              the knee of the confirmed front.
  4. robust   The picks under one satellite failure, a gateway outage and polar laser shutoff.
  5. report   Cost sensitivity (re-costing only, no re-simulation) and results/report.md.

    python solve.py                          # everything (~45 min on 8 cores)
    python solve.py --pop 48 --gens 20       # quicker search
    python solve.py --stage report           # only rebuild the report from saved CSVs
    python solve.py --max-shells 3 --floor 0.95
"""
from __future__ import annotations

import os

os.environ.setdefault("OMP_NUM_THREADS", "1")       # one process per core; keep numpy single-threaded
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")

import argparse
import math
import time
from concurrent.futures import ProcessPoolExecutor
from dataclasses import replace
from pathlib import Path

import numpy as np
import pandas as pd

import problem as pb
import report

# Service tiers: (coverage requirement, p99 target in ms). "full" = every grid point served at every step.
TIERS = (("full", None), ("full", 150), ("full", 120), ("full", 100), ("full", 90),
         (0.99, 150), (0.99, 100), (0.95, 150))
HEADLINE = ("full", 100)


def tier_label(t) -> str:
    cov, lat = t
    c = "full coverage" if cov == "full" else f"coverage >= {cov:.0%}"
    return c + ("" if lat is None else f", p99 <= {lat:g} ms")


def meets(df: pd.DataFrame, t) -> pd.Series:
    cov, lat = t
    ok = (df.violation == 0) & df.simulated.astype(bool)
    ok &= (df.full_coverage.astype(str) == "True") if cov == "full" else (df.coverage_mean >= cov)
    if lat is not None:
        ok &= df.latency_p99_ms <= lat
    return ok


# --- Evaluation cache ------------------------------------------------------------------
class Evaluator:
    """Parallel, cached evaluation of genomes at one fidelity; rows are appended to a CSV as they finish."""

    def __init__(self, st: pb.Settings, path: Path, pool: ProcessPoolExecutor, **model_kw):
        self.st, self.path, self.pool, self.kw = st, path, pool, model_kw
        self.rows: dict[tuple, dict] = {}
        if path.exists():
            for r in pd.read_csv(path).to_dict("records"):
                self.rows[tuple(int(x) for x in r["key"].split(","))] = r

    def __call__(self, genomes) -> list[dict]:
        todo = list(dict.fromkeys(g for g in genomes if g not in self.rows))
        futs = {g: self.pool.submit(pb.evaluate_genome, g, self.st, **self.kw) for g in todo}
        new = []
        for g, f in futs.items():
            try:
                self.rows[g] = f.result()
            except Exception as e:   # one bad design must not kill the run
                print(f"  FAILED {pb.design(g, self.st.max_shells).name}: {e}")
                self.rows[g] = dict(key=",".join(map(str, g)), simulated=False, violation=9.0, f_cost=math.inf,
                                    f_latency=1e4, f_cov=1.0)
            new.append(self.rows[g])
        if new:
            pd.DataFrame(new).to_csv(self.path, mode="a", header=not self.path.exists(), index=False)
        return [self.rows[g] for g in genomes]

    def frame(self) -> pd.DataFrame:
        return pd.DataFrame(list(self.rows.values()))


# --- NSGA-II ---------------------------------------------------------------------------
def _objectives(rows) -> tuple[np.ndarray, np.ndarray]:
    F = np.array([[r["f_cost"], r["f_latency"], r["f_cov"]] for r in rows], float)
    return F, np.array([r["violation"] for r in rows], float)


def nondominated_sort(F: np.ndarray, V: np.ndarray) -> list[list[int]]:
    """Fronts under constrained domination: feasible beats infeasible, less violation beats more."""
    n = len(F)
    def dom(a, b):
        if V[a] == 0 and V[b] > 0:
            return True
        if V[a] > 0 or V[b] > 0:
            return V[a] < V[b]
        return bool(np.all(F[a] <= F[b]) and np.any(F[a] < F[b]))
    S, cnt = [[] for _ in range(n)], np.zeros(n, int)
    for a in range(n):
        for b in range(a + 1, n):
            if dom(a, b):
                S[a].append(b); cnt[b] += 1
            elif dom(b, a):
                S[b].append(a); cnt[a] += 1
    fronts, cur = [], [i for i in range(n) if cnt[i] == 0]
    while cur:
        fronts.append(cur)
        nxt = []
        for a in cur:
            for b in S[a]:
                cnt[b] -= 1
                if cnt[b] == 0:
                    nxt.append(b)
        cur = nxt
    return fronts


def crowding(F: np.ndarray) -> np.ndarray:
    n = len(F)
    d = np.zeros(n)
    if n <= 2:
        return np.full(n, np.inf)
    for m in range(F.shape[1]):
        o = np.argsort(F[:, m])
        span = F[o[-1], m] - F[o[0], m]
        d[o[0]] = d[o[-1]] = np.inf
        if span > 0:
            d[o[1:-1]] += (F[o[2:], m] - F[o[:-2], m]) / span
    return d


def select(rows, k: int) -> tuple[list[int], np.ndarray, np.ndarray]:
    """Environmental selection: best k by front, then crowding. Returns indices, rank and crowding of those."""
    F, V = _objectives(rows)
    rank, crowd = np.zeros(len(rows), int), np.zeros(len(rows))
    keep = []
    for r, front in enumerate(nondominated_sort(F, V)):
        cd = crowding(F[front]) if V[front[0]] == 0 else -V[front]
        rank[front], crowd[front] = r, cd
        if len(keep) + len(front) <= k:
            keep += front
        else:
            keep += [front[i] for i in np.argsort(-cd)[:k - len(keep)]]
            break
    return keep, rank[keep], crowd[keep]


def variation(pop, rank, crowd, n: int, sizes, names, rng, st) -> list[tuple]:
    L, seen, out = len(pb.SHELL_GENES), set(pop), []

    def tournament():
        a, b = rng.integers(len(pop), size=2)
        return pop[a] if (rank[a], -crowd[a]) <= (rank[b], -crowd[b]) else pop[b]

    while len(out) < n:
        for _ in range(20):
            a, b = tournament(), tournament()
            child = []
            for k in range(st.max_shells):   # crossover shell by shell, so good shells survive intact
                src, oth = (a, b) if rng.random() < 0.5 else (b, a)
                child += [oth[k * L + i] if rng.random() < 0.15 else src[k * L + i] for i in range(L)]
            child.append(a[-1] if rng.random() < 0.5 else b[-1])
            for i, (size, name) in enumerate(zip(sizes, names)):
                if rng.random() < 1.5 / len(sizes):
                    if name.split("_", 1)[1] in pb.ORDINAL:
                        child[i] = int(np.clip(child[i] + rng.choice([-3, -2, -1, 1, 2, 3], p=[.1, .2, .2, .2, .2, .1]),
                                               0, size - 1))
                    else:
                        child[i] = int(rng.integers(size))
            child = pb.repair(tuple(child), st.max_shells, st.max_sats)
            if child not in seen:
                break
        seen.add(child)
        out.append(child)
    return out


def seeds(st: pb.Settings) -> list[tuple]:
    """Known designs: the 05 study's picks, an Iridium-like RF mesh, the proposal's RF/optical hybrid, a 2-altitude mix."""
    star, inc53 = (87.0, "star"), (53.0, "delta")
    specs = [
        [dict(alt=800, family=star, planes=6, spp=11)],
        [dict(alt=800, family=star, planes=6, spp=11, tech_in="rf", tech_x="rf")],
        [dict(alt=1000, family=star, planes=6, spp=12)],
        [dict(alt=1200, family=star, planes=8, spp=15)],
        [dict(alt=550, family=star, planes=12, spp=20)],
        [dict(alt=550, family=star, planes=12, spp=20, tech_in="rf", tech_x="rf")],
        [dict(alt=550, family=star, planes=12, spp=20, tech_in="rf", relay=4)],
        [dict(alt=550, family=inc53, planes=10, spp=12, tech_in="rf", cross=1), dict(alt=1200, family=star, planes=5, spp=11)],
    ]
    out = [pb.genome(s[:st.max_shells], st.max_shells) for s in specs]
    out.append(pb.genome(specs[-1][:st.max_shells], st.max_shells, inter_shell=st.max_shells > 1))
    return [pb.repair(g, st.max_shells, st.max_sats) for g in out]


def random_genome(sizes, names, rng, st) -> tuple:
    g = [int(rng.integers(s)) for s in sizes]
    for k in range(st.max_shells):   # start shells near or above the gap-free satellite count per plane
        i = k * len(pb.SHELL_GENES)
        floor = pb.min_spp(pb.ALTS[g[i + 1]]) // (2 if st.max_shells > 1 else 1)
        g[i + 4] = int(rng.integers(max(0, floor - 2), len(pb.SPP)))
        if k > 0 and rng.random() < 0.4:
            g[i] = 0
    return pb.repair(tuple(g), st.max_shells, st.max_sats)


def search(ev: Evaluator, a, st: pb.Settings) -> list[tuple]:
    rng = np.random.default_rng(a.seed)
    sizes, names = pb.gene_sizes(st.max_shells), pb.gene_names(st.max_shells)
    pop = list(dict.fromkeys(seeds(st)))
    while len(pop) < a.pop:
        g = random_genome(sizes, names, rng, st)
        if g not in pop:
            pop.append(g)
    rows = ev(pop)
    keep, rank, crowd = select(rows, a.pop)
    pop = [pop[i] for i in keep]
    t0 = time.time()
    for gen in range(1, a.gens + 1):
        kids = variation(pop, rank, crowd, a.pop, sizes, names, rng, st)
        allg = pop + kids
        rows = ev(allg)
        keep, rank, crowd = select(rows, a.pop)
        pop = [allg[i] for i in keep]
        df = pd.DataFrame([rows[i] for i in keep])
        full = df[meets(df, ("full", None))] if len(df) else df
        head = df[meets(df, HEADLINE)] if len(df) else df
        print(f"gen {gen:>3}/{a.gens}  evals {len(ev.rows):>5}  feasible {int((df.violation == 0).sum()):>3}  "
              f"front {int((rank == 0).sum()):>3}  "
              + (f"cheapest full: {full.sats.iloc[full.f_cost.argmin()]} sats EUR {full.f_cost.min():.0f}M  "
                 if len(full) else "no full coverage yet  ")
              + (f"cheapest full+p99<=100: {head.sats.iloc[head.f_cost.argmin()]} sats EUR {head.f_cost.min():.0f}M"
                 if len(head) else "")
              + f"  [{(time.time() - t0) / 60:.1f} min]", flush=True)
    return pop


# --- Tiers: cheapest per tier + local search ------------------------------------------
def neighbours(g: tuple, st: pb.Settings) -> list[tuple]:
    sizes, names, out = pb.gene_sizes(st.max_shells), pb.gene_names(st.max_shells), []
    L = len(pb.SHELL_GENES)
    for i, (size, name) in enumerate(zip(sizes, names)):
        if i < len(names) - 1 and not g[(i // L) * L] and not name.endswith("_active"):
            continue   # genes of a switched-off shell
        short = name.split("_", 1)[1] if "_" in name else name
        vals = [g[i] - 1, g[i] + 1] if short in pb.ORDINAL else range(size)
        for v in vals:
            if 0 <= v < size and v != g[i]:
                out.append(pb.repair(g[:i] + (v,) + g[i + 1:], st.max_shells, st.max_sats))
    return list(dict.fromkeys(x for x in out if x != g))


def tier_winners(df: pd.DataFrame, n: int = 1) -> dict:
    out = {}
    for t in TIERS:
        ok = df[meets(df, t)].sort_values(["f_cost", "f_latency"])
        out[t] = [tuple(int(x) for x in k.split(",")) for k in ok.key.head(n)]
    return out


def refine(ev: Evaluator, st: pb.Settings, rounds: int) -> None:
    for r in range(rounds):
        best = {g for gs in tier_winners(ev.frame()).values() for g in gs}
        before = tier_winners(ev.frame())
        batch = [n for g in best for n in neighbours(g, st)]
        print(f"local search round {r + 1}/{rounds}: {len(best)} tier winners, {len(batch)} neighbours", flush=True)
        ev(batch)
        if tier_winners(ev.frame()) == before:
            break


# --- Confirmation, knee, robustness ----------------------------------------------------
def front_rows(df: pd.DataFrame) -> pd.DataFrame:
    ok = df[(df.violation == 0) & df.simulated.astype(bool)].reset_index(drop=True)
    if not len(ok):
        return ok
    F = ok[["f_cost", "f_latency", "f_cov"]].to_numpy(float)
    first = nondominated_sort(F, np.zeros(len(F)))[0]
    return ok.iloc[first].sort_values("f_cost")


def knee(front: pd.DataFrame) -> pd.Series:
    """Point of the front closest to the ideal point after scaling each objective to [0, 1]."""
    F = front[["f_cost", "f_latency", "f_cov"]].to_numpy(float)
    span = F.max(axis=0) - F.min(axis=0)
    Z = (F - F.min(axis=0)) / np.where(span > 0, span, 1)
    return front.iloc[int(np.linalg.norm(Z, axis=1).argmin())]


def confirm(screen: Evaluator, full: Evaluator, a) -> pd.DataFrame:
    df = screen.frame()
    cands = tier_winners(df, a.confirm_tries)
    fr = front_rows(df)
    picks = np.unique(np.linspace(0, len(fr) - 1, min(a.front_points, len(fr))).round().astype(int)) if len(fr) else []
    front_g = [tuple(int(x) for x in fr.key.iloc[i].split(",")) for i in picks]
    todo = front_g + [g for gs in cands.values() for g in gs]
    print(f"confirming {len(set(todo))} designs at {a.hours:g} h / {a.step:g} s / {a.grid} points...", flush=True)
    full(todo)
    fdf = full.frame()
    rows = []
    for t in TIERS:
        hit = next((full.rows[g] for g in cands[t] if meets(pd.DataFrame([full.rows[g]]), t).iloc[0]), None)
        if hit is None:   # fall back to anything confirmed that meets the tier
            ok = fdf[meets(fdf, t)].sort_values("f_cost")
            hit = ok.iloc[0].to_dict() if len(ok) else None
        rows.append(dict(tier=tier_label(t), **(hit or {})))
        print(f"  {tier_label(t)}: " + (f"{hit['sats']} sats, EUR {hit['tco_meur']:.0f}M  {hit['shells']}" if hit
                                       else "none held at full fidelity"))
    return pd.DataFrame(rows)


def robustness(picks: pd.DataFrame, a, st_full: pb.Settings, pool) -> pd.DataFrame:
    st = replace(st_full, hours=a.robust_hours)
    rng = np.random.default_rng(a.seed + 1)
    jobs = []
    for _, p in picks.iterrows():
        g = tuple(int(x) for x in p.key.split(","))
        jobs.append((p.pick, "baseline", g, st, {}))
        for k in range(a.fail_draws):
            jobs.append((p.pick, f"1 satellite failed (draw {k + 1})", g, st,
                         dict(failed=frozenset({int(rng.integers(int(p.sats)))}))))
        jobs.append((p.pick, "Svalbard gateway down", g, st, dict(blocked=frozenset({"Svalbard"}))))
        jobs.append((p.pick, "cross-plane lasers off above 70 deg", g, replace(st, polar_off_deg=70.0), {}))
    futs = [(pick, sc, pool.submit(pb.evaluate_genome, g, s, **kw)) for pick, sc, g, s, kw in jobs]
    out = []
    for pick, sc, f in futs:
        r = f.result()
        out.append(dict(pick=pick, scenario=sc, sats=r["sats"], coverage_mean=r["coverage_mean"],
                        coverage_worst_point=r.get("coverage_worst_point"), max_gap_min=r.get("max_gap_min"),
                        latency_p99_ms=r["latency_p99_ms"], worst_point_p95_ms=r.get("worst_point_p95_ms")))
    return pd.DataFrame(out)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--stage", default="all", choices=["all", "search", "tiers", "confirm", "robust", "report"])
    ap.add_argument("--pop", type=int, default=80)
    ap.add_argument("--gens", type=int, default=40)
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--max-shells", type=int, default=2)
    ap.add_argument("--max-sats", type=int, default=800)
    ap.add_argument("--floor", type=float, default=0.90, help="minimum coverage_mean (constraint)")
    ap.add_argument("--budget", type=float, default=math.inf, help="cap on initial capex, M EUR")
    ap.add_argument("--screen", type=float, nargs=3, default=[3, 120, 1000], metavar=("HOURS", "STEP_S", "GRID"))
    ap.add_argument("--hours", type=float, default=24, help="confirmation fidelity")
    ap.add_argument("--step", type=float, default=60)
    ap.add_argument("--grid", type=int, default=2000)
    ap.add_argument("--refine-rounds", type=int, default=3)
    ap.add_argument("--confirm-tries", type=int, default=4)
    ap.add_argument("--front-points", type=int, default=16)
    ap.add_argument("--robust-hours", type=float, default=6)
    ap.add_argument("--fail-draws", type=int, default=4)
    ap.add_argument("--workers", type=int, default=os.cpu_count())
    ap.add_argument("--out", type=Path, default=Path(__file__).parent / "results")
    a = ap.parse_args()
    a.out.mkdir(parents=True, exist_ok=True)
    h, s, g = a.screen
    st_screen = pb.Settings(a.max_shells, a.max_sats, a.floor, a.budget, h, s, int(g))
    st_full = replace(st_screen, hours=a.hours, step_s=a.step, grid=a.grid)
    tag = f"k{a.max_shells}"
    t0 = time.time()
    with ProcessPoolExecutor(max_workers=a.workers) as pool:
        screen = Evaluator(st_screen, a.out / f"evals_screen_{tag}.csv", pool)
        full = Evaluator(st_full, a.out / f"evals_full_{tag}.csv", pool)
        if a.stage in ("all", "search"):
            print(f"NSGA-II: population {a.pop}, {a.gens} generations, {pb.n_genes(a.max_shells)} genes, "
                  f"screen {h:g} h / {s:g} s / {int(g)} points, {a.workers} workers ({len(screen.rows)} cached)")
            search(screen, a, st_screen)
        if a.stage in ("all", "tiers"):
            refine(screen, st_screen, a.refine_rounds)
        if a.stage in ("all", "confirm"):
            tiers = confirm(screen, full, a)
            tiers.to_csv(a.out / "tiers.csv", index=False)
            fr = front_rows(full.frame())
            fr.to_csv(a.out / "front.csv", index=False)
            k = knee(fr)
            print(f"knee of the confirmed front: {k.sats} sats, EUR {k.tco_meur:.0f}M, p99 {k.latency_p99_ms:.0f} ms, "
                  f"coverage {k.coverage_mean:.3f}  {k.shells}")
        if a.stage in ("all", "robust"):
            tiers, fr = pd.read_csv(a.out / "tiers.csv"), pd.read_csv(a.out / "front.csv")
            picks = pd.concat([knee(fr).to_frame().T.assign(pick="knee"),
                               tiers.dropna(subset=["key"]).assign(pick=lambda d: d.tier)])
            picks = picks.drop_duplicates("key")
            print(f"robustness: {len(picks)} picks at {a.robust_hours:g} h...", flush=True)
            robustness(picks, a, st_full, pool).to_csv(a.out / "robustness.csv", index=False)
    report.build(a.out, tag, st_screen, HEADLINE, TIERS)
    print(f"done in {(time.time() - t0) / 60:.1f} min -> {a.out}/report.md")


if __name__ == "__main__":
    main()
