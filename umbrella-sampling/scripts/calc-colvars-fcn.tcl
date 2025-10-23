# CC: calculate collective variables xi and phi
#     for current CA conformation
#     used to relate other quantities like linker flexibility
#     to different conformational states (fig 2C)

# pass molid (int or "top") and frame (int or "first" "last" "now")
# get xi (distance cv)
proc cvDist { atid i } {

# Calculate center of mass of group 1 (helix 7 top)
set sel [atomselect $atid "residue 131 to 135 and protein and backbone" frame $i]
set h7 [measure center $sel]

set sel [atomselect $atid "residue 196 to 203 and backbone and protein" frame $i]
set h10 [measure center $sel]

set dist [veclength [vecsub $h7 $h10]]

return $dist

}

# pass molid and frame
# get phi (dihedral CV)
proc cvTheta { atid i } {

    set sel [atomselect $atid "residue 131 to 135 and backbone and protein" frame $i]
    set h7 [measure center $sel]
    
set sel [atomselect top "residue 136 to 145 and backbone and protein" frame $i]
set h7b [measure center $sel]

# calculate center of mass of group 2 (helix 4)
set sel [atomselect top "residue 70 to 80" frame $i]
set h4 [measure center $sel]

# Calculate center of mass of group 2 (helix 10)
set sel [atomselect top "residue 196 to 203" frame $i]
set h10 [measure center $sel]

# CoM of helix 8+9 linker
set sel [atomselect top "residue 171 to 180 and backbone and protein" frame $i]
set h8 [measure center $sel]

# Calculate center of mass of group 4 (helix 1-2)
set sel [atomselect top "residue 16 to 45 and backbone and protein" frame $i]
set h2 [measure center $sel]

# Calculate dihedral angle H1+2+H7bottom-H8-H10
set b1 [vecsub $h2 $h7]
set b2 [vecnorm [vecsub $h7b $h7]]
set b3 [vecsub $h8 $h7b]

set v [vecsub $b1 [vecscale $b2 [vecdot $b1 $b2]]]
set w [vecsub $b3 [vecscale $b2 [vecdot $b3 $b2]]]

set x [vecdot $v $w]
set y [vecdot [veccross $b2 $v] $w]

set dhdr2 [expr 180 / atan(1) / 4 * atan2($y, $x)]

return $dhdr2

}
