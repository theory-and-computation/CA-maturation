# HIV-1 Capsid Shape Changes

Simulations and analysis tools for studying how the HIV-1 capsid protein changes shape during virus maturation.

## Overview

This repository contains computational workflows to study the transition pathway between the HIV-1 capsid (CA) protein: immature-like and mature-like states. 

**What we do:**
- **Umbrella sampling** - Systematically sample different protein shapes
- **String method** - Find the lowest energy pathway between shapes
- **Energy calculations** - Measure the energy of intermediate structures along the pathway and reveals key structural interactions


## Methodology

### 1. Umbrella Sampling Setup

We explore the protein shape changes using umbrella sampling. This technique uses constraints to sample different structures between the starting (immature) and ending (mature) states.

### 2. Finding the Energy Pathway

We find the most likely transition pathway using:
- **WHAM** - Combines data from all simulations to estimate energy differences
- **String method** - Refines the pathway to find the lowest energy route
- **Free energy calculations** - Reveals key structural interactions

### 3. Analyzing Intermediate Shapes

We analyze the protein shapes along the pathway to:
- Characterize structural features
- Calculate energy differences between structures
- Identify which interactions are most important

## Includes

- Simulation input files
- Automated scripts for setting up simulations
- Scripts to reproduce all figures
