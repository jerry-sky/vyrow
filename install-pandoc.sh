#!/bin/bash

deb="pandoc-2.11.3.2-1-amd64.deb"

# download the 2.11.3.2 release
wget "https://github.com/jgm/pandoc/releases/download/2.11.3.2/$deb"

# install it
sudo dpkg -i "$deb"

# remove the package
rm "$deb"
