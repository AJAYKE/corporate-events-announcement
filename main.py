import json
import warnings
from datetime import timedelta

import pandas as pd
import yfinance as yf

warnings.filterwarnings('ignore')
pd.set_option('display.max_columns', None)

file = open("corporate-announcements.json")
data = json.load(file)

df = pd.DataFrame(data)
df = df[['symbol', 'sm_name', 'desc', 'an_dt']]
df['an_dt'] = pd.to_datetime((df['an_dt']))

# start_time = pd.to_datetime('15:15:00').time()
# end_time = pd.to_datetime('9:15:00').time()
# df = df[(df['an_dt'].dt.time > start_time) | (df['an_dt'].dt.time < end_time)]

failed_stocks = []

def get_next_four_days_data(row):
    symbol = row['symbol'] + '.NS'
    start_timestamp = row['an_dt']
    t7_date = start_timestamp + timedelta(days=4)

    try:
        prices = yf.download(tickers=[symbol], interval="15m", start=start_timestamp, end=t7_date, rounding=True, progress=False)
        # Datetime = prices['Datetime'].values
        open = prices['Open'].values
        high = prices['High'].values
        low = prices['Low'].values
        close = prices['Close'].values
        adj_close = prices['Adj Close'].values
        volume = prices['Volume'].values
    except Exception as e:
        failed_stocks.append(row['symbol'])

    return pd.Series([ open, high, low, close, adj_close, volume],
                     index=['open', 'high', 'low', 'close', 'adj_close', 'volume'])

sample_df = df.head(3)

sample_df[['open', 'high', 'low', 'close', 'adj_close', 'volume']] = sample_df.apply(get_next_four_days_data, axis=1)

sample_df.to_csv('final_results.csv')
