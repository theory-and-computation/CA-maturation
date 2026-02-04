# CC: strip waters from all .dcd trajectory files

# arguments: 
# indir (directory of directories with dcd files)
# idxfile (file with indices of atoms to keep)
# s (stride for output trajectories)

set infile "pdbs/CA-mature.pdb"
set infileprot "pdbs/CA-mature-protein.pdb"

set indir [lindex $argv 0]
set idxfile [lindex $argv 1]
set s [lindex $argv 2]

mol new $infile waitfor all
mol new $infileprot waitfor all
animate delete all 0
animate delete all 1
mol top 0

set cvs [glob -directory $indir -type d *]
set nf [llength $cvs]

for {set i 0} {$i < $nf} {incr i} {
    set dir [lindex $cvs $i]
    set colvars [lindex [split $dir "/"] [expr -1 + [llength [split $dir "/"]]]]
    set coor [glob -directory $dir "./${colvars}.dcd"]
    mol addfile $coor molid 0 waitfor all

    set outfile "${dir}/${colvars}-protein.dcd"

    if {![file exists $outfile]} {
	set nframes [molinfo 0 get numframes]
	set n_iter [expr $nframes/$s]
    
	for {set j 0} {$j < $n_iter} {incr j} {
	    set f [expr $j * $s]
	    set sel [atomselect 0 "protein" frame $f]
	    $sel writepdb "$j.tmp.pdb"
	    animate read pdb "$j.tmp.pdb" 1
	    rm "$j.tmp.pdb"
	}
	animate write dcd $outfile waitfor all 1
    }
    animate delete all 0
    animate delete all 1
}

exit
