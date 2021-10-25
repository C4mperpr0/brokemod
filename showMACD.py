from macd import macd
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
from pyarrow.feather import read_feather, write_feather
import tasklib

data = read_feather('./fdatasets/adausd.feather')
print(len(data))

time = data['timestamp'][-250000:]#[::1440]
close = data['close'][-250000:]
#close = tasklib.change_steps(close)
time = time[-len(close):]


r = macd(close, smoothing_factor=2, step_seconds=60, evenSize=True)
macd = np.array(r['macd'])
signal = np.array(r['signal'])
histogram = np.array(r['histogram'])


fig, ax = plt.subplots(2)
ax[0].plot(time, close)
#ax[0].set_title('Close')
ax[1].plot(time, macd)
ax[1].plot(time, signal)
ax[1].fill_between(time, 0, histogram, where=(np.where(histogram < 0, True, False)), color='r')
ax[1].fill_between(time, 0, histogram, where=(np.where(histogram < 0, False, True)), color='g')
plt.show()
