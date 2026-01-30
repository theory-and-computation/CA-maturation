#!/bin/bash
#SBATCH --job-name=equil
#SBATCH --account=alviny6_lab_gpu
#SBATCH --partition=gpu
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --gres=gpu:1
#SBATCH --time=24:00:00

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
  sbatch --account=alviny6_lab_gpu --partition=gpu --nodes=1 --ntasks=1 --gres=gpu:1 --time=24:00:00 \
         --exclude="$new_excl" --job-name=equil --export=ALL,EXCLUDE="$new_excl",RETRIES="$((RETRIES+1))" "$0"
  exit 0
fi
echo "running equilibration steps"

$AMBER_EXEC -O -i min.in     -o min.out     -p complex-solvated.prmtop -c complex-solvated.inpcrd -r min.rst     -ref complex-solvated.inpcrd
$AMBER_EXEC -O -i heat.in    -o heat.out    -p complex-solvated.prmtop -c min.rst                  -r heat.rst    -x heat.nc    -ref min.rst
$AMBER_EXEC -O -i density.in -o density.out -p complex-solvated.prmtop -c heat.rst                 -r density.rst -x density.nc -ref heat.rst
$AMBER_EXEC -O -i equil.in   -o equil.out   -p complex-solvated.prmtop -c density.rst              -r equil.rst   -x equil.nc

