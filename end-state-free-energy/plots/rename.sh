#!/usr/bin/env bash

mkdir -p renamed

for old in decomp-*.png; do
    num=$(echo "$old" | sed -E 's/decomp-([0-9]+)\.png/\1/')
    new_num=$((num - 1))
    new=$(printf "decomp-%d.png" "$new_num")
    cp "$old" "renamed/$new"
done

echo "Renamed files are in ./renamed/"

