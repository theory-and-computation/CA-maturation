#!/usr/bin/python

""" A simple script for submitting steered MD scripts """

import os,sys,re

#----------------------#
# Function Definitions #
#----------------------#

def genColVarConfig(cv1, cv2):
  template = open('colvarstemplate.in', 'r').read()
  output  = open('colvarsconfig/%s_%s.cvc' % (cv1, cv2), 'w')
  output.write(template % (cv1, cv2))

def genVarConfig(cv1, cv2, jobstep):
  """ Generates user-defined variables for NAMD """

  prev_jobstep = jobstep - 1
  jobstep = '%05d' % jobstep
  prev_jobstep = '%05d' % prev_jobstep  

  basename='CA-mature'
  nsteps=10000000
  outputname='output/%s-%s/%s-%s' %(cv1, cv2, cv1, cv2)
  rstname='../steer-2d-1111/output/%s-%s/%s-%s.restart' % (cv1, cv2, cv1, cv2) 
  firstjob='no'
  temperature=310

  langPistPeriod=200
  langPistDecay=100
  rstFreq=10000

  output = open('varsconfig/%s_%s.var' % (cv1, cv2), 'w')
  output.write(r"""
##########################
# NAMD Runtime Variables #
##########################

set cv1         %s
set cv2         %s

set basename    %s
set nsteps      %s
set outputname  %s
set rstname     %s
set firstjob    %s
set temperature %s

set lPP         %s
set lPD         %s
set rstFreq     %s

""" %(cv1, cv2, basename, nsteps, outputname, rstname, 
      firstjob, temperature,
      langPistPeriod, langPistDecay, rstFreq))

  os.system('mkdir -p output/%s-%s' % (cv1, cv2))

def gen_sub(cv1, cv2, jobstep):
  """ Generates a SLURM submission script and returns the file name 
      -  Use only for jobstep >= 1 """

  cv1 = "%04.1f" % cv1
  cv2 = "%04.1f" % cv2
  job_id = '%s_%s_%05d' % (cv1, cv2, jobstep)
  script_name = "run-umb_%s.sh" % job_id
  nodes = 1;
  output = open(script_name, 'w')  
  output.write(r"""#!/bin/bash

#SBATCH -p free-gpu       # Queue (partition) name
#SBATCH -A alviny6_lab_gpu   # Account to charge
#SBATCH --nodes=%d        # Total # of nodes
#SBATCH --ntasks=1       # Total # of mpi tasks
#SBATCH --cpus-per-task=%d   # cores per task
#SBATCH --gres=gpu:A30:4    # Specify 4 A30 GPUs
#SBATCH -t 6:00:00       # Run time (hh:mm:ss)
#SBATCH --constraint="intel,avx512,fastscratch,nvme"

#SBATCH -J %s_%s   # Job name
#SBATCH -o log/slurm_%s_%s.out

export PATH=$PATH:/share/crsp/lab/alviny6/share/utilities/bin/
# module load namd/2.14b2/gcc.8.4.0
# Run NAMD
""" % (nodes, 32*nodes, cv1, cv2, cv1, cv2))

  genColVarConfig(cv1, cv2)
  genVarConfig(cv1, cv2, jobstep)

  output.write(r"""namd3 +p29 +pmepes 5 +setcpuaffinity +devices 0,1,2,3 --source varsconfig/%s_%s.var umbrella.conf > log/%s_%s.log &
""" % (cv1, cv2, cv1, cv2))

  output.write(r"""wait""")
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

for jobstep, state in enumerate(os.listdir("../steer-2d-1111/output")):
  if (state != "run.stk"):
    theta = float(state.split(".0-")[0]);
    dist = float(state.split(".0-")[1]);
    if (jobstep >= 500 and jobstep < 600):
      script = gen_sub(theta, dist, jobstep)
      jobid = submit(script)  

#gen_sub(38, 40, jobstep)


