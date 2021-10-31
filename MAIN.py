import matplotlib.pyplot as plt
import numpy as np
from pyarrow.feather import read_feather, write_feather
import tasklib
from trade import *

while 1:
    temp = input("Datenbank Datei\nz.B. btcusd.feather\n>>>")
    try:
        data = read_feather('./fdatasets/btcusd.feather')
        break
    except:
        print("Daten konnten nicht eingelesen werden, bitt versuchen Sie es erneut!\n\n\n")

while 1:
    temp = input(f"\nZeitraum\n(wie weit zurück von neuestem Punkt in Min.)\nmax. {len(data)}\n>>>")
    try:
        time = data['timestamp'][-int(temp):].reset_index(drop=True)
        close = data['close'][-int(temp):].reset_index(drop=True)
        break
    except:
        print("Daten konnten nicht eingeteilt werden, bitte versuchen Sie es erneut!\n\n\n")

def evaluate(macd_standard_config):
    return macd_standard_config


tradingObj = TradeCurrency(test_tradescheme(), evaluate, interval_manual=60)
print('\n\n\n')
for i in range(len(time)):
    if i % 10000 == 0:
        print(f'{i} of {len(time)} done!')
    tradingObj.trade(time[i], close[i])

d = tradingObj.trade_scheme['macd_standard_config']['values']
volume_total = [v['volume_total'] for v in tradingObj.trade_scheme['macd_standard_config']['trades']]
d = tasklib.even_size(d)
macd = np.array(d['macd'])
time = time[:len(macd)]
close = close[:len(macd)]
signal = np.array(d['signal'])
histogram = np.array(d['histogram'])

while len(volume_total) < len(time):
    volume_total.insert(0, volume_total[0])
    
fig, ax = plt.subplots(3)
ax[0].plot(time, close)
ax[0].set_title('Close')
ax[1].plot(time, macd)
ax[1].plot(time, signal)
ax[1].fill_between(time, 0, histogram, where=(np.where(histogram < 0, True, False)), color='r')
ax[1].fill_between(time, 0, histogram, where=(np.where(histogram < 0, False, True)), color='g')
ax[2].plot(time, volume_total)
plt.gcf().autofmt_xdate()
plt.show()
