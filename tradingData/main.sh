#!/bin/bash

script_dir=$(dirname "$(readlink -f "$0")")
cd "$script_dir"

xz -d *.xz
python3 takerVolume.py >> takerVolume.log
python3 loanRatio.py >> loanRatio.log
python3 longShortAccountRatio.py >>longShortAccountRatio.log
python3 openInterestVolume.py >> openInterestVolume.log
xz -z *.db