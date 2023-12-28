#!/bin/bash 

#this is awk text editor utility. "-F," sets the field or the divider as every time there is a comma. The next arguement in '' means Number of Records NR which is a built in 
#variable in awk less than or equal to 101 (because i want to include the header price title, then 100 values for price) print the 9th field. Then it does this for the CSV
#file in the same directory xnas-itch
awk -F, 'NR <= 101 {print $9}' xnas-itch-20220103.trades.csv