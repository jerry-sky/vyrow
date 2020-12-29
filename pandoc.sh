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
# URL with the MathJax script that enables LaTeX markup on the website
mathjax="$5"

pandoc "$input_file" \
    --mathjax="$mathjax" \
    --standalone \
    --from markdown+yaml_metadata_block \
    --to html \
    --template "$template" \
    --css "$stylesheet_filename" \
    -H "$headers"
