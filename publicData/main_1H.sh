#!/bin/bash

script_dir=$(dirname "$(readlink -f "$0")")
cd "$script_dir"

xz -d *.xz
python3 openInterest.py >> openInterest.log
python3 priceLimit.py >> priceLimit.log
xz -z *.db