import json
import warnings
from datetime import timedelta
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt

warnings.filterwarnings('ignore')
pd.set_option('display.max_columns', None)

# Load data from JSON file
with open("corporate-announcements.json") as file:
    data = json.load(file)

# Create DataFrame
df = pd.DataFrame(data)

# Extract relevant columns and convert 'an_dt' to datetime
df['an_dt'] = pd.to_datetime(df['an_dt'])

# Filter announcements to include only those occurring after market close and before market open
start_time = pd.to_datetime('15:10:00').time()
end_time = pd.to_datetime('9:10:00').time()
df = df[(df['an_dt'].dt.time > start_time) | (df['an_dt'].dt.time < end_time)]

# Function to retrieve next day's returns
def get_next_day_returns(row):
    symbol = row['symbol'] + '.NS'
    timestamp = row['an_dt']
    t_date = timestamp + timedelta(days=1) if timestamp.time() > start_time else timestamp
    t7_date = t_date + timedelta(days=7)

    try:
        prices = yf.download(tickers=[symbol], interval="1d", start=t_date, end=t7_date, rounding=True, progress=False)
        next_day = prices.iloc[0]
        adj_close = next_day['Adj Close']
        open_ = next_day['Open']
        intraday_return = (adj_close - open_) * 100 / open_
    except IndexError:
        adj_close = 0
        open_ = 0
        intraday_return = 0

    return pd.Series([t_date, open_, adj_close, intraday_return],
                     index=['t_date', 'open', 'adj_close', 'intraday_return'])

# Apply function to DataFrame
df[['t_date', 'open', 'adj_close', 'intraday_return']] = df.apply(lambda row: get_next_day_returns(row), axis=1)

# Perform additional analysis
# 1. Visualizations
plt.figure(figsize=(10, 6))
plt.hist(df['intraday_return'], bins=20, color='skyblue', edgecolor='black')
plt.title('Distribution of Intraday Returns')
plt.xlabel('Intraday Return (%)')
plt.ylabel('Frequency')
plt.grid(True)
plt.show()

plt.figure(figsize=(10, 6))
plt.plot(df['an_dt'], df['intraday_return'], marker='o', linestyle='-')
plt.title('Intraday Returns Over Time')
plt.xlabel('Date')
plt.ylabel('Intraday Return (%)')
plt.grid(True)
plt.show()

# 2. Statistical Analysis
print("Summary Statistics of Intraday Returns:")
print(df['intraday_return'].describe())

df.to_csv('results.csv')
