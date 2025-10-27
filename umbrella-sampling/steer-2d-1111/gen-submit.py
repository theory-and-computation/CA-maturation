#!/usr/bin/python

""" A simple script for submitting steered MD scripts """

import os,sys,re
import numpy as np

#----------------------#
# Function Definitions #
#----------------------#

def genColVarConfig(basename, params):
  template = open('colvarstemplate.in', 'r').read()
  output  = open('colvarsconfig/%s_%s_%s.cvc' % (basename, params[0], params[1]), 'w')
  output.write(template % params)

def gen_sub(jobstep, params, params_prev):
  """ Generates a SLURM submission script and returns the file name 
      -  Use only for jobn >= 1 """

  script_name = "run-steer_%d_%d_%.1f.sh" % (jobstep, params[0], params[1])
  output = open(script_name, 'w')  

  basename = 'CA-mature'
  # three colvars
  cv1 = '%04.1f' % params[0]
  cv2 = '%04.1f' % params[1]
  #cv3 = '%04.1f' % params[2]
  prev_cv1 = '%04.1f' % params_prev[0]
  prev_cv2 = '%04.1f' % params_prev[1]
  #prev_cv3 = '%04.1f' % params_prev[2]
  if jobstep == 0:
    first_run = 'yes'
  else:
    first_run = 'no'
  genColVarConfig(basename, (cv1,cv2))

  output.write(r"""#!/bin/bash

#SBATCH -p free-gpu       # Queue (partition) name
#SBATCH -A alviny6_lab_gpu   # Account to charge
#SBATCH --nodes=1        # Total # of nodes
#SBATCH --ntasks=1       # Total # of mpi tasks
#      #SBATCH --cpus-per-task=32   # cores per task
#SBATCH --gres=gpu:A30    # Specify 4 A30 GPUs
#SBATCH -t 24:00:00       # Run time (hh:mm:ss)
#SBATCH --constraint="intel,avx512,fastscratch,nvme"
#SBATCH --requeue # not sure if this will work

#SBATCH -J CA.mature_%s   # Job name
#SBATCH -o log/slurm_%s.out
export cv1='%s'
export prev_cv1='%s'
export cv2='%s'
export prev_cv2='%s'

export PATH=$PATH:/share/crsp/lab/alviny6/share/utilities/bin/

# Set environmental variables
export basename='%s'
export nsteps='50000'
export temp='310'

export basedir='output'
""" % (jobstep, cv1, cv1, prev_cv1, cv2, prev_cv2, basename))
  if (first_run == 'yes'):
    output.write("export rstname='../steer-1022/output_1024/'%s'-'%s'/'%s'-'%s'.restart'\n" % (prev_cv1, prev_cv2, prev_cv1, prev_cv2))
  else:
    output.write("export rstname=$basedir'/'%s'-'%s'/'%s'-'%s'.restart'\n" % (prev_cv1, prev_cv2, prev_cv1, prev_cv2))

  output.write("""export rundir=$basedir'/'%s'-'%s
export output=$rundir'/'%s'-'%s

export firstjob='no'
export steer='yes'

export langPistPeriod='200'
export langPistDecay='100'
export rstFreq='10000'

# Set up directories
mkdir -p $rundir

# Store the output trajectory file names
echo $PWD'/'$output'.dcd' >> $basedir'/run.stk'

# Run NAMD
namd3 equil.conf > 'log/'$basename'_%05d_%s_%s.log'
""" % (cv1, cv2, cv1, cv2, jobstep, cv1, cv2))
  output.close()
  os.system('chmod +x %s' % script_name)
  return script_name

def submit(fname, params=''):
  """ Submits the LSF job with fname, and returns the jobID """
  
  out = os.popen('sbatch %s < %s' % (params, fname) ).read()
  m = re.search('Submitted batch job (\d+)', out)
  return m.group(1)

def run_steer(theta_grid, dist, dist_old):
  for i in range(len(theta_grid)-1):
    now = (theta_grid[i+1],dist)
    prev=(theta_grid[i],dist)
    if i == 0:
      prev=(theta_grid[i],dist_old);

    script = gen_sub(i, now, prev)

    if i == 0:
      jobid = submit(script)
    else:
      jobid = submit(script, '--dependency=afterok:%s' % jobid)

#--------------#
# Main Routine #
#--------------#

theta_min = -30
theta_max = 110
dist_min = 40.2
dist_max = 49.8

dist_list = [];

for cvc in (os.listdir("../steer-1022/output_1024/")):
  if (cvc != "run.stk"):
    # get colvars from an old SMD simulation
    vals = cvc.split(".0-");
    theta = float(vals[0]);
    dist = float(vals[1]);
    
    if dist not in dist_list:
      dist_list += [dist];
      # grid on multiples of 5 angles
      inc_start = 5*np.ceil(theta / 5);
      dec_start = 5*np.floor(theta / 5);
      # run steered simulation in two directions
      # one with increasing angle, the other with decreasing
      theta_inc = np.arange(inc_start,theta_max+1,5);
      theta_dec = np.flipud(np.arange(theta_min, dec_start+1,5));

      theta_inc = np.append([theta], theta_inc);
      #theta_dec = np.append([theta], theta_dec);
  
      run_steer(theta_inc, dist, dist);
      run_steer(theta_dec, dist, dist);
