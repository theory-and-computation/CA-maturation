# Umbrella sampling data guide

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
Figure 2B: run pmf-MFEP.ipynb
Figure 2C: run rmsf.ipynb

Figure 3A-C: run pmf-MFEP.ipynb

Figure S1: run plot_pmf_error.ipynb
