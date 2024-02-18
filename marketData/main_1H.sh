#!/bin/bash

script_dir=$(dirname "$(readlink -f "$0")")
cd "$script_dir"

xz -d *.xz
python3 books.py >> books.log
xz -z *.db