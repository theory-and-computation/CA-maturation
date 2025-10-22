#!/bin/bash
#SBATCH --job-name=run
#SBATCH --account=alviny6_lab_gpu
#SBATCH --partition=gpu
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --gres=gpu:1
#SBATCH --time=36:00:00

set -euo pipefail

module load amber
module load cuda

AMBER_EXEC="pmemd.cuda"
RETRIES=${RETRIES:-0}
MAX_RETRIES=8

if nvidia-smi -q -d ECC | grep -q "Uncorrectable.*: *[1-9]"; then
  badnode="${SLURMD_NODENAME:-$(hostname -s)}"
  new_excl="${EXCLUDE:+$EXCLUDE,}$badnode"
  if [ "$RETRIES" -ge "$MAX_RETRIES" ]; then echo "Max retries reached"; exit 1; fi
  sbatch --account=alviny6_lab_gpu --partition=gpu --nodes=1 --ntasks=1 --gres=gpu:1 --time=36:00:00 \
         --exclude="$new_excl" --job-name=run --export=ALL,EXCLUDE="$new_excl",RETRIES="$((RETRIES+1))" "$0"
  exit 0
fi

echo "running production runs"

$AMBER_EXEC -O -i prod.in -o prod1.out -p complex-solvated.prmtop -c equil.rst -r prod1.rst -x prod1.nc

