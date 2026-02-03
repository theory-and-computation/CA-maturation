# HIV-1 Capsid Protein Maturation

Simulations and analysis tools for studying how the HIV-1 capsid protein changes conformation during virus maturation.

## Overview

This repository contains computational workflows to study the transition pathway between the HIV-1 capsid (CA) protein: immature-like and mature-like states. 








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
