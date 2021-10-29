from macd import macd
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
from pyarrow.feather import read_feather, write_feather
import tasklib
from trade import *

data = read_feather('./fdatasets/btcusd.feather')

time = data['timestamp'][-2500000:].reset_index(drop=True)  #[::1440]
close = data['close'][-2500000:].reset_index(drop=True)
#close = tasklib.change_steps(close)
#time = time[-len(close):]

def evaluate(macd_standard_config):
    #print(macd_standard_config['histogram'][-1])
    return macd_standard_config


tradingObj = TradeCurrency(test_tradescheme(), evaluate, interval_manual=60)
for i in range(0, 5000, 1):
    if i % 5000 == 0:
        print(i)
    tradingObj.trade(time[i], close[i])

print(tradingObj.trade_scheme['macd_standard_config']['values'].keys())
d = tradingObj.trade_scheme['macd_standard_config']['values']
macd = np.array(d['macd'])
time = time[:len(macd)]
close = close[:len(macd)]
signal = np.array(d['signal'])
histogram = np.array(d['histogram'])

fig, ax = plt.subplots(2)
ax[0].plot(time, close)
#ax[0].set_title('Close')
ax[1].plot(time, macd)
ax[1].plot(time, signal)
ax[1].fill_between(time, 0, histogram, where=(np.where(histogram < 0, True, False)), color='r')
ax[1].fill_between(time, 0, histogram, where=(np.where(histogram < 0, False, True)), color='g')
plt.show()
