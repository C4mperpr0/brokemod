from macd import macd

def test_tradescheme():
    return {'macd_standard_config': {'method': 'macd', 'args': {'fast_ema_time': 12,
                                                                'slow_ema_time': 26,
                                                                'signal_time': 9,
                                                                'smoothing_factor': 2}}}

# trades values: index timestamp action(sell/buy) amount amount_usd total_amount total_amount_usd

class TradeCurrency:
    def __init__(self, trade_scheme, evaluate, timestamp=[], values=[], volume=100, interval_manual=None, interval_warn=False):
        self.interval_warn = interval_warn
        self.trade_scheme = trade_scheme
        self.evaluate = evaluate
        self.timestamp = timestamp
        self.values = values
        self.volume = volume

        # check interval
        if interval_manual is None:
            self.interval = (timestamp[0] - timestamp[1]).total_seconds()
            if self.interval_warn:
                for i in range(1, len(timestamp)):
                    if timestamp[i] - timestamp[i - 1] != self.interval:
                        raise Exception(f"Time interval must be consistent, auto-detected {self.interval} seconds.")
        else:
            self.interval = interval_manual

    def trade(self, timestamp, close):
        if self.interval_warn:
            if not self.timestamp == [] and not (timestamp - self.timestamp[-1]).total_seconds() == self.interval:
                raise Exception(f"Time interval must be consistent, given {self.interval} seconds but also {(timestamp - self.timestamp[-1]).total_seconds()}")
        self.values.append(close)
        self.timestamp.append(timestamp)

        for indicator_config in self.trade_scheme:
            if self.trade_scheme[indicator_config]['method'] == 'macd':
                #print(self.trade_scheme[indicator_config])
                self.trade_scheme[indicator_config]['values'] = macd(self.values, step_seconds=self.interval,
                                                                     progress=self.trade_scheme[indicator_config]['values'] if 'values' in self.trade_scheme[indicator_config].keys() else None,
                                                                     **self.trade_scheme[indicator_config]['args'])

        # example evaluation method
        # works only for trading scheme with "macd_standard_config" (type macd)
        if self.trade_scheme[indicator_config]['values'] is None:
            return

        if 'trades' not in self.trade_scheme['macd_standard_config']:
            self.trade_scheme['macd_standard_config']['trades'] = []
        if 'trade_status' not in self.trade_scheme['macd_standard_config']:
            self.trade_scheme['macd_standard_config']['trade_status'] = {'volume_crypto': 0, 'volume_usd': 0}

        impulse = 'sell' if self.trade_scheme[indicator_config]['values']['histogram'][-1] <= 0 else 'buy'
        if impulse == 'sell' and self.trade_scheme['macd_standard_config']['trade_status']['volume_crypto'] == 0:
            impulse = 'keep'
        elif impulse == 'buy' and self.trade_scheme['macd_standard_config']['trade_status']['volume_crypto'] > 0:
            impulse = 'keep'

        if impulse == 'keep':
            self.trade_scheme['macd_standard_config']['trade_status'] = {'volume_crypto': self.trade_scheme['macd_standard_config']['trade_status']['volume_crypto'],
                                                                         'volume_usd': self.trade_scheme['macd_standard_config']['trade_status']['volume_crypto'] * close}
            self.trade_scheme['macd_standard_config']['trades'].append({'timestamp': timestamp,
                                                                        'value': close,
                                                                        'volume_crypto': self.trade_scheme['macd_standard_config']['trade_status']['volume_crypto'],
                                                                        'volume_usd': self.trade_scheme['macd_standard_config']['trade_status']['volume_usd'],
                                                                        'volume_uninvested': self.volume,
                                                                        'volume_total': self.volume + self.trade_scheme['macd_standard_config']['trade_status']['volume_usd'],
                                                                        'impulse': impulse,
                                                                        'histogram': self.trade_scheme[indicator_config]['values']['histogram'][-1]})
        elif impulse == 'buy':
            self.trade_scheme['macd_standard_config']['trade_status'] = {'volume_crypto': self.volume / close,
                                                                         'volume_usd': self.volume}
            self.trade_scheme['macd_standard_config']['trades'].append({'timestamp': timestamp,
                                                                        'value': close,
                                                                        'volume_crypto': self.volume / close,
                                                                        'volume_usd': self.volume,
                                                                        'volume_uninvested': 0,
                                                                        'volume_total': self.volume,
                                                                        'impulse': impulse,
                                                                        'histogram': self.trade_scheme[indicator_config]['values']['histogram'][-1]})
            self.volume = 0
        elif impulse == 'sell':
            self.volume += self.trade_scheme['macd_standard_config']['trade_status']['volume_crypto'] * close
            self.trade_scheme['macd_standard_config']['trade_status'] = {'volume_crypto': 0, 'volume_usd': 0}
            self.trade_scheme['macd_standard_config']['trades'].append({'timestamp': timestamp,
                                                                        'value': close,
                                                                        'volume_crypto': 0,
                                                                        'volume_usd': 0,
                                                                        'volume_uninvested': self.volume,
                                                                        'volume_total': self.volume,
                                                                        'impulse': impulse,
                                                                        'histogram': self.trade_scheme[indicator_config]['values']['histogram'][-1]})









