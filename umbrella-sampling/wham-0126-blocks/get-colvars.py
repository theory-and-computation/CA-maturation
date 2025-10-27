#!/usr/bin/python

import sys
import os
import glob
import re

def write_timeseries (jobstep, xi1, xi2, output):
  global last_ts
  
  colvar_dir   = "../umb-012825/output/%s-%s" % (xi1, xi2) 
  basename     = "%s-%s" % (xi1, xi2)
  colvar_fname = '%s/%s.colvars.traj' % (colvar_dir, basename)
  
  infile = open(colvar_fname, 'r').readlines()

  # Skip the header and first line 
  #if jobstep > 0: 
  infile = infile[1:]
        
  for line in infile:
    line = line.split()
    if line[0] != '#':                       # Skip the comments
      timestep = int(line[0])
      ac = float(line[1])
      bd = float(line[2])
      if (timestep >= 0 and timestep < 5000000):
        output.write('%8d     %.5f       %.5f\n' % (timestep, bd, ac))
        
  last_ts = timestep

#------#
# Main #
#------#

colvars_list = sorted(glob.glob('../umb-010525/output/*/*.colvars.traj'))
endjobstep = 2

for line in colvars_list:
 
  fname = os.path.dirname(line)
  match = re.match('../umb-010525/output/(-?[0-9]+.0)-([0-9]+.[0-9])', fname) 
  xi1 = match.group(1)
  xi2 = match.group(2)

  basename = '%s-%s' % (xi1, xi2)
  output = open('1-timeseries/' + basename + '.dat', 'w')
  last_ts = 0

  for jobstep in range(1, endjobstep):
    write_timeseries(jobstep, xi1, xi2, output)

