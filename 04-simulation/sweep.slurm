#!/bin/bash -l
# Slurm job for the constellation sweep on MeluXina (docs.lxp.lu). From 04-simulation:  sbatch sweep.slurm
# Re-submitting after a timeout resumes: rows already in results/sweep.csv are skipped.
#SBATCH --job-name=lynq-sweep
#SBATCH --account=p200XXX           # your MeluXina project ID (required)
#SBATCH --partition=cpu
#SBATCH --qos=default               # up to 48 h; `short` (6 h) may start sooner
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=128         # one worker per physical core of a cpu node
#SBATCH --time=01:00:00             # default grid needs ~5 min; raise for the stress matrix
#SBATCH --output=sweep-%j.log

# Same Python module used to build .venv; modules exist only on compute nodes, so it is loaded here.
PYTHON_MODULE="Python"

set -eo pipefail
module load "$PYTHON_MODULE"
cd "$SLURM_SUBMIT_DIR"
.venv/bin/python sweep.py --workers "$SLURM_CPUS_PER_TASK" "$@"
