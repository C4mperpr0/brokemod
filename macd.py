import numpy as np
from datetime import datetime

def macd(close, fast_ema_time=12, slow_ema_time=26, signal_time=9, smoothing_factor=2, step_seconds=60, evenSize=True):
    #https://www.investopedia.com/terms/e/ema.asp

    # als ema times in days
    # smoothingfactor for days, if steps are not 1d factor will be automaticly ajusted (reference is step_seconds)

    smoothing_factor = smoothing_factor * (step_seconds / (60*60*24))


    fast_ema_factor = smoothing_factor / (fast_ema_time + 1)
    slow_ema_factor = smoothing_factor / (slow_ema_time + 1)
    signal_factor = smoothing_factor / (signal_time + 1)
    fast_ema = []
    fast_ema.append(np.average(close[:fast_ema_time]))
    for i in close[fast_ema_time:]:
        fast_ema.append((i - fast_ema[-1]) * fast_ema_factor + fast_ema[-1])

    slow_ema = []
    slow_ema.append(np.average(close[:slow_ema_time]))
    for i in close[slow_ema_time:]:
        slow_ema.append((i - slow_ema[-1]) * slow_ema_factor + slow_ema[-1])

    macd = []
    for i in range(len(slow_ema)):
        macd.append(fast_ema[i + (slow_ema_time - fast_ema_time)] - slow_ema[i])

    signal = []
    signal.append(np.average(macd[:signal_time]))
    for i in macd[signal_time:]:
        signal.append((i - signal[-1]) * signal_factor + signal[-1])

    histogram = []
    for i in range(len(signal)):
        histogram.append(macd[i + signal_time - 1] - signal[i])

    if evenSize:
        for i in range((len(close) - len(macd))):
            macd.insert(0, macd[0])
        for i in range((len(close) - len(signal))):
            signal.insert(0, signal[0])
        for i in range((len(close) - len(histogram))):
            histogram.insert(0, histogram[0])

    return {'macd': macd, 'signal': signal, 'histogram': histogram}