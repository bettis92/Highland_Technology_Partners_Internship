import csv
import sys

inputfile = sys.argv[1]
interval_count = int(sys.argv[2])

with open(inputfile, 'r') as f:
    csvreader = csv.reader(f)
    next(csvreader)  # skip the header

    current_count = 0
    num_trades = 0
    total_prices = 0
    total_qty = 0
    min_price = 999999999999999  # set to a large number
    max_price = -1
    interval_start_time = None  # Initialize variable to hold the start time

    for row in csvreader:
        current_price = int(row[8])
        current_qty = int(row[9])

        if current_count == 0:  # If starting a new interval, capture the start time
            interval_start_time = int(row[0])
            interval_start_price = int(row[8])

        current_count += 1
        num_trades += 1
        total_prices += current_price
        total_qty += current_qty
        min_price = min(min_price, current_price)
        max_price = max(max_price, current_price)

        if current_count >= interval_count:
            avg_price = round(total_prices / current_count)
            interval_end_price = int(row[8])
            interval_dif = interval_end_price - interval_start_price            
            print(f'Interval start time: {interval_start_time}\nTrades in this window: {current_count}\nShares in window: {total_qty}\nAvg price: {avg_price}\nMin price: {min_price}\nMax price: {max_price}\nFirst to last price diffference {interval_dif}\nTotal trades in file so far {num_trades}\n')
            current_count = 0
            total_prices = 0
            total_qty = 0
            min_price = 999999999999999
            max_price = -1

    # handle the final batch of records
    if current_count > 0:
        avg_price = round(total_prices / current_count)
        interval_end_price = int(row[8])
        interval_dif = interval_end_price - interval_start_price
        print(f'Interval start time: {interval_start_time}\nTrades in this window: {current_count}\nShares in window: {total_qty}\nAvg price: {avg_price}\nMin price: {min_price}\nMax price: {max_price}\nFirst to last price diffference {interval_dif}\nTotal trades in file {num_trades}\n')

