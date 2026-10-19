#!/bin/bash
# Slurm job for the constellation sweep. From 04-simulation:  sbatch sweep.slurm
# Re-submitting after a timeout resumes: rows already in results/sweep.csv are skipped.
#SBATCH --job-name=lynq-sweep
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=64          # cores on one node; lower it if the node has fewer
#SBATCH --time=02:00:00
#SBATCH --output=sweep-%j.log
##SBATCH --partition=batch         # uncomment and set if your cluster needs a partition

# Python 3.10+ module used to build .venv (`module avail python`); empty if using miniforge/system Python.
PYTHON_MODULE="lang/Python/3.11.5-GCCcore-13.2.0"

set -eo pipefail
[ -n "$PYTHON_MODULE" ] && module load "$PYTHON_MODULE"
cd "$SLURM_SUBMIT_DIR"
.venv/bin/python sweep.py --workers "$SLURM_CPUS_PER_TASK" "$@"
