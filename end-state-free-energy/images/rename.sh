#!/bin/bash

for f in render-*.tga; do
    num=$(echo "$f" | sed -E 's/render-0*([0-9]+)\.tga/\1/')
    # Increment by 1
    newnum=$((num + 1))
    mv -v "$f" "render-${newnum}.tga"
done

