from collections import defaultdict, deque

class CandleStore:
    def __init__(self, history_limit=200):
        self.history_limit = history_limit
        # dict[(symbol, interval)] -> deque of candles
        self.store = defaultdict(lambda: deque(maxlen=history_limit))

    def update(self, symbol, interval, candle):
        key = (symbol, interval)
        candles = self.store[key]

        if candle["is_closed"]:
            # append new closed candle
            candles.append(candle)
        else:
            # update last candle if exists, else append
            if candles:
                candles[-1] = candle
            else:
                candles.append(candle)

    def get(self, symbol, interval):
        """Return all candles for a symbol/interval"""
        return list(self.store[(symbol, interval)])

    def last(self, symbol, interval):
        """Return last candle or None"""
        candles = self.store[(symbol, interval)]
        return candles[-1] if candles else None

    def get_last_time(self, symbol, interval):
        candles = self.store[(symbol, interval)]
        return candles[-1]["time"] if candles else None
