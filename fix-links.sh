#!/bin/bash

find . -type f | grep '\.html$' |
while read file; do
    # links are without the `.html` at the end — GH Pages handles it
    perl -i -pe 's/(")([^"]+)(\.md)(\#[^"]+)?(")/"$2$4"/gm' -- "$file"
done
