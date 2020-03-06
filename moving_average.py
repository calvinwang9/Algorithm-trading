import pandas_datareader as pdr
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime

# TODO:
#- implement portfolio of stocks (tech)
#- different trading strategies
#- combining multiple trading strategies
#- using live data

# -------------------- data importing -------------------------
stock = 'IVV'
start_time = datetime.datetime(2000, 1, 1)
end_time = datetime.datetime(2020, 3, 1)
data = pdr.get_data_yahoo(stock, start=start_time, end=end_time)

# -------------- moving average algorithm ---------------------
short_window = 50
long_window = 200

signals = pd.DataFrame(index=data.index)
signals['price'] = data['Adj Close']
signals['signal'] = 0.0

signals['short_avg'] = data['Close'].rolling(window = short_window, min_periods = 1, center = False).mean()

signals['long_avg'] = data['Close'].rolling(window = long_window, min_periods = 1, center = False).mean()

signals['signal'][short_window:] = np.where(
        signals['short_avg'][short_window:] > signals['long_avg'][short_window:],
        1.0, 0.0)

signals['positions'] = signals['signal'].diff()

#print(signals)

# --------------- plotting the algorithm ---------------------

# Initialize the plot figure
fig = plt.figure(figsize=(13,10))

# Add a subplot and label for y-axis
ax1 = fig.add_subplot(111,  ylabel='Price in $')

# Plot the closing price
data['Close'].plot(ax=ax1, color='r', lw=2.)

# Plot the short and long moving averages
signals[['short_avg', 'long_avg']].plot(ax=ax1, lw=2.)

# Plot the buy signals
ax1.plot(signals.loc[signals.positions == 1.0].index, 
         signals.short_avg[signals.positions == 1.0],
         '^', markersize=10, color='m')
         
# Plot the sell signals
ax1.plot(signals.loc[signals.positions == -1.0].index, 
         signals.short_avg[signals.positions == -1.0],
         'v', markersize=10, color='k')
         
# Show the plot
plt.show()

# --------------- backtesting ---------------------
# Set the initial capital
initial_capital= float(100000.0)

# Create a DataFrame `positions`
positions = pd.DataFrame(index=signals.index).fillna(0.0)

# Buy a 100 shares
positions['sharePrice'] = 100*signals['signal']   
  
# Initialize the portfolio with value owned   
portfolio = positions.multiply(data['Adj Close'], axis=0)

# Store the difference in shares owned 
pos_diff = positions.diff()

# Add `holdings` to portfolio
portfolio['holdings'] = (positions.multiply(data['Adj Close'], axis=0)).sum(axis=1)

# Add `cash` to portfolio
portfolio['cash'] = initial_capital - (pos_diff.multiply(data['Adj Close'], axis=0)).sum(axis=1).cumsum()   

# Add `total` to portfolio
portfolio['total'] = portfolio['cash'] + portfolio['holdings']

# Add `returns` to portfolio
portfolio['returns'] = portfolio['total'].pct_change()

# Print the first lines of `portfolio`
#print(portfolio)

# Create a figure
fig = plt.figure(figsize=(13,10))

ax1 = fig.add_subplot(111, ylabel='Portfolio value in $')

# Plot the equity curve in dollars
portfolio['total'].plot(ax=ax1, lw=2.)

ax1.plot(portfolio.loc[signals.positions == 1.0].index, 
         portfolio.total[signals.positions == 1.0],
         '^', markersize=10, color='m')
ax1.plot(portfolio.loc[signals.positions == -1.0].index, 
         portfolio.total[signals.positions == -1.0],
         'v', markersize=10, color='k')

# Show the plot
plt.show()

# --------------- summary analysis ---------------------

#print(signals.loc[signals.positions == -1.0]['price'])
num_buy = len(signals.loc[signals.positions == 1.0])
num_sell = len(signals.loc[signals.positions == -1.0])
total_buy = sum(signals.loc[signals.positions == 1.0]['price'])
total_sell = sum(signals.loc[signals.positions == -1.0]['price'])

total_profit = total_sell - total_buy + (num_buy-num_sell)*signals['price'][-1]
print('\n\n---------- analysis -----------')
print('(all prices in USD, assume no transaction costs)')
print('years = ' + str(round((end_time-start_time).days/365, 2)))
print('trades made = ' + str(num_buy+num_sell))
print('current price = ' + str(signals['price'][-1]))
print('total profit = ' + str(round(total_profit, 2)))
print('baseline profit(hold) = ' + str(round(signals['price'][-1] - signals['price'][0], 2)))

print('\nportfolio profit = ' + str(round(portfolio['total'][-1] - initial_capital, 2)))

print('holdings = 100 shares bought at ' + str(signals['price'][0]) + ' now at ' + str(signals['price'][-1]))
print('baseline profit = ' + str(round(100*(signals['price'][-1]-signals['price'][0]), 2)))

summary = signals.loc[signals.positions == 1.0].append(signals.loc[signals.positions == -1.0]).sort_values(by=['Date'])


del summary['short_avg']
del summary['long_avg']
del summary['signal']

#print(summary)