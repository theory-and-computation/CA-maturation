#!/bin/bash

### PART 1: Running MMPBSA.py.MPI calculations ###
for dir in $(seq 1 32); do
    if [ -d "$dir" ]; then
        echo "############# RUNNING $dir #############"
        cd "$dir" || continue

        if ls *.nc 1> /dev/null 2>&1; then
            echo "Running MMPBSA.py.MPI (standard decomposition) in $dir"
            mpirun -np 1 MMPBSA.py.MPI -O -i mmpbsa.in -o FINAL_RESULTS_MMPBSA.dat \
                -do FINAL_DECOMP_MMPBSA.dat -sp complex-solvated.prmtop -cp frame.prmtop \
                -rp frame-ntd.prmtop -lp frame-ctd.prmtop -y prod1.nc

            echo "Running MMPBSA.py.MPI (pairwise decomposition) in $dir"
#            mpirun -np 1 MMPBSA.py.MPI -O -i mmpbsa-pairwise.in -o FINAL_RESULTS_PAIRWISE.dat \
#                -do FINAL_PAIRWISE.dat -sp complex-solvated.prmtop -cp frame.prmtop \
#                -rp frame-ntd.prmtop -lp frame-ctd.prmtop -y prod1.nc
        else
            echo "No .nc files found in $dir. Skipping MMPBSA runs."
        fi

        cd ..
        echo "############# COMPLETED $dir #############"
    fi
done




### PART 2: Running plot-occupancy.py after all calculations are complete ###
#PLOT_SCRIPT_PATH="./plot-occupancy.py"
#
#if [ ! -f "$PLOT_SCRIPT_PATH" ]; then
#    echo "Error: plot-occupancy.py not found in the current directory."
#    exit 1
#fi
#
#for DIR in */ ; do
#    if [ -d "$DIR" ]; then 
#        echo "############# PLOTTING IN $DIR #############"
#
#        # Copy plot-occupancy.py to the directory
#        cp "$PLOT_SCRIPT_PATH" "$DIR"
#
#        cd "$DIR" || continue
#        
#        # Run plot-occupancy.py
#        if [ -f "plot-occupancy.py" ]; then  
#            echo "Running plot-occupancy.py in $DIR"
#            python3 plot-occupancy.py
#        else
#            echo "Failed to copy plot-occupancy.py to $DIR. Skipping."
#        fi
#
#        rm plot-occupancy.py       
#	cd ..
#        echo "############# COMPLETED PLOTTING IN $DIR #############"
#    fi
#done
#
#
#### PART 3: Run VMD for rendering in each directory ###
#for DIR in */ ; do
#    if [ -d "$DIR" ]; then 
#        echo "############# RUNNING VMD IN $DIR #############"
#        
#        cd "$DIR" || continue
#        
#        if [ -f "visualize-residues.tcl" ]; then
#            vmd -e visualize-residues.tcl
#        else
#            echo "visualize-residues.tcl not found in $DIR. Skipping VMD rendering."
#        fi
#        cd ..
#        
#        echo "############# COMPLETED VMD IN $DIR #############"
#    fi
#done
#
#
#### PART 4: Combining Images and Creating GIF ###
#echo "############# COMBINING IMAGES #############"
#
#mkdir -p combined
#
#desired_width=1700
#desired_height=1500
#
#for frame_number in {1..33}; do
#    png_file="plots/decomp-${frame_number}.png"
#    tga_file="images/render-${frame_number}.tga"
#    resized_tga_file="images/render-${frame_number}-resized.tga"
#    combined_file="combined/combined-${frame_number}.png"
#    
#    if [ -f "$png_file" ] && [ -f "$tga_file" ]; then
#        convert "$tga_file" -resize ${desired_width}x${desired_height}\! "$resized_tga_file"
#        convert +append "$png_file" "$resized_tga_file" "$combined_file"
#        
#        rm "$resized_tga_file"
#
#        echo "Combined $png_file and $tga_file -> $combined_file"
#    else
#        echo "Skipping frame $frame_number, files not found."
#    fi
#done
#
#echo "############# IMAGE COMBINATION COMPLETED #############"
#
#
#
#### PART 5: Creating GIF from Combined Images ###
#echo "############# CREATING GIF #############"
#
#if [ -d "combined" ] && ls combined/combined-*.png 1> /dev/null 2>&1; then
#    cd combined || exit 1
#
#    convert -delay 10 -loop 0 $(ls combined-*.png | sort -V) combined_animation.gif
#
#    echo "GIF creation completed! Saved as combined/combined_animation.gif"
#
#    cd ..
#else
#    echo "No combined images found to create GIF. Please check the combined/ directory."
#fi

