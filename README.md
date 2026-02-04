# HIV-1 Capsid Protein Maturation

Simulations and analysis tools for studying how the HIV-1 capsid protein changes conformation during virus maturation.

## Overview

This repository contains computational workflows to study the transition pathway between the HIV-1 capsid (CA) protein: immature-like and mature-like states. 




# Steered MD and Umbrella Sampling

This repository contains a workflow for preparing and running umbrella sampling simulations across the conformational landscape of CA protein.

Find it in the `umbrella-sampling/` folder.

---

## Requirements

- NAMD 3.0
- Python 3
- Bash shell (Linux/macOS)

## Directory guide

steer-1022/: 1D steering from mature to immature. Includes scripts to run NAMD and input and output files.

steer-2d-1111/: 2D steering to collective variable windows. Includes scripts to run NAMD and input and output files.

umb-112724/: first 20 ns umbrella sampling. Includes scripts to run NAMD and final coordinate files.

umb-122124/: next 20 ns umbrella sampling. Includes scripts to run NAMD.

umb-010525/: next 20 ns umbrella sampling. Includes scripts to run NAMD.

umb-012825/: final 20 ns umbrella sampling. Includes scripts to run NAMD.

# WHAM data guide

wham-0512-last60/: WHAM on last 60 ns of biased trajectories

wham-0126-blocks/: WHAM on 10ns blocks of trajectories

Figure 1A: run on the command line "vmd -e immature_lattice.vmd" from scripts/

Figure 1B: run on the command line "vmd -e mature_lattice.vmd" from scripts/

Figure 2A: run on the command line "vmd -e colvars.vmd" from scripts/

Figure 2B: run pmf-MFEP.py

Figure 2C: run rmsf.py

Figure 3A-C: run pmf-MFEP.py

Figure S1: run plot_pmf_error.py




# Minimum Free Energy Pathway Analysis

This repository contains a workflow for preparing, running, and analyzing molecular dynamics simulations monomeric maturation in AMBER.

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




The following executables must be available:
- `tleap`
- `pmemd.cuda` or `pmemd` or `sander`

---

## Environment Setup

All steps were run using an AmberTools23 Conda environment.

Activate the environment before running the workflow:

### Structure directories should be moved out of structure/ into the same directory as run script

```bash
conda activate AmberTools23

# Prepare unbiased MD simulations with tleap for Amber
./pre-automate.sh

# Submit equilibration and production runs
./pmemd-submit.sh

# Analysis of minimum free energy pathway states
./post-automate.sh
~                        
