#!/bin/bash

PATTERNS=("_MMPBSA*" "slurm-*" "*nc" "*out" "*png" "*rst")

for dir in */; do
    [[ -d "$dir" ]] || continue
    echo "Processing $dir"

    for pat in "${PATTERNS[@]}"; do
        files=( "$dir"$pat )
        # Remove only if something matches
        if [[ -e "${files[0]}" ]]; then
            rm -f "${files[@]}"
            echo "Removed pattern '$pat' in $dir"
        else
            echo "No match for '$pat' in $dir"
        fi
    done

    echo "Completed $dir"
done

