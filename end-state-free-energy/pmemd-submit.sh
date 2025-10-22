#!/bin/bash

for dir in */; do
    [[ -d "$dir" && "$dir" =~ ^[0-9]+/$ ]] || continue

    if [ -f "${dir}pmemd-equil.sh" ] && [ -f "${dir}pmemd-run.sh" ]; then
        echo "############# RUNNING $dir #############"
        cd "$dir" || continue
        chmod +x pmemd-equil.sh pmemd-run.sh

        dir_number="${dir%/}"  # remove trailing slash
        equil_output=$(sbatch --job-name=equil-"$dir_number" pmemd-equil.sh)
        JOBID=$(echo "$equil_output" | awk '{print $4}')

        if [ -z "$JOBID" ]; then
            echo "Failed to submit pmemd-equil.sh in $dir"
            cd ..
            continue
        fi

        echo "Equilibration job submitted with JOBID: $JOBID"
        sbatch --dependency=afterok:$JOBID --job-name=run-"$dir_number" pmemd-run.sh
        cd ..
        echo "############# COMPLETED $dir #############"
    else
        echo "Skipping $dir - Missing pmemd-equil.sh or pmemd-run.sh"
    fi
done

