#!/bin/bash
set -euo pipefail

mkdir -p output

for dir in */; do
    [ "$dir" = "output/" ] && continue
    dirname="${dir%/}"
    for file in "$dir"*.{jpg,jpeg,png,gif,bmp,tiff,webp,svg}; do
        [ -f "$file" ] || continue
        basename="${file##*/}"
        cp "$file" "output/${dirname}-${basename}"
    done
done
