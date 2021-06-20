#!/bin/bash

# get the script running directory
dir="${BASH_SOURCE%/*}"

# check whether `getopt` is available
getopt --test > /dev/null
if [ "$?" -ne 4 ]; then
    echo "getopt not available in this environment"
    exit 1
fi

OPTIONS="d:t:s:h:r:"

# parse given options (switches)
PARSED=$(getopt --options=$OPTIONS --name "$0" -- "$@")
if [[ "$?" -ne 0 ]]; then
    # invalid options detected
    exit 2
fi
# read getopt’s output this way to handle the quoting right
eval set -- "$PARSED"

# path to the Pandoc template file
template="$dir/template/pandoc-template.html"
# styling
stylesheet="$dir/template/style.css"
# website root
website_root="/"
# path to the headers file (additional headers to be included inside the `<head>` element in the output HTML document)
headers="$dir/template/head.html"
# the directory that contains the Markdown documents to render
working_dir=""

while true; do
    case "$1" in
        -t)
            template="$2"
            shift 2
            ;;
        -s)
            stylesheet="$2"
            shift 2
            ;;
        -h)
            headers="$2"
            shift 2
            ;;
        -d)
            working_dir="$2"
            shift 2
            ;;
        -r)
            website_root="$2"
            shift 2
            ;;
        --)
            shift
            break
            ;;
    esac
done

# require working directory
if [ -z "$working_dir" ]; then
    "you need to provide a working directory (-d dir)"
    exit 1
fi

# make sure there are not dashes in the front
working_dir=$(readlink -f -- "$working_dir")

# make sure the directory exists
mkdir -p "$working_dir"

# copy the stylesheet to the working directory
cp -- "$stylesheet" "$working_dir"

# convert all Markdown documents in the working directory to HTML documents
find "$working_dir" -type f | grep '\.md$' |
while read file; do
    # first, prerender the document into JSON
    # then, use `pandoc-katex` to prerender LaTeX
    # finally, render the document into HTML and save it
    "$dir"/pandoc "$file" \
        --standalone \
        --from markdown-blank_before_header-implicit_figures+lists_without_preceding_blankline+gfm_auto_identifiers \
        --to json \
            | "$dir"/pandoc-katex \
                | "$dir"/pandoc \
                    --from json \
                    --to html \
                    --template "$template" \
                    --css "$website_root${stylesheet##*/}" \
                    --standalone \
                    -H "$headers" \
                        > "${file%???}"".html" # replace `.md` with `.html`
    # remove the raw Markdown document
    rm "$file"
done
