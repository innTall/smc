def select_high_tf(candles: dict) -> dict:
    """
    Input: {symbol: {tf1: candle1, tf2: candle2, ...}}
    Output: selected candle dict with highest TF priority
    """
    priority = ["4h", "1h", "15m"]
    symbol = list(candles.keys())[0]
    tf_candles = candles[symbol]

    for tf in priority:
        if tf_candles.get(tf):
            return {"symbol": symbol, "interval": tf, **tf_candles[tf]}
    return None
