# load mature and immature structures
# align them show CVs as balls and lines
# used on PDBs with only CA protein

# arguments:
# infile (pdb file)
# c (chain id to use)

set infile [lindex $argv 0]
mol new $infile
set c [lindex $argv 1]

color Display Background white
display projection orthographic
axes location Off

# ntd
mol modselect 0 0 resid 16 to 145 and backbone and chain $c
mol modcolor 0 0 ColorID 7
mol modmaterial 0 0 AOChalky
mol modstyle 0 0 NewCartoon 0.3 10.0 4.1 0

# ctd
mol addrep 0
mol modselect 1 0 resid 145 to 221 and backbone and chain $c
mol modcolor 1 0 ColorID 14
mol modmaterial 1 0 AOChalky
mol modstyle 1 0 NewCartoon 0.3 10.0 4.1 0

set r 2
set w 4

set sel [atomselect 0 "resid 17 to 46 and backbone and not hydrogen and chain ${c}"]
set 1m [measure center $sel weight mass]

set sel [atomselect 0 "resid 132 to 136 and backbone and not hydrogen and chain ${c}"]
set 2m [measure center $sel weight mass]

set sel [atomselect 0 "resid 137 to 146 and backbone and not hydrogen and chain ${c}"]
set 3m [measure center $sel weight mass]

set sel [atomselect 0 "resid 172 to 181 and backbone and not hydrogen and chain ${c}"]
set 4m [measure center $sel weight mass]

set sel [atomselect 0 "resid 197 to 204 and backbone and not hydrogen and chain ${c}"]
set 5m [measure center $sel weight mass]

mol new

# start with distance cv
graphics 1 color red

graphics 1 sphere $2m radius $r
graphics 1 sphere $5m radius $r

graphics 1 line $2m $5m width $w style solid

# then the dihedral
mol new
graphics 2 color red

graphics 2 sphere $1m radius $r
graphics 2 sphere $2m radius $r
graphics 2 sphere $3m radius $r
graphics 2 sphere $4m radius $r

graphics 2 line $1m $2m width $w style solid
graphics 2 line $2m $3m width $w style solid
graphics 2 line $3m $4m width $w style solid

# calculate cvs

set dist [veclength [vecsub $2m $5m]]

set b1 [vecsub $1m $2m]
set b2 [vecnorm [vecsub $3m $2m]]
set b3 [vecsub $4m $3m]

set v [vecsub $b1 [vecscale $b2 [vecdot $b1 $b2]]]
set w [vecsub $b3 [vecscale $b2 [vecdot $b3 $b2]]]

set x [vecdot $v $w]
set y [vecdot [veccross $b2 $v] $w]

set dhdr [expr 180 / atan(1) / 4 * atan2($y, $x)]

puts "dist:"
puts $dist
puts "dihedral:"
puts $dhdr
