import pandas_datareader as pdr
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
import math


# -------------------- data importing -------------------------
stock = 'IVV'
start_time = datetime.datetime(2010, 1, 1)
end_time = datetime.datetime(2019, 12, 26)
data = pdr.get_data_yahoo(stock, start=start_time, end=end_time)

# ---------------------- algorithm ----------------------------
period = 10
algo = pd.DataFrame(index=data.index)
algo['price'] = data['Adj Close']

algo['m_avg'] = algo['price'].rolling(window = period, min_periods = period).mean()

algo['deviation'] = algo['m_avg'] - algo['price']

algo['dev_sq'] = algo['deviation']**2

dev_sq_avg = algo['dev_sq'].mean()

stdev = math.sqrt(dev_sq_avg)

print(stdev)

# when short moving average is higher than long moving average
#algo['greater'] = np.where(algo['short_m_avg'] > algo['long_m_avg'], 1, 0)

# when there is a change in 'greater' we react with an action to buy (1) or sell (-1)
#algo['action'] = algo['greater'].diff()


#print(algo)


# ---------------------- plotting -----------------------------
fig = plt.figure(figsize=(13,10))
ax1 = fig.add_subplot(111,  ylabel='Price in $')

data['Adj Close'].plot(ax=ax1, color='r', lw=2.)

algo[['short_m_avg', 'long_m_avg']].plot(ax=ax1, lw=2.)

# Plot the buy signals
ax1.plot(algo.loc[algo.action == 1].index, 
         algo.price[algo.action == 1],
         '^', markersize=10, color='m')
         
# Plot the sell signals
ax1.plot(algo.loc[algo.action == -1].index, 
         algo.price[algo.action == -1],
         'v', markersize=10, color='k')
         
plt.show()

# ------------------ summary analysis -------------------------
num_buy = len(algo.loc[algo.action == 1])
num_sell = len(algo.loc[algo.action == -1])
total_buy = sum(algo.loc[algo.action == 1]['price'])
total_sell = sum(algo.loc[algo.action == -1]['price'])

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