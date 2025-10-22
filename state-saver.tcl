set output_prefix "frame-"
set molID [molinfo top get id]

for {set i 1} {$i <= 32} {incr i} {
    animate goto [expr {$i - 1}]
    set sel [atomselect $molID "segname 0A0"]
    set output_file "${output_prefix}$i.pdb"
    $sel writepdb $output_file
    $sel delete
    puts "Saved: $output_file"
}

puts "All specified frames processed."

