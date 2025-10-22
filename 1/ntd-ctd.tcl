mol new frame-1.pdb

set ntd [atomselect 0 "resid 1 to 149"]
set ctd [atomselect 0 "resid 150 to 221"]

$ntd writepdb frame-1-ntd.pdb
$ctd writepdb frame-1-ctd.pdb

exit
