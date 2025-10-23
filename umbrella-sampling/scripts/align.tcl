# CC: functions to align immature pdb to mature pdb
#     by NTD and calculate RMSD
#     run in VMD after loading mature and immature 
#     reference pdbs
#
proc miAlign { } {
   set sel_m [atomselect 0 "protein and backbone and residue 16 to 116 and not hydrogen"]
   set sel_i [atomselect 1 "protein and backbone and residue 1 to 101 and not hydrogen"]

   set sel_whole [atomselect 1 "all"]

   set M [measure fit $sel_i $sel_m]
   $sel_whole move $M
}

proc miRMSD { } {
  set sel_m [atomselect 0 "protein and backbone and resid 16 to 221 and not index 3453 and not hydrogen"]
  set sel_i [atomselect 1 "protein and backbone and resid 148 to 353 and not hydrogen"]

  return [measure rmsd $sel_i $sel_m]
}
