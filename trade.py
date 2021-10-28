from macd import macd


def test_tradescheme():
    return {'macd_standard_config': {'method': 'macd', 'args': {'fast_ema_time': 12,
                                                                'slow_ema_time': 26,
                                                                'signal_time': 9,
                                                                'smoothing_factor': 2}}}

# trades values: index timestamp action(sell/buy) amount amount_usd total_amount total_amount_usd

class TradeCurrency:
    def __init__(self, trade_scheme, evaluate, timestamp=[], values=[], trades=[], interval_manual=None, interval_warn=False):
        self.interval_warn = interval_warn
        self.trade_scheme = trade_scheme
        self.evaluate = evaluate
        self.timestamp = timestamp
        self.values = values

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

        r = {}

        for indicator_config in self.trade_scheme:
            if self.trade_scheme[indicator_config]['method'] == 'macd':
                indicator_values = macd(self.values, step_seconds=self.interval,
                                        progress=r[indicator_config] if indicator_config in r.keys() else None,
                                        evenSize=True,
                                        **self.trade_scheme[indicator_config]['args'])
            r[indicator_config] = indicator_values

        return r
        # dont forget to remove for evaluation algo.

        #if None in r.values():
        #    return None
        #else:
        #    eval = self.evaluate(**r)


