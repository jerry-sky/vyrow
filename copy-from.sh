#!/bin/bash

wrk_dir="$1"
src_dir="$2"

if [ -n "$src_dir" ]; then
    # given source directory is not empty

    # get the absolute paths of the source and working directories
    wrk_dir=$(readlink -f -- "$wrk_dir")
    src_dir=$(readlink -f -- "$src_dir")

    if [ "$wrk_dir" = "$src_dir" ]; then
        echo "::warning::working directory is the same as the source directory"
        exit 0
    fi

    exclude=""

    echo "$wrk_dir" | grep ^"$src_dir" >/dev/null
    if [ "$?" -eq 0 ]; then
        # the source directory *does* contain the working directory
        # exclude the working directory from copying
        exclude="${wrk_dir#$src_dir}"
    fi

    rsync -r "$src_dir"/{*,.[!.]?*} "$wrk_dir" --exclude .git --exclude "$exclude"

fi
