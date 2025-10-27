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

  script_name = "run-steer_%d.sh" % (jobstep)
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
#SBATCH --requeue
#SBATCH -A alviny6_lab_gpu   # Account to charge
#SBATCH --nodes=1        # Total # of nodes
#SBATCH --ntasks=1       # Total # of mpi tasks
#    #SBATCH --cpus-per-task=16   # cores per task
#SBATCH --gres=gpu:A30    # Specify 4 A30 GPUs
#SBATCH -t 24:00:00       # Run time (hh:mm:ss)
#SBATCH --constraint="intel,avx512,fastscratch,nvme"

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
""" % (jobstep, jobstep, cv1, prev_cv1, cv2, prev_cv2, basename))

  output.write("export rstname=$basedir'/'%s'-'%s'/'%s'-'%s'.restart'\n" % (prev_cv1, prev_cv2, prev_cv1, prev_cv2))

  output.write("""export rundir=$basedir'/'%s'-'%s
export output=$rundir'/'%s'-'%s

export firstjob='%s'
export steer='yes'

export langPistPeriod='200'
export langPistDecay='100'
export rstFreq='10000'

# Set up directories
mkdir -p $rundir

# Store the output trajectory file names
echo $PWD'/'$output'.dcd' >> $basedir'/run.stk'

# Run NAMD
namd3 equil.conf > 'log/'$basename'_%05d.log'
""" % (cv1, cv2, cv1, cv2, first_run, jobstep))
  output.close()
  os.system('chmod +x %s' % script_name)
  return script_name

def submit(fname, params=''):
  """ Submits the LSF job with fname, and returns the jobID """
  
  out = os.popen('sbatch %s < %s' % (params, fname) ).read()
  m = re.search('Submitted batch job (\d+)', out)
  return m.group(1) 

#--------------#
# Main Routine #
#--------------#

# let's make a library of colvar points
nsteps = 19;
# dihedral H6-H4-H4b-H8: immature (30) to mature (100)
theta = np.linspace(190,10,nsteps); 
#psi = np.linspace(90,-45,nsteps);
theta[theta < -180] += 360;
#psi[psi < -180] += 360;
dist = np.linspace(40.2,49.8,nsteps);
# angle H7-H8+9-H10
#ang = np.append(np.linspace(150,125,nsteps-5),125*np.ones(5));

for i in range(nsteps): 
  now = (theta[i],dist[i])
  if i==0:
    prev=now
  else:
    prev=(theta[i-1],dist[i-1])
    
  script = gen_sub(i, now, prev) 

  if i == 0:
    jobid = submit(script)
  else:
    jobid = submit(script, '--dependency=afterok:%s' % jobid)

