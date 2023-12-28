#!/bin/bash
#This is the same as print_itch shell file in the same directory, except its written to take an arguement for the file name as the first parameter after calling the .sh name.
#This makes it so we could use this script on any other similarly formatted CSV where we would want to isolate row 9.

File=$1

awk -F, 'NR <= 101 {print $9}' "$File"