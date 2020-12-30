#!/bin/bash

archive="pandoc-katex-0.1.4-x86_64-unknown-linux-gnu.tar.gz"

# download the 0.1.4 release
wget https://github.com/xu-cheng/pandoc-katex/releases/download/0.1.4/"$archive"

# unpack the binary
tar -zxf "$archive" ./bin/pandoc-katex --strip-components 2

# remove the archive
rm "$archive"

echo 'the binary `pandoc-katex` has been installed locally'
