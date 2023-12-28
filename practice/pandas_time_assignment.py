#import pandas and datetime to use these tools
import pandas as pd
from datetime import datetime, timedelta

#In pandas, "T" is minutes in time series attributes and parameters, so we specify the interval is 15T
inputfile = "/home/betti/practice/xnas-itch-20220103.trades.csv"
interval_minutes = '15T'  

# Read the CSV file
df = pd.read_csv(inputfile)

# Convert the timestamp column from nanoseconds to datetime, and create it as a new column on the right.
df['Interval_Start'] = pd.to_datetime(df.iloc[:, 0], unit='ns')

# Set the timestamp column as the index, and don't create a copy table with inplace=true, work off the existing table.
df.set_index('Interval_Start', inplace=True)

# Convert the price and quantity columns to int
df.iloc[:, [8, 9]] = df.iloc[:, [8, 9]].astype(int)

#adjust price column for results that are comprehended easier
df.iloc[:, 8] = df.iloc[:, 8] /1e9

# Define the aggregation functions that we want to do to each column of ints
aggregations = {
    df.columns[8]: ['mean', 'min', 'max'],  # Price info
    df.columns[9]: ['sum', 'count'],  # Quantity of shartes and trades
}
# Resample the DataFrame and apply aggregations
resampled_data = df.resample(interval_minutes).apply(aggregations) #sorting data into bins, apply aggregations to this new creation
resampled_data['mean_price'] = resampled_data.iloc[:, 0].round()
resampled_data['min_price'] = resampled_data.iloc[:, 1]
resampled_data['max_price'] = resampled_data.iloc[:, 2]
resampled_data['total_shares'] = resampled_data.iloc[:, 3]
resampled_data['total_trades'] = resampled_data.iloc[:, 4]
resampled_data['interval_End'] = (resampled_data.index + pd.Timedelta(minutes=15))

# Print the results
print(resampled_data[['interval_End', 'mean_price', 'min_price', 'max_price', 'total_shares', 'total_trades']])

