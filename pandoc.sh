#!/bin/bash

# file to convert from
input_file="$1"
# path to the pandoc template file
template="$2"
# the name of the styles files (CSS file)
## please note — this is NOT a full path to the file,
## the full path will be resolved with respect to the `<base>` tag defined in the `<head>` of the HTML output document
stylesheet_filename="$3"
# path to the headers file (additional headers to be included inside the `<head>` element in the output HTML document)
headers="$4"

# get the script running directory
dir="${BASH_SOURCE%/*}"

# first, prerender the document into JSON
# then, use `pandoc-katex` to prerender LaTeX
# finally, render the document to HTML
pandoc "$input_file" \
    --standalone \
    --from markdown+yaml_metadata_block \
    --to json \
        | "$dir"/pandoc-katex \
            | pandoc \
                --from json \
                --to html \
                --template "$template" \
                --css "$stylesheet_filename" \
                --standalone \
                -H "$headers"
