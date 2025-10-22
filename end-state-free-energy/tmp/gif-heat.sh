#!/bin/bash

output="pairwise_heatmap.mp4"
fps=3

rm -f input.txt

for img in $(ls *.png | sort -V -r); do
    echo "file '$img'" >> input.txt
done

ffmpeg -f concat -safe 0 -r $fps -i input.txt -c:v libx264 -pix_fmt yuv420p "$output"

rm input.txt

echo "MP4 created: $output"

