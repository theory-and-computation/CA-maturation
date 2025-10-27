#!/usr/bin/python

import os 
import re

os.system('ls -1 1-timeseries/*.dat > timeseries_files')

files  = open('timeseries_files', 'r').readlines()
output = open('wham-cc.inp', 'w')

output.write("""\
bia-1.dat
rho-1.dat
pmf-1.dat\n""")

# Write the minimum and maximum values:
ndims = 2
var_range = [(-36.2, 118.8, 2.5), 
             (37.3, 51.3, 0.5)]

xminfile = open('2-windowparams/xmin-cc.dat', 'w')
xmaxfile = open('2-windowparams/xmax-cc.dat', 'w')
dxfile   = open('2-windowparams/dx-cc.dat', 'w')

for i in range (ndims):
  xminfile.write("%.1f\n" % var_range[i][0])
  xmaxfile.write("%.1f\n" % var_range[i][1])
  dxfile.write("%.1f\n" % var_range[i][2])

output.write("""\
%s
2-windowparams/xmin-cc.dat
2-windowparams/xmax-cc.dat
2-windowparams/dx-cc.dat
0.0 -999999.0 -999999.0
0.000001  10000
%s\n""" % (ndims, len(files)))

# Write the file names, window potential, and length of files
for line in files:

    line  = line.strip()
    basename = os.path.basename(line)
    match = re.match('(-?[0-9]+.0)-([0-9]+.[0-9]).dat', basename)

    xi1_ref = float(match.group(1))
    xi2_ref = float(match.group(2))
    xi1_force = 0.2
    xi2_force = 12.0

    window_fname = './2-windowparams/%.1f-%.1f.k' % (xi1_ref, xi2_ref)
    window_file = open(window_fname, 'w')
    window_file.write('%.1f  %.2f\n' % (xi1_ref, xi1_force))
    window_file.write('%.1f  %.2f\n' % (xi2_ref, xi2_force))

    nsteps = len(open(line).readlines()) 
    
    output.write('./%s\n' %line)
    output.write('%s\n' % window_fname)
    output.write('%s\n' % nsteps)

output.close()
