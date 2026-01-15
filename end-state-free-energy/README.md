
Analysis of the Minimum Free Energy Pathway

# Minimum Free Energy Pathway (MFEP) Workflow

This repository contains a workflow for preparing, running, and analyzing molecular dynamics simulations to HIV-1 capsid maturation. 

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

# Prepare unbiased MD simulations with tleap for Amber 
./pre-automate.sh

# Submit equilibration and production runs
./pmemd-submit.sh

# Analysis of minimum free energy pathway states
./post-automate.sh
