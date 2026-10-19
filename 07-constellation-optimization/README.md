# Lynq NTN-Pulse: constellation optimisation

Multi-objective search for the LEO constellation that best trades **10-year cost**, **latency (p99)** and
**coverage**. Altitudes can be mixed (up to 2 shells by default, `--max-shells 3`). ISL technology (RF or
optical), the number of crosslink terminals per satellite and the relay subset are decision variables. The full
formulation is in [PLAN.md](PLAN.md).

The folder is self-contained. `globalnet/` is a copy of `../05-global-coverage/globalnet` (orbits, global grid,
gateways, Dijkstra over the mesh), extended for RF/optical links, brick / +Grid / relay-subset layouts, polar
laser shutoff, inter-shell links, optical acquisition and failed satellites. Its defaults reproduce the 05 results.

| File | What it does |
|---|---|
| `globalnet/` | Coverage, ISL mesh and latency model |
| `costmodel.py` | Satellite mass and bus, Δv and propellant, lifetime by altitude, launch, per-plane OTVs, ops: 10-year TCO |
| `problem.py` | Decision variables ↔ design, repair, analytic pruning, objectives and constraint |
| `solve.py` | NSGA-II → local search per service tier → full-fidelity confirmation → robustness |
| `report.py` | `results/report.md`: answer, tier table, Pareto front, RF vs optical, mixed altitude, cost sensitivity |
| `sweep.slurm` | MeluXina batch job |

## Run locally

```bash
cd 07-constellation-optimization
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/python -m pytest -q                  # 21 tests
.venv/bin/python solve.py                      # ~1 h on 8 cores
.venv/bin/python solve.py --pop 48 --gens 20   # quicker
.venv/bin/python solve.py --stage report       # rebuild the report from saved CSVs
```

## Run on MeluXina

You need a MeluXina user account with an SSH key registered, and your project ID (`p200XXX`).

**1. Log in and get the code** (login node, port 8822):

```bash
ssh -p 8822 <user>@login.lxp.lu
cd $HOME        # or your project folder: /project/home/p200XXX
git clone https://github.com/gambhirsharma/Lynq && cd Lynq/07-constellation-optimization
```

**2. Build the venv on a compute node.** Modules only exist on compute nodes, and the venv must use the same
Python module the job loads:

```bash
salloc -A p200XXX -p gpu -q dev -N 1 -t 00:30:00     # short interactive allocation
srun --pty bash -l                                   # (only if salloc leaves you on the login node)
module load Python
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/python -m pytest -q                        # 21 tests should pass
exit                                                 # leave the node (twice if you used srun)
```

**3. Set your project ID and submit:**

```bash
sed -i 's/p200XXX/p200123/' sweep.slurm              # your project ID
sbatch sweep.slurm --pop 128 --gens 60               # all 128 CPUs of a node: a bigger population costs ~no extra time
```

Any `solve.py` arguments go after `sweep.slurm`. The job uses the `gpu` partition because the project has GPU
node-hours only. With CPU hours, change `--partition=cpu`.

**4. Follow it:**

```bash
squeue --me                       # PD = waiting, R = running
tail -f optimize-<jobid>.log      # one line per generation, then the tier answers
sacct -j <jobid> --format=JobID,State,Elapsed,MaxRSS
scancel <jobid>                   # stop it
```

If the job hits its time limit, run the same `sbatch` command again. Every evaluation is cached in
`results/evals_*.csv`, so it carries on where it stopped.

**5. Get the results** (from your own machine):

```bash
scp -P 8822 "<user>@login.lxp.lu:~/Lynq/07-constellation-optimization/results/*" ./results/
```

`results/report.md` has the answer. Also in `results/`: `tiers.csv`, `front.csv`, `robustness.csv` and the
raw `evals_*.csv`.

Troubleshooting: `module load Python` fails → `module avail Python` and put the exact name in `PYTHON_MODULE` in
`sweep.slurm` (and rebuild the venv with it). `pip install` cannot reach PyPI from the compute node → build the
venv on the login node with `python3 -m venv` instead, using the same Python version. `dev` QOS is rejected → use
`-q default`.

## Limits

- Cost numbers are parametric, calibrated to the proposal's 90 satellites (~€0.75 M all-in each). Check the
  terminal, launch and per-plane prices in `costmodel.CostParams` and `globalnet/config.py:ISL_TECH`.
- Coverage and latency only: no traffic or capacity, so optical's throughput advantage is not valued.
- Circular orbits, no J2. The 28 gateways are fixed.
