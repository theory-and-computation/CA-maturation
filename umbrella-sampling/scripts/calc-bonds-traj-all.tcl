# CC: scan through folders of dcd trajectories
#     measure bond over time between two atoms with given indices
#     print bond length to text file along with CVs
#     (data not shown in paper but this was used to examine
#     stability of certain salt bridges)
#
# arguments: 
# indir (directory of directories containing trajectories)
# outfile (name of output text file)
# atoms (two ints, pdb file atom indices of bond pair)

set infile "CA-mature.pdb"
set indir [lindex $argv 0]
set outfile [lindex $argv 1]
set atoms [list [lindex $argv 2] [lindex $argv 3]]

set out [open $outfile w+]

mol new ${infile}
animate delete all
set cvs [glob -directory $indir -type d *]
set nf [llength $cvs]

for {set i 0} {$i < $nf} {incr i} {
    set dir [lindex $cvs $i]
    set colvars [lindex [split $dir "/"] [expr -1 + [llength [split $dir "/"]]]]
    set theta [string range $colvars 0 [expr [string last "-" $colvars] - 1]]
    set dist [string range $colvars [expr [string last "-" $colvars] + 1] end]
    set coor [glob -directory $dir "./${colvars}.dcd"]
    mol addfile $coor molid 0 waitfor all
    
    set cv1 [measure bond $atoms molid 0 frame all]
    puts $out "${theta} ${dist} ${cv1}"
    animate delete all
}
exit
