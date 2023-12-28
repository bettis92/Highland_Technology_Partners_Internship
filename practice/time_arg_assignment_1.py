import csv
from datetime import datetime, timedelta
import sys

inputfile = sys.argv[1] #take argument 1 from command line input as a string
interval_minutes = int(sys.argv[2]) #take argument 2 from command line input then turn into an integer.

with open(inputfile, 'r') as f:
    csvreader = csv.reader(f)
    next(csvreader)  # skip the header

    current_count = 0
    total_prices = 0
    total_qty = 0
    min_price = 999999999999999
    max_price = -1
    interval_start_time = None

    for row in csvreader:
        current_time_ns = int(row[0]) #take current time in each row in nano second from
        current_time = datetime.fromtimestamp(current_time_ns / 1e9)  # Convert nanoseconds to seconds with /1e9, to get a standard unix epoch timestamp. convert that to date time.
        current_price = int(row[8])
        current_qty = int(row[9])

        if current_count == 0:
            interval_start_time = current_time #grab the time at count 0 in the group and save it as the interval start time
            next_reset_time = interval_start_time + timedelta(minutes=interval_minutes) #set reset time by adding (input) minute time delta to the starting time

        current_count += 1
        total_prices += current_price
        total_qty += current_qty
        min_price = min(min_price, current_price)
        max_price = max(max_price, current_price)

        if current_time >= next_reset_time:
            avg_price = total_prices / current_count
            avg_price = round(avg_price)
            time_difference = current_time - interval_start_time #grab the exact time difference and show the user so they can see its close to input
            minutes_covered = time_difference.total_seconds() / 60 #time delta has no method to convert to minutes apparently so convert to total seconds and divide by 60
            minutes_covered = round(minutes_covered, 2) #in the print out it was giving a long float, so round to two digits for presentation.
            print(f'\nInterval start time: {interval_start_time}\nAvg price: {avg_price}\nMin price: {min_price}\nMax price: {max_price}\nTrades counted in this window: {current_count}\nShares in window: {total_qty}\nMinutes Covered In This Window: {minutes_covered:.2f}')
            current_count = 0
            total_prices = 0
            total_qty = 0
            min_price = 999999999999999
            max_price = -1
            
    if current_count > 0: #I kept this block to recycle this method for taking care of the final batch from the first method. 
        avg_price = total_prices / current_count
        avg_price = round(avg_price)
        time_difference = current_time - interval_start_time
        minutes_covered = time_difference.total_seconds() / 60
        minutes_covered = round(minutes_covered, 2)
        print(f'\nInterval start time: {interval_start_time}\nAvg price: {avg_price}\nMin price: {min_price}\nMax price: {max_price}\nTrades counted in this window: {current_count}\nShares in window: {total_qty}\nMinutes Covered In This Window: {minutes_covered:.2f}')

