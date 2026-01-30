<<<<<<< HEAD
### Overview
=======
# HIV-1 Capsid Shape Changes
>>>>>>> bfae858 (updated readme)

Simulations and analysis tools for studying how the HIV-1 capsid protein changes shape during virus maturation.

## Overview

<<<<<<< HEAD
Contents
Simulation setup: Input structures, force-field parameters, and umbrella sampling definitions
Sampling workflow: Window generation, restraint definitions, and production protocols
Free-energy reconstruction: WHAM/string-based analysis used to recover the MFEP

Intermediate analysis: End-state free-energy calculations and structural characterization
Post-processing scripts: Tools for reproducing figures and numerical results
=======
This repository contains computational workflows to study the transition pathway between two key shapes of the HIV-1 capsid (CA) protein: immature-like and mature-like states. 

**What we do:**
- **Umbrella sampling** - Systematically sample different protein shapes
- **String method** - Find the lowest energy pathway between shapes
- **Energy calculations** - Measure the energy of intermediate shapes along the pathway

## Repository Structure

```
.
├── umbrella-sampling/          # Simulations of protein shape transitions
│   ├── input/                  # Starting structures and parameters
│   ├── windows/                # Individual simulation windows
│   ├── production/             # Main simulation runs
│   └── analysis/               # Data analysis tools
│
├── end-state-free-energy/      # Energy calculations
│   ├── intermediates/          # Intermediate protein shapes
│   ├── calculations/           # Energy calculation setup
│   └── results/                # Analysis results
│
└── scripts/                    # Tools for processing and visualization
    ├── figures/                # Figure generation scripts
    └── analysis/               # Data processing utilities
```

## Methodology

### 1. Umbrella Sampling Setup

We explore the protein shape changes using umbrella sampling. This technique uses constraints to sample different conformations between the starting (immature) and ending (mature) states.

### 2. Finding the Energy Pathway

We find the most likely transition pathway using:
- **WHAM** - Combines data from all simulations to estimate energy differences
- **String method** - Refines the pathway to find the lowest energy route
- **"Free energy calculations** - Reveals key residue interactions

### 3. Analyzing Intermediate Shapes

We analyze the protein shapes along the pathway to:
- Characterize structural features
- Calculate energy differences between structures

## Key Features

- Automated scripts for setting up simulations
- Analysis and scripts for figure recreation
>>>>>>> bfae858 (updated readme)
