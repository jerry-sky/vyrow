#!/bin/bash

wrk_dir="$1"
src_dir="$2"

if [ -n "$src_dir" ]; then
    # given source directory is not empty

    # get the absolute paths of the source and working directories
    wrk_dir=$(readlink -f "$wrk_dir")
    src_dir=$(readlink -f "$src_dir")

    # get the list of all files to copy excluding those
    # that are the working directory itself or the `.git` directory
    find "$src_dir" -type f | grep -v ^"$wrk_dir" | grep -v '\/\.git\/'
        | xargs -d '\n' cp -r -t "$wrk_dir" --
fi
