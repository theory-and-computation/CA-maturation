# CC: print coordinates of Ca atoms of linker
#     along with CVs for RMSF calculations
#     used to relate RMSF to conformational state (Fig 2C)

# arguments:
# indir (directory of directories with dcd files)
# outfile (output text file name)
#
source calc-colvars-fcn.tcl

set infile "CA-mature.pdb"
set indir [lindex $argv 0]
set outfile [lindex $argv 1]

set out [open $outfile w+]

# alignment reference
mol new "all-atom-MI.pdb"
set sel_i [atomselect top "residue 146 to 150" frame 1]

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
    set stride 10 
    set nframes [molinfo 1 get numframes]
    set n_iter [expr min(50,$nframes/$stride)]

    mol top 1
    
    for {set j 0} {$j < $n_iter} {incr j} {
	set f [expr $j * $stride]
       # CoM of C terminal domain
	set sel_m [atomselect 1 "residue 146 to 150 and protein and backbone and not hydrogen" frame $f]
	set sel_whole [atomselect 1 "all" frame $f]
	# align CURRENT to IMMATURE to standardize
        set M [measure fit $sel_m $sel_i]
        $sel_whole move $M

       set sel_linker [atomselect 1 "protein and backbone and residue 146 to 150 and type CA" frame $f]
       set linker_xyz [concat [$sel_linker get {x y z}]]

       set distReal [cvDist 1 $f]
       set thetaReal [cvTheta 1 $f]

       puts $out "${thetaReal},${distReal},${linker_xyz}"
   }
    animate delete all
}
exit
