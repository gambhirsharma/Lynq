# Lynq NTN-Pulse: constellation optimisation

Multi-objective search for the LEO constellation that best trades **10-year cost**, **latency (p99)** and
**coverage**. Altitudes can be mixed (up to 2 shells by default, `--max-shells 3`). ISL technology (RF or
optical), the number of crosslink terminals per satellite and the relay subset are decision variables. The full
formulation is in [PLAN.md](PLAN.md).

It reuses the physics of `../05-global-coverage/globalnet` (orbits, global grid, gateways, Dijkstra over the
mesh), extended there for RF/optical links, brick / +Grid / relay-subset layouts, polar laser shutoff,
inter-shell links, optical acquisition and failed satellites. The defaults reproduce the 05 results.

| File | What it does |
|---|---|
| `costmodel.py` | Satellite mass and bus, Δv and propellant, lifetime by altitude, launch, per-plane OTVs, ops: 10-year TCO |
| `problem.py` | Decision variables ↔ design, repair, analytic pruning, objectives and constraint |
| `solve.py` | NSGA-II → local search per service tier → full-fidelity confirmation → robustness |
| `report.py` | `results/report.md`: answer, tier table, Pareto front, RF vs optical, mixed altitude, cost sensitivity |

## Run

```bash
cd 05-global-coverage && python3 -m venv .venv && .venv/bin/pip install -r requirements.txt && cd ..
cd 07-constellation-optimization
../05-global-coverage/.venv/bin/python -m pytest -q          # 21 tests, ~10 s
../05-global-coverage/.venv/bin/python solve.py               # ~1 h on 8 cores
../05-global-coverage/.venv/bin/python solve.py --pop 48 --gens 20   # quicker
../05-global-coverage/.venv/bin/python solve.py --stage report       # rebuild the report from saved CSVs
```

On MeluXina: set `--account` in `sweep.slurm`, build the venv on a compute node, then `sbatch sweep.slurm`
(any `solve.py` arguments pass through). Every evaluation is cached in `results/evals_*.csv`, so a re-submitted
job resumes where it stopped.

Outputs in `results/`: `evals_screen_k2.csv`, `evals_full_k2.csv`, `tiers.csv`, `front.csv`, `robustness.csv`,
`report.md`. The headline answer is the cheapest design with full coverage and p99 ≤ 100 ms, plus the knee of the
confirmed front.

## Limits

- Cost numbers are parametric, calibrated to the proposal's 90 satellites (~€0.75 M all-in each). Check the
  terminal, launch and per-plane prices in `costmodel.CostParams` and `globalnet/config.py:ISL_TECH`.
- Coverage and latency only: no traffic or capacity, so optical's throughput advantage is not valued.
- Circular orbits, no J2. The 28 gateways are fixed.
