#!/bin/bash

# Loop until valid input is provided
while true; do
    read -p "Please enter the csv file path: " inputfile
    read -p "Please enter an an amount of minutes per analysis read out: " interval_minutes

    # Check if interval_minutes is a non-negative integer
    if ! [[ "$interval_minutes" =~ ^[0-9]+$ ]]; then
        echo "Invalid input for minutes. Please enter a non-negative integer."
        continue
    fi

    # Check if both inputs are provided and the input file exists
    if [[ -n "$inputfile" && -n "$interval_minutes" && -f "$inputfile" ]]; then
        # Call the Python script with the provided arguments
        python3 /home/betti/practice/time_arg_assignment_1.py "$inputfile" "$interval_minutes"
        exit 0
    else
        echo "Invalid input. Please provide a valid file path and interval count."
    fi
done