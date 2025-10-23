#!/usr/bin/python

import os 
import re

os.system('ls -1 1-timeseries/*.dat > timeseries_files')

files  = open('timeseries_files', 'r').readlines()
output = open('wham-f.inp', 'w')

output.write("""\
pore_2d_bia.dat
pore_2d_rho.dat
pore_2d_pmf.dat
8.0 27.0 0.5   8.0 27.0 0.5
0.0 -9999.0 -9999.0
0.000001  10000
%s\n""" % `len(files)`)

for line in files:

    line  = line.strip()
    basename = os.path.basename(line)

    match = re.match('a2_(\d+)-(\d+).dat', basename)
    ac_ref = int(match.group(1))
    bd_ref = int(match.group(2))

    ac_force = 2.0
    bd_force = 2.0

    output.write('%s\n' % line)   
    output.write(' %.1f %.2f  %.1f %.2f\n' % (ac_ref, ac_force, bd_ref, bd_force))

output.close()
