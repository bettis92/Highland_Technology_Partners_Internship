#!/bin/bash

# Loop until valid input is provided
while true; do
    read -p "Please enter the csv file path: " inputfile
    read -p "Please enter an the amount of trades per analysis: " interval_count

    # Check if interval_count is a non-negative integer
    if ! [[ "$interval_count" =~ ^[0-9]+$ ]]; then
        echo "Invalid interval count. Please enter a non-negative integer."
        continue
    fi

    # Check if both inputs are provided and the input file exists
    if [[ -n "$inputfile" && -n "$interval_count" && -f "$inputfile" ]]; then
        # Call the Python script with the provided arguments
        python3 /home/betti/practice/arg_assignment_1.py "$inputfile" "$interval_count"
        exit 0
    else
        echo "Invalid input. Please provide a valid file path and interval count."
    fi
done
