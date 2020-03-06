import pandas_datareader as pdr
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime

# -------- simple momentum ------------
# - very basic momentum strategy
# - buy when stock has risen by a certain percentage
# - sell when stock has fallen by a certain percentage

# assumptions:
#   - no transaction costs or trading restrictions
#   - all prices in USD

# summary:
#   - very poor performance 
#   - overreaction to bullish/bearish conditions leads to bad trades
#   - higher sensitivities led to better performance than lower due less trading volume = lose less money 


# -------------------- data importing -------------------------
stock = 'IVV'
start_time = datetime.datetime(2010, 1, 1)
end_time = datetime.datetime(2019, 12, 26)
data = pdr.get_data_yahoo(stock, start=start_time, end=end_time)

# ---------------------- algorithm ----------------------------
sensitivity = 0.035
algo = pd.DataFrame(index=data.index)
algo['price'] = data['Adj Close']

algo['pct_change'] = algo['price'].pct_change()

algo['buy'] = np.where(algo['pct_change'] > sensitivity, 1, 0)
algo['sell'] = np.where(algo['pct_change'] < -sensitivity, 1, 0)


# ---------------------- plotting -----------------------------
fig = plt.figure(figsize=(13,10))
ax1 = fig.add_subplot(111,  ylabel='Price in $')

data['Adj Close'].plot(ax=ax1, color='r', lw=2.)

# Plot the buy signals
ax1.plot(algo.loc[algo.buy == 1].index, 
         algo.price[algo.buy == 1],
         '^', markersize=10, color='m')
         
# Plot the sell signals
ax1.plot(algo.loc[algo.sell == 1].index, 
         algo.price[algo.sell == 1],
         'v', markersize=10, color='k')
         
plt.show()

# ------------------ summary analysis -------------------------
num_buy = len(algo.loc[algo.buy == 1])
num_sell = len(algo.loc[algo.sell == 1])
total_buy = sum(algo.loc[algo.buy == 1]['price'])
total_sell = sum(algo.loc[algo.sell == 1]['price'])

#print(num_buy)
#print(num_sell)
#print(total_buy)
#print(total_sell)
print('\n\n')

# profit/loss from buying and selling action + outstanding share value
final_position = (total_sell - total_buy) + (num_buy - num_sell) * algo['price'][-1]
print('final position = ' + str(final_position))

# benchmark performance (buy and hold)
benchmark = algo['price'][-1] - algo['price'][0]
print('benchmark = ' + str(benchmark))