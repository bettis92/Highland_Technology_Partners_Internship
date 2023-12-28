import csv
from datetime import datetime, timedelta
import sys

inputfile = "/home/betti/practice/xnas-itch-20220103.trades.csv"
interval_minutes = 15  

with open(inputfile, 'r') as f:
    csvreader = csv.reader(f)
    next(csvreader)  # skip the header

    current_count = 0
    total_prices = 0
    total_qty = 0
    min_price = 999999999999999
    max_price = -1
    interval_start_time = None
    first_time = True

    for row in csvreader:
        current_time_ns = int(row[0])
        current_time = datetime.fromtimestamp(current_time_ns / 1e9)  # Convert nanoseconds to seconds, then change that to date time
        if first_time:
            interval_start_time = current_time
            next_reset_time = interval_start_time + timedelta(minutes=interval_minutes)
            first_time = False
        current_price = int(row[8])
        current_qty = int(row[9])

        
        current_count += 1
        total_prices += current_price
        total_qty += current_qty
        min_price = min(min_price, current_price)
        max_price = max(max_price, current_price)

        if current_time >= next_reset_time:
            avg_price = total_prices / current_count
            avg_price = round(avg_price)
            time_difference = current_time - interval_start_time
            minutes_covered = time_difference.total_seconds() / 60
            minutes_covered = round(minutes_covered, 2)
            interval_start_time_formatted = interval_start_time.strftime("%Y-%m-%d %H:%M:%S")
            print(f'\nInterval start time: {interval_start_time_formatted}\nAvg price: {avg_price}\nMin price: {min_price}\nMax price: {max_price}\nTrades counted in this window: {current_count}\nShares in window: {total_qty}\nMinutes Covered In This Window: {minutes_covered}')
            current_count = 0
            total_prices = 0
            total_qty = 0
            min_price = 999999999999999
            max_price = -1
            interval_start_time = next_reset_time
            next_reset_time = next_reset_time + timedelta(minutes=interval_minutes)
            
    if current_count > 0:
        avg_price = total_prices / current_count
        avg_price = round(avg_price)
        time_difference = current_time - interval_start_time
        minutes_covered = time_difference.total_seconds() / 60
        minutes_covered = round(minutes_covered, 2)
        interval_start_time_formatted = interval_start_time.strftime("%Y-%m-%d %H:%M:%S")
        print(f'\nInterval start time: {interval_start_time_formatted}\nAvg price: {avg_price}\nMin price: {min_price}\nMax price: {max_price}\nTrades counted in this window: {current_count}\nShares in window: {total_qty}\nMinutes Covered In This Window: {minutes_covered}')

