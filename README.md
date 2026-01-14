Overview

This repository contains workflows and analysis scripts for characterizing conformational transitions of the HIV-1 capsid (CA) protein using molecular simulation and free-energy methods.

The study employs umbrella sampling to construct a minimum free energy pathway (MFEP) connecting structurally defined immature-like and mature-like CA conformations. String method was used to obtain the underlying free-energy [athway along the chosen reaction coordinates. Discrete states along the MFEP are subsequently analyzed using end-state free-energy calculations to quantify energetic contributions and to characterize intermediate conformations encountered along the transition.

Contents
Simulation setup: Input structures, force-field parameters, and umbrella sampling definitions
Sampling workflow: Window generation, restraint definitions, and production protocols
Free-energy reconstruction: WHAM/string-based analysis used to recover the MFEP
Intermediate analysis: End-state free-energy calculations and structural characterization
Post-processing scripts: Tools for reproducing figures and numerical results
