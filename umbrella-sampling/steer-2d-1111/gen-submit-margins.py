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

export cv1='%s'
export prev_cv1='%s'
export cv2='%s'
export prev_cv2='%s'

export PATH=$PATH:~/Desktop/tools/NAMD_3.0_Linux-x86_64-multicore-CUDA/

# Set environmental variables
export basename='%s'
export nsteps='50000'
export temp='310'

export basedir='output'
""" % (cv1, prev_cv1, cv2, prev_cv2, basename))
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

# given list of 
def run_steer(theta_grid, dist, dist_old):
  scripts = [];
  for i in range(len(theta_grid)-1):
    now = (theta_grid[i+1],dist)
    prev=(theta_grid[i],dist)
    if i == 0:
      prev=(theta_grid[i],dist_old);

    script = gen_sub(i, now, prev)
    scripts += ["bash " + script];
  submit = " && ".join(scripts);
  os.popen(submit)
#SBATCH -o log/slurm_%s.out

#--------------#
# Main Routine #
#--------------#

theta_min = -30
theta_max = 110
dist_min = 38.1
dist_max = 49.8

for cvc in (os.listdir("output")):
  scripts = [];
  if (cvc != "run.stk"):
    # get colvars from an old SMD simulation
    vals = cvc.split(".0-");
    theta = float(vals[0]);
    dist = float(vals[1]);

    if (dist==49.8):
      now = (theta,50.5);
      later = (theta,51.2);
      prev = (theta,49.8);
      scripts += ["bash " + gen_sub(100,now,prev), \
                  "bash " + gen_sub(101,later,now)];
    if (dist==40.2):
      now = (theta,39.5);
      later = (theta,38.8);
      even_later = (theta,38.1);
      prev = (theta,dist);
      scripts += ["bash " + gen_sub(200,now,prev), \
                  "bash " + gen_sub(201,later,now), \
                  "bash " + gen_sub(202,even_later,later)];
    #if (theta == -30):
    #  now = (-35,dist);
    #  prev = (-30,dist);
    #  scripts += ["bash " + gen_sub(999, now, prev)];
    # grid on multiples of 5 angles
    #inc_start = 5*np.ceil(theta / 5);
    #dec_start = 5*np.floor(theta / 5);
    # run steered simulation in two directions
    # one with increasing angle, the other with decreasing
    #theta_inc = np.arange(inc_start,theta_max+1,5);
    #theta_dec = np.flipud(np.arange(theta_min, dec_start+1,5));

    #theta_inc = np.append([theta], theta_inc);
    #theta_dec = np.append([theta], theta_dec);
  
    #run_steer(theta_inc, 50.5, 49.8);
    #run_steer(theta_dec, 50.5, 49.8);
  submit = " && ".join(scripts);
  #os.popen(submit)
  print(submit)
