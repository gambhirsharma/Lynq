#!/bin/bash -l
# Slurm job for the constellation optimisation on MeluXina (docs.lxp.lu). From 07-constellation-optimization:  sbatch sweep.slurm (uses ../05-global-coverage/.venv)
# Re-submitting after a timeout resumes: evaluations cached in results/evals_*.csv are reused.
#SBATCH --job-name=lynq-optimize
#SBATCH --account=p200XXX           # your MeluXina project ID (required)
#SBATCH --partition=gpu             # CPU-only code, but our project has GPU node-hours only
#SBATCH --qos=default               # up to 48 h; `short` (6 h) may start sooner
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=128         # all CPUs of a gpu node
#SBATCH --time=02:00:00             # default run needs ~15 min on 128 cores
#SBATCH --output=sweep-%j.log

# Same Python module used to build .venv; modules exist only on compute nodes, so it is loaded here.
PYTHON_MODULE="Python"

set -eo pipefail
module load "$PYTHON_MODULE"
cd "$SLURM_SUBMIT_DIR"
../05-global-coverage/.venv/bin/python solve.py --workers "$SLURM_CPUS_PER_TASK" "$@"
