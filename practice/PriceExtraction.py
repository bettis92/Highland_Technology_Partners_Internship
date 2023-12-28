# sys allows us to specify "stderr" and "stdin" which we will go into later. csv 
# imports a library that gets us ready to do processes on csv files
import sys
import csv

#Since we were having trouble before, this prints "script started" to let us know 
#the script has started, but the next arguement specifies that the type of this print
#is "stderr". I learned when we are piping inputs and outputs forom bash to python
#the system is looking for sdtin(input) and stdout(output).
#the reson we specify "stderr" here is so its not included as input or output in the
#process
print("Script started", file=sys.stderr)

# This is DictReader is part of the csv library
# This reader treats each row as a separate dictionary where the keys are the 
# column names and the values are the column values
# "sys.stdin" is prepping this dict reader to receive the input, specifically the 
# input is the result of the first process in the shell script (101 rows from csv)
# which will be piped to this python script
reader = csv.DictReader(sys.stdin)

#This is another deactive print via "stderr" that says "ok we are reading the csv"
print("Read CSV data", file=sys.stderr)

# I added this line to specify that we are looking at the price column because
# That is not specifically visable with this process
print("price")

# This is saying for each dictionary(row) in reader(collection of dictionaries)
# print(dictionary['value for this key']) which is how you print dictionary values
# so for each dictionary in this collection of dicitonaries
# print current dictionaries value associated with key 'price'.
for row in reader:
    print(row['price'])

#this is just another deactive debugging script letting us know we are done.
print("Script finished", file=sys.stderr)

