#!/bin/bash

source_dir=$(pwd)

FILES_TO_COPY=("*.in" "rename.py" "pmemd-prep.sh" "pmemd-equil.sh" "pmemd-run.sh")

for dir in */; do
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

