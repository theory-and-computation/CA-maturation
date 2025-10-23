# CC: From coordinate references and frames, produce a pdb
#     used to assemble minimum free energy pathway (Fig 3)

# Usage: vmd -dispdev text -e get-image.tcl -args
#          [inputFile] [outDCD]

set inputFile [lindex $argv 0]
set outDCD [lindex $argv 1]

mol new "CA-mature.pdb"
set sel0 [atomselect top "protein and backbone and residue 31 to 130 and not hydrogen" frame 0]
animate delete all

set f [open ${inputFile} r]
set fData [read $f]
close $f

set imgList [split $fData "\n"]
set nImg [llength $imgList]

for {set i 0} {$i < [expr $nImg-1]} {incr i} {
    set img [lindex $imgList $i]
    set imgSplit [split $img ", "]
    set dcdFile [lindex $imgSplit 0]
    set frm [expr [lindex $imgSplit 2] - 1]
    
    mol addfile ${dcdFile} first $frm last $frm waitfor all
    set selWhole [atomselect top "protein" frame now]
    set selN [atomselect top "protein and backbone and residue 31 to 130 and not hydrogen" frame now]
    set M [measure fit $selN $sel0]
    $selWhole move $M
}

animate write dcd ${outDCD} beg 0 end [expr $nImg-2] waitfor all

exit
