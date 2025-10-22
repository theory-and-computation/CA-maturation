#!/bin/bash
if [ -f "copy.sh" ]; then
    chmod +x copy.sh
    echo "Running copy.sh in $(pwd)"
    ./copy.sh
else
    echo "copy.sh not found in $(pwd)"
    exit 1
fi

for dir in */; do
    [[ -d "$dir" && "$dir" =~ ^[0-9]+/$ ]] || continue
    if [ -f "${dir}pmemd-prep.sh" ]; then
        echo "########################### RUNNING $dir ###########################"
        cd "$dir" || continue
        chmod +x pmemd-prep.sh
        echo "Running pmemd-prep.sh in $(pwd)"
        ./pmemd-prep.sh
        [ -f frame-ba.pdb ] && rm frame-ba.pdb
        cd ..
        echo "########################### COMPLETED $dir ###########################"
    fi
done

