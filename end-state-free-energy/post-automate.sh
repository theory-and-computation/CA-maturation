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
            mpirun -np 8 MMPBSA.py.MPI -O -i mmpbsa-pairwise.in -o FINAL_RESULTS_PAIRWISE.dat \
                -do FINAL_PAIRWISE.dat -sp complex-solvated.prmtop -cp frame.prmtop \
                -rp frame-ntd.prmtop -lp frame-ctd.prmtop -y prod1.nc
        else
            echo "No .nc files found in $dir. Skipping MMPBSA runs."
        fi

        cd ..
        echo "############# COMPLETED $dir #############"
    fi
done




### PART 2: Running plot-occupancy.py after all calculations are complete ###
PLOT_SCRIPT_PATH="./plot-occupancy.py"

if [ ! -f "$PLOT_SCRIPT_PATH" ]; then
    echo "Error: plot-occupancy.py not found in the current directory."
    exit 1
fi

for DIR in */ ; do
    if [ -d "$DIR" ]; then 
        echo "############# PLOTTING IN $DIR #############"
        cp "$PLOT_SCRIPT_PATH" "$DIR"

        cd "$DIR" || continue
        
        # Run plot-occupancy.py
        if [ -f "plot-occupancy.py" ]; then  
            echo "Running plot-occupancy.py in $DIR"
            python3 plot-occupancy.py
        else
            echo "Failed to copy plot-occupancy.py to $DIR. Skipping."
        fi

        rm plot-occupancy.py       
	cd ..
        echo "############# COMPLETED PLOTTING IN $DIR #############"
    fi
done


### PART 3: Run VMD for rendering in each directory ###
for DIR in */ ; do
    if [ -d "$DIR" ]; then 
        echo "############# RUNNING VMD IN $DIR #############"       
        cd "$DIR" || continue     
        if [ -f "visualize-residues.tcl" ]; then
            #vmd -e visualize-residues.tcl
            cat visualize-residues.tcl | vmd
        else
            echo "visualize-residues.tcl not found in $DIR. Skipping VMD rendering."
        fi
        cd ..     
        echo "############# COMPLETED VMD IN $DIR #############"
    fi
done


### PART 4: Combining Images and Creating GIF ###
echo "############# COMBINING IMAGES #############"

plot_width=2500
plot_height=1500
render_width=1500
render_height=1500

frame_index=1

for frame_number in {1..33}; do
    if [ "$frame_number" -eq 33 ]; then
        echo "Skipping frame $frame_number (excluded by convention)"
        continue
    fi

    png_file="plots/decomp-${frame_number}.png"
    tga_file="images/render-${frame_number}.tga"
    resized_png_file="plots/decomp-${frame_number}-resized.png"
    resized_tga_file="images/render-${frame_number}-resized.tga"
    padded_frame=$(printf "frame-%03d.png" "$frame_index")
    combined_file="combined/$padded_frame"

    if [ -f "$png_file" ] && [ -f "$tga_file" ]; then
        convert "$png_file" -resize ${plot_width}x${plot_height}\! "$resized_png_file"
        convert "$tga_file" -resize ${render_width}x${render_height}\! "$resized_tga_file"

        convert +append "$resized_png_file" "$resized_tga_file" "$combined_file"

        rm "$resized_png_file" "$resized_tga_file"

        echo "Combined $png_file and $tga_file -> $combined_file"
        frame_index=$((frame_index + 1))
    else
        echo "Skipping frame $frame_number, files not found."
    fi
done


# part 5

if [ -d "combined" ] && ls combined/frame-*.png 1> /dev/null 2>&1; then
    cd combined || exit 1

    mkdir -p tmp_frames
    count=0
    for img in $(ls frame-*.png | sort -Vr); do
        printf -v newname "frame-%05d.png" "$count"
        cp "$img" "tmp_frames/$newname"
        ((count++))
    done

    ffmpeg -y -framerate 2 -i tmp_frames/frame-%05d.png -vf "format=yuv420p" combined.mp4
    echo "MP4 created as combined.mp4"

    echo "Creating GIF in reverse order..."
    convert -delay 50 -loop 0 $(ls frame-*.png | sort -Vr) combined.gif
    echo "GIF created as combined.gif"

    rm -r tmp_frames
    cd ..
else
    echo "No combined images found to create animations. Please check the combined/ directory."
fi

