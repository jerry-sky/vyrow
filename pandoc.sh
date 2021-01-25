#!/bin/bash

# file to convert from
input_file="$1"
# path to the pandoc template file
template="$2"
# the name of the styles files (CSS file)
stylesheet_filename="$3"
# path to the headers file (additional headers to be included inside the `<head>` element in the output HTML document)
headers="$4"

# get the script running directory
dir="${BASH_SOURCE%/*}"

# first, prerender the document into JSON
# then, use `pandoc-katex` to prerender LaTeX
# finally, render the document into HTML
pandoc "$input_file" \
    --standalone \
    --from markdown+yaml_metadata_block+gfm_auto_identifiers \
    --to json \
        | "$dir"/pandoc-katex \
            | pandoc \
                --from json \
                --to html \
                --template "$template" \
                --css "$stylesheet_filename" \
                --standalone \
                -H "$headers"
