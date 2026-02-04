# Umbrella sampling guide

This folder contains a Python script that generates submit scripts for NAMD, and input and output files for this block of umbrella sampling simulations.

To run umbrella sampling, you need an input pdb and psf, and restart files from previous simulations for each desired window. You also need config files to set up the biasing on the order parameters.

The script `gen-submit.py` generates the config files and submit scripts. It also automatically submits the scripts using SLURM. To run it:

```python3 gen-submit.py```

Make sure that paths specified in the Python script are all correct.