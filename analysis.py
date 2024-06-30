import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV file into a DataFrame
df = pd.read_csv('results_seond.csv')

# Convert date columns to datetime format
df['t_date'] = pd.to_datetime(df['t_date'])

# Calculate intraday returns
df['intraday_returns'] = (df['open'] - df['adj_close'])


daily_investment = df.groupby(pd.Grouper(key='t_date', freq='D'))['open'].sum()
daily_returns = df.groupby(pd.Grouper(key='t_date', freq='D'))['intraday_returns'].sum()

monthly_investment = daily_investment.resample('M').sum()
monthly_returns = daily_returns.resample('M').sum()

yearly_investment = daily_investment.resample('Y').sum()
yearly_returns = daily_returns.resample('Y').sum()


cumulative_returns_daily = daily_returns.cumsum()
cumulative_returns_monthly = monthly_returns.cumsum()
cumulative_returns_yearly = yearly_returns.cumsum()

cumulative_returns_daily_percent = cumulative_returns_daily * 100
cumulative_returns_monthly_percent = cumulative_returns_monthly * 100
cumulative_returns_yearly_percent = cumulative_returns_yearly * 100


# Measure volatility of intraday returns
volatility = df.groupby(pd.Grouper(key='t_date', freq='M'))['intraday_returns'].std()

df['cumulative_returns'] = df['intraday_returns'].cumsum()

# Calculate drawdown
df['cum_max'] = df['cumulative_returns'].cummax()
df['drawdown'] = df['cumulative_returns'] - df['cum_max']

# Determine maximum drawdown
cumulative_returns = df['intraday_returns'].cumsum()
max_drawdown = (cumulative_returns - cumulative_returns.cummax()).min()

# Analyze trading frequency and duration
trade_frequency = df.groupby(pd.Grouper(key='t_date', freq='D')).size()
trade_duration = df.groupby(pd.Grouper(key='t_date', freq='D')).size().diff().fillna(0)



# Plot graphs for each metric
fig, axes = plt.subplots(nrows=3, ncols=2, figsize=(15, 10))

# Average Returns
axes[0, 0].plot(daily_returns, label='Daily Returns')
axes[0, 0].plot(monthly_returns, label='Monthly Returns')
axes[0, 0].plot(yearly_returns, label='Yearly Returns')
axes[0, 0].set_title('Average Returns')
axes[0, 0].legend()

# Volatility
axes[0, 1].plot(yearly_investment, label = 'avg daily investment in the year')
axes[0, 1].plot(yearly_returns, label = 'total yearwise returns' )
axes[0, 1].set_title('Avg daily investment in a year and total returns')
axes[0, 1].legend()

# cummulative returns
axes[1, 0].plot(cumulative_returns_monthly, label='Cumulative Monthly Returns')
axes[1, 0].plot(cumulative_returns_yearly, label='Cumulative Yearly Returns')
axes[1, 0].legend()
axes[1, 0].set_title('Cumulative Monthly and Yearly Returns')

#maximum drawdown
axes[1, 1].plot(monthly_investment, label = 'avg daily investment in the month')
axes[1, 1].plot(monthly_returns, label = 'total monthwise returns' )
axes[1, 1].set_title('Avg daily investment in a month and total returns')
axes[1, 1].legend()

# Trading Frequency
axes[2, 0].plot(daily_returns )
axes[2, 0].set_title('total daywise returns')

axes[2, 1].plot(daily_investment, label = 'avg daily investment')
axes[2, 1].set_title('Avg daily investment')
axes[2, 1].legend()
plt.tight_layout()
plt.show()


fig1, axes1 = plt.subplots(nrows=2, ncols=2, figsize=(15, 10))

axes1[0, 0].plot(daily_returns)
axes1[0, 0].set_title('Daily Returns in percentage')
axes1[0, 0].legend()

axes1[0, 1].plot(cumulative_returns_monthly)
axes1[0, 1].set_title('Monthly Returns in percentage')
axes1[0, 1].legend()

axes1[1, 0].plot(cumulative_returns_yearly)
axes1[1, 0].set_title('Yearly Returns in percentage')
axes1[1, 0].legend()

axes1[1, 1].plot(cumulative_returns_daily_percent , label='Cumulative Daily Returns')
axes1[1, 1].plot(cumulative_returns_monthly_percent, label='Cumulative Monthly Returns')
axes1[1, 1].plot(cumulative_returns_yearly_percent, label='Cumulative Yearly Returns')
axes1[1, 1].legend()
axes1[1, 1].set_title('Cumulative Monthly and Yearly Returns')

plt.tight_layout()
plt.show()




