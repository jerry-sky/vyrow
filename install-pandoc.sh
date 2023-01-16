#!/bin/bash

archive="pandoc.tar.gz"

version="2.19.2"

# download the archive containing the executable
curl -L --output "$archive" "https://github.com/jgm/pandoc/releases/download/$version/pandoc-$version-linux-amd64.tar.gz"

# unpack the archive
tar -x "pandoc-$version/bin/pandoc" --strip-components=2 -f "$archive"

# remove the archive
rm "$archive"
