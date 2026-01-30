#!/bin/bash
#SBATCH --job-name=mmpbsa-para
#SBATCH -A alviny6_lab
#SBATCH -p standard
#SBATCH --nodes=1
#SBATCH --ntasks=4          
#SBATCH -t 72:00:00

module load amber          # Load AmberTools if installed as a module
module load openmpi        # Ensure MPI is available

cd $SLURM_SUBMIT_DIR || exit

start_time=$(date +%s)

# Run MMPBSA in parallel using 4 tasks
mpirun -np 4 MMPBSA.py.MPI -O -i mmpbsa.in -o FINAL_RESULTS_MMPBSA.dat \
    -do FINAL_DECOMP_MMPBSA.dat  \
    -sp construct123-solvated.prmtop -cp construct123.prmtop \
    -rp construct12.prmtop -lp construct3.prmtop \
    -y *.mdcrd > progress.log 2>&1

# Capture the end time
end_time=$(date +%s)

# Compute and print elapsed time
elapsed=$((end_time - start_time))
echo "Elapsed time: $elapsed seconds" >> progress.log

