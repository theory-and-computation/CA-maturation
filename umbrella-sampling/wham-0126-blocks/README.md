# WHAM instructions

This folder contains all output files from running weighted histogram analysis. To run it yourself, you will need .colvars.traj files reporting the two order parameters from biased simulations. These are not included in the repository, but you can generate them by running the umbrella sampling scripts yourself.

Once you have the .colvars.traj files, you can run WHAM.

1. Process .colvars.traj files

Run the script `get-colvars.py`:

```python3 get-colvars.py```

This adds a .dat file for each umbrella sampling window containing all samples in order parameter space in that window to the 1-timeseries/ folder. This step can take a few minutes, depending on how long your runs are.

2. Set up config files

Run the script `gen-wham-cc-inp.py`:

```python3 gen-wham-cc-inp.py```

This generates config files for each US window in the 2-windowparams/ folder, and another config file called wham-cc.inp in the current folder. Edit the Python script to change the WHAM parameters.

3. Run WHAM

Run the WHAM executable:

```./wham > wham-cc.out```

It will automatically detect the config files. The output files are pmf.dat, rho.dat, and bia.dat. We use pmf.dat for later analysis. wham-cc.out is a log file containing info about the 2D histogram and how quickly WHAM converges.