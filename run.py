from macd import macd
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
from pyarrow.feather import read_feather, write_feather
import tasklib
from trade import *

data = read_feather('./fdatasets/btcusd.feather')

time = data['timestamp'][-250000:].reset_index(drop=True)  #[::1440]
close = data['close'][-250000:].reset_index(drop=True)
#close = tasklib.change_steps(close)
#time = time[-len(close):]

def evaluate(macd_standard_config):
    #print(macd_standard_config['histogram'][-1])
    return None


tradingObj = TradeCurrency(test_tradescheme(), evaluate, interval_manual=60)
for i in range(25000):
    if i % 100 == 0:
        print(i)
    r = tradingObj.trade(time[i], close[i])

macd = np.array(r['macd_standard_config']['macd'])
signal = np.array(r['macd_standard_config']['signal'])
histogram = np.array(r['macd_standard_config']['histogram'])
time = time[:len(macd)]
close = close[:len(macd)]

fig, ax = plt.subplots(2)
ax[0].plot(time, close)
#ax[0].set_title('Close')
ax[1].plot(time, macd)
ax[1].plot(time, signal)
ax[1].fill_between(time, 0, histogram, where=(np.where(histogram < 0, True, False)), color='r')
ax[1].fill_between(time, 0, histogram, where=(np.where(histogram < 0, False, True)), color='g')
plt.show()
