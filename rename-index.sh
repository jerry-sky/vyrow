#!/bin/bash

index_file="$(ls | grep -iE ^readme\.html$ | head -n1)"
if [ -n "$index_file" ]; then
    mv -- "$index_file" index.html
else
    echo "::warning::missing the main readme file thus no index.html has been generated"
fi
