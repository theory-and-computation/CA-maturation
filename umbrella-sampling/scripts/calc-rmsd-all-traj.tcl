# CC: calculate RMSD of current CA to reference mature/immature
#     over time for all CV windows, print along with current CVs

# arguments: 
# indir (directory of directories with dcd files)
# outfile (output text file name)
# s (stride for trajectory calculations, we used 10)
source calc-colvars-fcn.tcl

set infile "CA-mature.pdb"
set indir [lindex $argv 0]
set outfile [lindex $argv 1]
set s [lindex $argv 2]

set out [open $outfile w+]

# alignment reference
mol new "all-atom-MI.pdb"
set sel_m [atomselect top "residue 0 to 221" frame 0]
set sel_i [atomselect top "residue 0 to 221" frame 1]

mol new ${infile}
set cvs [glob -directory $indir -type d *]
set nf [llength $cvs]

for {set i 0} {$i < $nf} {incr i} {
    set dir [lindex $cvs $i]
    set colvars [lindex [split $dir "/"] [expr -1 + [llength [split $dir "/"]]]]
    set theta [string range $colvars 0 [expr [string last "-" $colvars] - 1]]
    set dist [string range $colvars [expr [string last "-" $colvars] + 1] end]
    set coor [glob -directory $dir "./${colvars}.dcd"]
    mol addfile $coor molid 1 waitfor all

    # stride: number of frames to skip
    set stride $s
    set nframes [molinfo 1 get numframes]
    set n_iter [expr min(50,$nframes/$stride)]

    mol top 1
    
    for {set j 0} {$j < $n_iter} {incr j} {
	set f [expr $j * $stride]
       # CoM of C terminal domain
	set sel_curr [atomselect 1 "residue 0 to 221 and protein and backbone and not hydrogen and not index 3453" frame $f]
	set sel_whole [atomselect 1 "all" frame $f]
	# align CURRENT to IMMATURE
        set M [measure fit $sel_curr $sel_i]
        $sel_whole move $M

	set seli_all [atomselect 0 "all" frame 1]
	set cv1 [measure rmsd $sel_curr $seli_all]

	#align CURRENT to MATURE
	set M [measure fit $sel_curr $sel_m]
	$sel_whole move $M
	
	set selm_all [atomselect 0 "all" frame 0]
	set cv2 [measure rmsd $sel_curr $selm_all]

       set distReal [cvDist 1 $f]
       set thetaReal [cvTheta 1 $f]

	# print phi, xi, RMSD to immature, RMSD to mature
	puts $out "${thetaReal},${distReal},${cv1},${cv2}"
   }
    animate delete all
}
exit
