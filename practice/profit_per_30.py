import pandas as pd
import pytz

#Load the CSV file
data = pd.read_csv('filtered_file.csv', parse_dates=['exit_time'])

#Convert "exit_time" from its current timezone to CST
data['exit_time'] = data['exit_time'].dt.tz_convert('America/Chicago')

#Group by 30-minute intervals starting at 8:30am CST
# We'll first set 'exit_time' as the index for resampling purposes
data.set_index('exit_time', inplace=True)
data = data.between_time('08:30', '23:59')  # Filter rows outside this time range

#calculate profit/loss
#Multiply net_pts by 2,000 and then sum for each interval
profits = data.resample('30T').apply(lambda x: sum(x['net_pts'] * 2000))

# 5. Display the results
print(profits)