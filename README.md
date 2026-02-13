# HIV-1 Capsid Protein Maturation

Simulations and analysis tools for studying how the HIV-1 capsid protein changes conformation during virus maturation.

## Overview

This repository contains computational workflows to study the transition pathway between the HIV-1 capsid (CA) protein immature-like and mature-like states. It includes two main approaches:

1. **Steered MD and Umbrella Sampling** — Biased simulations across the conformational landscape of CA protein using NAMD.
2. **Minimum Free Energy Pathway Analysis** — Unbiased molecular dynamics simulations of monomeric maturation using AMBER.

---

## Requirements

### Umbrella Sampling Workflow (NAMD)

- NAMD 3.0
- Python 3
- Bash shell (Linux/macOS)

### MFEP Workflow (AMBER)

- Conda
- AmberTools23 — [Installation instructions](https://ambermd.org/AmberTools.php)
- Amber MD engine: `pmemd.cuda` (GPU), `pmemd` (CPU), or `sander` (CPU)
- Bash shell (Linux/macOS)

The following executables must be available: `tleap`, and one of `pmemd.cuda`, `pmemd`, or `sander`.

---

## Directory Guide

### Steered MD and Umbrella Sampling

| Directory | Description |
|---|---|
| `steer-1022/` | 1D steering from mature to immature. Includes scripts to run NAMD and input/output files. |
| `steer-2d-1111/` | 2D steering to collective variable windows. Includes scripts to run NAMD and input/output files. |
| `umb-112724/` | First 20 ns umbrella sampling. Includes scripts to run NAMD and final coordinate files. |
| `umb-122124/` | Next 20 ns umbrella sampling. Includes scripts to run NAMD. |
| `umb-010525/` | Next 20 ns umbrella sampling. Includes scripts to run NAMD. |
| `umb-012825/` | Final 20 ns umbrella sampling. Includes scripts to run NAMD. |

### WHAM Analysis

| Directory | Description |
|---|---|
| `wham-0512-last60/` | WHAM on last 60 ns of biased trajectories. |
| `wham-0126-blocks/` | WHAM on 10 ns blocks of trajectories. |

---

## Reproducing Figures

| Figure | Command |
|---|---|
| Figure 1A | `vmd -e immature_lattice.vmd` (from `scripts/`) |
| Figure 1B | `vmd -e mature_lattice.vmd` (from `scripts/`) |
| Figure 2A | `vmd -e colvars.vmd` (from `scripts/`) |
| Figure 2B | Run `pmf-MFEP.py` |
| Figure 2C | Run `rmsf.py` |
| Figures 3A–C | Run `pmf-MFEP.py` |
| Figure S1 | Run `plot_pmf_error.py` |

---

## Minimum Free Energy Pathway Workflow

### Environment Setup

```bash
conda activate AmberTools23

# Prepare unbiased MD simulations with tleap for Amber
./pre-automate.sh

# Submit equilibration and production runs
./pmemd-submit.sh

# Analysis of minimum free energy pathway states
./post-automate.sh
```
