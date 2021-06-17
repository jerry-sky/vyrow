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
"$dir"/pandoc "$input_file" \
    --standalone \
    --from markdown-blank_before_header-implicit_figures+lists_without_preceding_blankline+gfm_auto_identifiers \
    --to json \
        | "$dir"/pandoc-katex \
            | "$dir"/pandoc \
                --from json \
                --to html \
                --template "$template" \
                --css "$stylesheet_filename" \
                --standalone \
                -H "$headers"
