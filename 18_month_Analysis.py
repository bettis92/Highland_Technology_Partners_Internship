import pandas as pd
import pytz
import argparse

# Initialize argument parser
parser = argparse.ArgumentParser(description="Analyze trading data.")
parser.add_argument("file_path", help="Path to the CSV file containing trading data.")
parser.add_argument("time_interval", help="Time interval for data resampling. E.g., '30T' for 30 minutes.")
parser.add_argument("qty_per_trade", type=int, help="Quantity per trade.")
parser.add_argument("point_value", type=int, help="Point value.")


# Parse arguments
args = parser.parse_args()

# # Load the CSV file without headers and assign column names

data = pd.read_csv(args.file_path, header=None, names=["exit_time", "col2", "net_pts", "col4", "col5"])
# data['exit_time'] = pd.to_datetime(data['exit_time'])
def custom_parser(dt_str):
    try:
        return pd.to_datetime(dt_str, format='%Y-%m-%d %H:%M:%S.%f%z')
    except ValueError:
        return pd.to_datetime(dt_str, format='%Y-%m-%d %H:%M:%S%z')

data['exit_time'] = data['exit_time'].apply(custom_parser)



# Extract the first and last day for later summary
start_day = data['exit_time'].min().strftime('%Y-%m-%d')
end_day = data['exit_time'].max().strftime('%Y-%m-%d')

# Extract the number of unique dates
total_trading_days = data['exit_time'].dt.date.nunique()

Total_sum_net_points = data['net_pts'].sum()

# Convert the exit_time to CST
data['exit_time'] = data['exit_time'].dt.tz_convert('America/Chicago')

# Set the exit time as the index
data.set_index('exit_time', inplace=True)

# Filter only times where the market is open after CST conversion.
start_time = '08:30:00'
end_time = '15:30:00'

data = data[(data.index.time >= pd.to_datetime(start_time).time()) & 
            (data.index.time < pd.to_datetime(end_time).time())]

# Multiply by the specified quantity per trade and point value to get the profit.
data['profit'] = data['net_pts'] * args.qty_per_trade * args.point_value

Total_sum_net_profit = data['profit'].sum()

# Resample the data into bins at the specified time interval
data_resampled = data.resample(args.time_interval)
sum_net_profit = data_resampled['profit'].sum()
sum_net_pts = data_resampled['net_pts'].sum()
std_net_pts = data_resampled['net_pts'].std()
min_net_pts = data_resampled['net_pts'].min()
max_net_pts = data_resampled['net_pts'].max()

resampled_df = pd.DataFrame({
    'Sum Net Profit': sum_net_profit,
    'Sum Net Points': sum_net_pts,
    'Std Net Pts': std_net_pts,
    'Min Net Pts': min_net_pts,
    'Max Net Pts': max_net_pts
})

resampled_df = resampled_df[~(pd.isna(resampled_df['Min Net Pts']) & pd.isna(resampled_df['Max Net Pts']))]

# Group by 30-minute time windows (or whatever the interval is) and calculate the mean, sum, etc. for each series using the resampled_df
average_profits_grouped = resampled_df['Sum Net Profit'].groupby(resampled_df.index.time).mean()
avg_net_pts_grouped = resampled_df['Sum Net Points'].groupby(resampled_df.index.time).mean()
std_net_pts_grouped = resampled_df['Std Net Pts'].groupby(resampled_df.index.time).mean()
min_net_pts_grouped = resampled_df['Min Net Pts'].groupby(resampled_df.index.time).mean()
max_net_pts_grouped = resampled_df['Max Net Pts'].groupby(resampled_df.index.time).mean()
sum_net_profits_grouped = resampled_df['Sum Net Profit'].groupby(resampled_df.index.time).sum()
sum_net_pts_grouped = resampled_df['Sum Net Points'].groupby(resampled_df.index.time).sum()


# Create a new data frame to hold all the series
result_df = pd.DataFrame({
    'Avg Profits': average_profits_grouped,
    'Avg Net Points': avg_net_pts_grouped,
    'Standard Deviation': std_net_pts_grouped,
    'Minimum Net Points': min_net_pts_grouped,
    'Maximum Net Points': max_net_pts_grouped,
    'Total Window Sum Profits' : sum_net_profits_grouped,
    'Total Window Sum Net Points':sum_net_pts_grouped
})

# Adjust the time window for the grouped data
start_time = pd.to_datetime('08:30').time()
end_time = pd.to_datetime('15:30').time()

result_df = result_df[(result_df.index >= start_time) & 
                      (result_df.index < end_time)]


print(result_df)
print(f"The data analyzed is from {start_day} to {end_day}")
print(f"The total net profits for {round(Total_sum_net_profit,2)}")
print(f"The total net points for {round(Total_sum_net_points,2)}")
print(f"Analysis covered {start_day} to {end_day}, which is {total_trading_days} total trading days.")



































