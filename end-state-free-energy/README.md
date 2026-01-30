
Analysis of the Minimum Free Energy Pathway

# Minimum Free Energy Pathway (MFEP) Workflow

<<<<<<< HEAD
This repository contains a workflow for preparing, running, and analyzing molecular dynamics simulations to HIV-1 capsid maturation. 
=======
This repository contains a workflow for preparing, running, and analyzing molecular dynamics simulations monomeric maturation in AMBER.
>>>>>>> 592b5f7 (update and overwrite)

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

<<<<<<< HEAD
The following executables must be available in your `$PATH`:
=======
The following executables must be available:
>>>>>>> 592b5f7 (update and overwrite)
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
