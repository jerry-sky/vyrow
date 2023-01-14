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
LONG_OPTIONS="keep-original,dont-copy-stylesheet,toc"

# parse given options (switches)
PARSED=$(getopt --options=$OPTIONS --longoptions=$LONG_OPTIONS --name "$0" -- "$@")
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
# do not remove the original Markdown document (off by default, remove originals by default)
keep_original=""
# do not copy the stylesheet file (off by default, copy the stylesheet by default)
dont_copy_stylesheet=""
# generate ToC based on level 2+ headers in the document
toc=""

while true; do
    case "$1" in
        -t)
            template="$2"
            shift 2
            ;;
        --toc)
            toc="--toc"
            shift 1
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
        --keep-original)
            keep_original="y"
            shift 1
            ;;
        --dont-copy-stylesheet)
            dont_copy_stylesheet="y"
            shift 1
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
if [ -z "$dont_copy_stylesheet" ]; then
    cp -- "$stylesheet" "$working_dir"
fi


file='/tmp/___vyrow_tmp_document.md'
include_before_body='/tmp/___vyrow_tmp_before_body.html'

title_regex_expression='^(\s*\#\s?)(.+)(\s*)$'

# convert all Markdown documents in the working directory to HTML documents
find "$working_dir" -type f | grep '\.md$' |
while read original_file; do
    cp "$original_file" "$file"
    # don’t modify the metadata by default
    metadata="METADATA"
    # to be inserted before TOC (empty the file)
    >"$include_before_body"
    # check if the document has a YAML metadata block
    if [ "$(head -n1 "$file")" != "---" ]; then
        # extract the first h1 value to set as a page title
        # (`xargs` is here for whitespace trimming)
        title=$(perl -0777 -pe 's/'"$title_regex_expression"'/$2\n/gm' "$file" | head -n1 | xargs)
        if [ -n "$title" ]; then
            # extracted header title is not empty
            # add a page title
            metadata="pagetitle=$title"
            # remove the original header from the file
            sed -E '0,/'"$title_regex_expression"'/{/'"$title_regex_expression"'/d}' -i "$file"
        else
            # if no header title found use filename
            # strip directory
            title="${original_file##*/}"
            # strip extension (only the last one)
            title="${title%.*}"
            metadata="pagetitle=$title"
        fi
        # add the header before TOC
        printf '%s\n' "<h1>$title</h1>" >>"$include_before_body"
    fi
    # first, prerender the document into JSON
    # then, use `pandoc-katex` to prerender LaTeX
    # finally, render the document into HTML and save it
    "$dir"/pandoc "$file" \
        --metadata "$metadata" \
        --standalone \
        --from markdown-blank_before_header-implicit_figures+lists_without_preceding_blankline+gfm_auto_identifiers \
        --to json \
            | "$dir"/pandoc-katex \
                | "$dir"/pandoc \
                    --from json \
                    --to html \
                    --template "$template" \
                    --css "$website_root${stylesheet##*/}" \
                    --standalone $toc \
                    --include-before-body="$include_before_body" \
                    -H "$headers" \
                        > "${original_file%???}"".html" # replace `.md` with `.html`
    # remove the raw Markdown document
    if [ -z "$keep_original" ]; then
        rm "$original_file"
    fi
done
