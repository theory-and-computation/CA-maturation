#!/bin/bash

source_dir=$(pwd)

FILES_TO_COPY=("*.in" "rename.py" "pmemd-prep.sh" "pmemd-equil.sh" "pmemd-run.sh")

# Only process directories whose names are purely numeric (e.g., 1/, 2/, 10/, 32/)
for dir in */; do
    [[ -d "$dir" && "$dir" =~ ^[0-9]+/$ ]] || continue
    dir_name="${dir%/}"
    echo "########################### COPYING FILES TO $dir_name ###########################"

    for file in "${FILES_TO_COPY[@]}"; do
        for match in "$source_dir"/$file; do
            if [ -f "$match" ]; then
                cp "$match" "$dir"
                echo "Copied $(basename "$match") to $dir_name"
            fi
        done
    done

    echo "########################### COMPLETED COPYING TO $dir_name ###########################"
done

