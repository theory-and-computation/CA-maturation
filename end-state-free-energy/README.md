
Analysis of the Minimum Free Energy Pathway Workflow

# Step 1: Setup
conda activate AmberTools23

# Step 2: Prepare unbiased MD simulations with tleap for Amber 
./pre-automate.sh

# Step 3: Submit equilibration and production runs
./pmemd-submit.sh

# Step 4: Analysis of minimum free energy pathway states
./post-automate.sh