# import pandas as pd
# import pytz
# import argparse

# # Initialize argument parser
# parser = argparse.ArgumentParser(description="Analyze trading data.")
# parser.add_argument("file_path", help="Path to the CSV file containing trading data.")
# parser.add_argument("time_interval", help="Time interval for data resampling. E.g., '30T' for 30 minutes.")
# parser.add_argument("qty_per_trade", type=int, help="Quantity per trade.")
# parser.add_argument("point_value", type=int, help="Point value.")


# # Parse arguments
# args = parser.parse_args()

# # # Load the CSV file without headers and assign column names

# data = pd.read_csv(args.file_path, header=None, names=["exit_time", "col2", "net_pts", "col4", "col5"])
# # data['exit_time'] = pd.to_datetime(data['exit_time'])
# def custom_parser(dt_str):
#     try:
#         return pd.to_datetime(dt_str, format='%Y-%m-%d %H:%M:%S.%f%z')
#     except ValueError:
#         return pd.to_datetime(dt_str, format='%Y-%m-%d %H:%M:%S%z')

# data['exit_time'] = data['exit_time'].apply(custom_parser)



# # Extract the first and last day for later summary
# start_day = data['exit_time'].min().strftime('%Y-%m-%d')
# end_day = data['exit_time'].max().strftime('%Y-%m-%d')

# # Extract the number of unique dates
# total_trading_days = data['exit_time'].dt.date.nunique()

# Total_sum_net_points = data['net_pts'].sum()

# # Convert the exit_time to CST
# data['exit_time'] = data['exit_time'].dt.tz_convert('America/Chicago')

# # Set the exit time as the index
# data.set_index('exit_time', inplace=True)

# # Filter only times where the market is open after CST conversion.
# start_time = '08:30:00'
# end_time = '15:30:00'

# data = data[(data.index.time >= pd.to_datetime(start_time).time()) & 
#             (data.index.time < pd.to_datetime(end_time).time())]

# # Multiply by the specified quantity per trade and point value to get the profit.
# data['profit'] = data['net_pts'] * args.qty_per_trade * args.point_value

# Total_sum_net_profit = data['profit'].sum()

# # Resample the data into bins at the specified time interval
# data_resampled = data.resample(args.time_interval)
# sum_net_profit = data_resampled['profit'].sum()
# sum_net_pts = data_resampled['net_pts'].sum()
# std_net_pts = data_resampled['net_pts'].std()
# min_net_pts = data_resampled['net_pts'].min()
# max_net_pts = data_resampled['net_pts'].max()

# # Remove zero values
# sum_net_profit = sum_net_profit[sum_net_profit != 0]
# sum_net_pts = sum_net_pts[sum_net_pts != 0]
# std_net_pts = std_net_pts[std_net_pts != 0]
# min_net_pts = min_net_pts[min_net_pts != 0]
# max_net_pts = max_net_pts[max_net_pts != 0]

# # Group by 30-minute time windows and calculate the mean for each series
# average_profits_grouped = sum_net_profit.groupby(sum_net_profit.index.time).mean()
# avg_net_pts_grouped = sum_net_pts.groupby(sum_net_pts.index.time).mean()
# std_net_pts_grouped = std_net_pts.groupby(std_net_pts.index.time).mean()
# min_net_pts_grouped = min_net_pts.groupby(min_net_pts.index.time).mean()
# max_net_pts_grouped = max_net_pts.groupby(max_net_pts.index.time).mean()
# sum_net_profits_grouped = sum_net_profit.groupby(sum_net_profit.index.time).sum()
# sum_net_pts_grouped = sum_net_pts.groupby(sum_net_pts.index.time).sum()

# # Create a new data frame to hold all the series
# result_df = pd.DataFrame({
#     'Avg Profits': average_profits_grouped,
#     'Avg Net Points': avg_net_pts_grouped,
#     'Standard Deviation': std_net_pts_grouped,
#     'Minimum Net Points': min_net_pts_grouped,
#     'Maximum Net Points': max_net_pts_grouped,
#     'Total Window Sum Profits' : sum_net_profits_grouped,
#     'Total Window Sum Net Points':sum_net_pts_grouped
# })

# # Adjust the time window for the grouped data
# start_time = pd.to_datetime('08:30').time()
# end_time = pd.to_datetime('15:30').time()

# result_df = result_df[(result_df.index >= start_time) & 
#                       (result_df.index < end_time)]


# print(result_df)
# print(f"The data analyzed is from {start_day} to {end_day}")
# print(f"The total net profits for {round(Total_sum_net_profit,2)}")
# print(f"The total net points for {round(Total_sum_net_points,2)}")
# print(f"Analysis covered {start_day} to {end_day}, which is {total_trading_days} total trading days.")
