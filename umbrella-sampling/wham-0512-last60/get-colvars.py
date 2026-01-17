#!/usr/bin/python

import sys
import os
import glob
import re

# open NAMD output files across different runs
# with given CV coordinates
# and copy data to 1-timeseries/ in one file
def write_timeseries (jobstep, xi1, xi2, output):
  global last_ts
  
  colvar_dir   = "../umb-122124/output/%s-%s" % (xi1, xi2) 
  basename     = "%s-%s" % (xi1, xi2)
  colvar_fname = '%s/%s.colvars.traj' % (colvar_dir, basename)

  infile = open(colvar_fname, 'r').readlines()

  colvar_dir2   = "../umb-010525/output/%s-%s" % (xi1, xi2)
  colvar_fname2 = '%s/%s.colvars.traj' % (colvar_dir2, basename)

  infile2 = open(colvar_fname2, 'r').readlines()

  colvar_dir3   = "../umb-012825/output/%s-%s" % (xi1, xi2)
  colvar_fname3 = '%s/%s.colvars.traj' % (colvar_dir3, basename)

  infile3 = open(colvar_fname3, 'r').readlines()
  # Skip the header and first line 
  #if jobstep > 0: 
  infile = infile[1:]
        
  for line in infile:
    line = line.split()
    if line[0] != '#':                       # Skip the comments
      timestep = int(line[0])
      ac = float(line[1])
      bd = float(line[2])
      output.write('%8d     %.5f       %.5f\n' % (timestep, bd, ac))

  last_ts = timestep

  infile2 = infile2[1:]
  for line in infile2:
    line = line.split()
    if line[0] != '#':                       # Skip the comments
      timestep = int(line[0])+last_ts
      ac = float(line[1])
      bd = float(line[2])
      output.write('%8d     %.5f       %.5f\n' % (timestep, bd, ac))

  last_ts = timestep

  infile3 = infile3[1:]
  for line in infile3:
    line = line.split()
    if line[0] != '#':                       # Skip the comments
      timestep = int(line[0])+last_ts
      ac = float(line[1])
      bd = float(line[2])
      output.write('%8d     %.5f       %.5f\n' % (timestep, bd, ac))

  last_ts = timestep

#------#
# Main #
#------#

# get list of all CV pairs
colvars_list = sorted(glob.glob('../umb-012825/output/*/*.colvars.traj'))

# collect data from all CV pairs
for line in colvars_list:

  # get CV values as strings from path name
  fname = os.path.basename(line)
  match = re.match('(-?[0-9]+.0)-([0-9]+.[0-9]).colvars.traj', fname) 
  xi1 = match.group(1)
  xi2 = match.group(2)

  basename = '%s-%s' % (xi1, xi2)
  output = open('1-timeseries/' + basename + '.dat', 'w')
    
  write_timeseries(1, xi1, xi2, output)

