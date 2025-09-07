import requests
import time
import logging

APIURL = "https://open-api.bingx.com/openApi/swap/v3/quote/klines"
logger = logging.getLogger("smc")

def _normalize_symbol(symbol: str) -> str:
    # BingX uses dash format, e.g. BTC-USDT
    return symbol.replace("USDT", "-USDT")

def get_last_confirmed_candle(symbol: str, interval: str) -> dict:
    params = {"symbol": _normalize_symbol(symbol), "interval": interval, "limit": 3}
    logger.debug(f"Fetching last confirmed candle: {params}")
    response = requests.get(APIURL, params=params)
    response.raise_for_status()
    data = response.json()

    # Handle dict or list
    if isinstance(data, dict):
        candles = data.get("data", [])
    elif isinstance(data, list):
        candles = data
    else:
        raise ValueError("Unexpected response format")

    if len(candles) < 2:
        raise ValueError("Not enough candles returned")

    c = candles[-2]  # penultimate = last confirmed

    # Handle dict or list candle format
    if isinstance(c, dict):
        timestamp = int(c.get("time") or c.get("openTime"))
        close = float(c["close"])
    else:  # list format
        timestamp = int(c[0])
        close = float(c[4])

    return {"symbol": symbol, "interval": interval, "timestamp": timestamp, "close": close}
    
def get_last_candles(symbol: str, interval: str, limit: int = 10) -> list:
    params = {"symbol": _normalize_symbol(symbol), "interval": interval, "limit": limit}
    response = requests.get(APIURL, params=params)
    response.raise_for_status()
    data = response.json()

    if isinstance(data, dict):
        candles = data.get("data", [])
    elif isinstance(data, list):
        candles = data
    else:
        raise ValueError("Unexpected response format")

    result = []
    for c in candles:
        if isinstance(c, dict):
            result.append({
                "openTime": int(c.get("openTime") or c.get("time")),
                "open": float(c["open"]),
                "high": float(c["high"]),
                "low": float(c["low"]),
                "close": float(c["close"]),
                "volume": float(c["volume"]),
                "closeTime": int(c.get("closeTime") or c.get("time")),
            })
        else:  # list format
            result.append({
                "openTime": int(c[0]),
                "open": float(c[1]),
                "high": float(c[2]),
                "low": float(c[3]),
                "close": float(c[4]),
                "volume": float(c[5]),
                "closeTime": int(c[6]),
            })
    return result