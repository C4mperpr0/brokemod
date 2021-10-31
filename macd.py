import numpy as np

def macd(close, fast_ema_time=12, slow_ema_time=26, signal_time=9, smoothing_factor=2, step_seconds=60, progress=None):
    # https://www.investopedia.com/terms/e/ema.asp

    # als ema times in days
    # smoothingfactor for days, if steps are not 1d factor will be automaticly ajusted (reference is step_seconds)

    # check if enough values are given
    if len(close) <= slow_ema_time + signal_time:
        return None
    #progress = None

    smoothing_factor *= (step_seconds / 86400)

    fast_ema_factor = smoothing_factor / (fast_ema_time + 1)
    slow_ema_factor = smoothing_factor / (slow_ema_time + 1)
    signal_factor = smoothing_factor / (signal_time + 1)

    fast_ema = [np.average(close[:fast_ema_time])] if progress is None else progress['fast_ema']
    for i in close[fast_ema_time + len(fast_ema) - 1:]:
        fast_ema.append((i - fast_ema[-1]) * fast_ema_factor + fast_ema[-1])

    slow_ema = [np.average(close[:slow_ema_time])] if progress is None else progress['slow_ema']
    for i in close[slow_ema_time + len(slow_ema) - 1:]:
        slow_ema.append((i - slow_ema[-1]) * slow_ema_factor + slow_ema[-1])

    macd = [] if progress is None else progress['macd']
    for i in range(len(macd), len(slow_ema)):
        macd.append(fast_ema[i + (slow_ema_time - fast_ema_time)] - slow_ema[i])

    signal = [np.average(macd[:signal_time])] if progress is None else progress['signal']
    for i in macd[signal_time+len(signal) - 1:]:
        signal.append((i - signal[-1]) * signal_factor + signal[-1])

    histogram = [] if progress is None else progress['histogram']
    for i in range(len(histogram), len(signal)):
        histogram.append(macd[i + signal_time - 1] - signal[i])



    return {'fast_ema': fast_ema, 'slow_ema': slow_ema, 'macd': macd, 'signal': signal, 'histogram': histogram,}
