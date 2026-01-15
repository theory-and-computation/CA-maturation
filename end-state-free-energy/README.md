
Analysis of the Minimum Free Energy Pathway Workflow

# Step 1: Setup
# Minimum Free Energy Pathway (MFEP) Workflow

This repository contains a workflow for preparing, running, and analyzing molecular dynamics simulations to obtain the Minimum Free Energy Pathway (MFEP) using Amber.

---

## Requirements

- Conda
- AmberTools23  
  Installation instructions: https://ambermd.org/AmberTools.php
- Amber MD engine:
  - `pmemd.cuda` (GPU), or
  - `pmemd` (CPU), or
  - `sander` (CPU)
- Bash shell (Linux/macOS)

The following executables must be available in your `$PATH`:
- `tleap`
- `pmemd.cuda` or `pmemd` or `sander`

---

## Environment Setup

All steps were run using an AmberTools23 Conda environment.

Activate the environment before running the workflow:

```bash
conda activate AmberTools23

# Step 2: Prepare unbiased MD simulations with tleap for Amber 
./pre-automate.sh

# Step 3: Submit equilibration and production runs
./pmemd-submit.sh

# Step 4: Analysis of minimum free energy pathway states
./post-automate.sh
