#!/bin/bash

lows = ls run-steer_1[2-9].sh

jobid = sbatch run-steer_11.sh
for l in $lows
do
   jobid = sbatch $l -d afterok:$jobid
done
