#!/bin/bash

archive="pandoc-katex.tar.gz"

version="0.1.10"

# download the archive containing the executable
curl -L --output "$archive" "https://github.com/xu-cheng/pandoc-katex/releases/download/$version/pandoc-katex-$version-x86_64-unknown-linux-gnu.tar.gz"

# unpack the archive
tar -x "./bin/pandoc-katex" --strip-components=2 -f "$archive"

# remove the archive
rm "$archive"
