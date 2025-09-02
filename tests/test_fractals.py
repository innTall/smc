import sys, os, json, requests
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.fractals import FractalDetector, filter_normal_fractals

def load_config():
    with open("config.json", "r") as f:
        return json.load(f)

def fetch_candles(symbol: str, interval: str, limit: int = 200):
    """
    Fetch historical candles from BingX Swap v3 public endpoint (API mode).
    """
    url = "https://open-api.bingx.com/openApi/swap/v3/quote/klines"
    params = {
        "symbol": symbol.replace("USDT", "-USDT"),
        "interval": interval,
        "limit": limit
    }

    r = requests.get(url, params=params)
    r.raise_for_status()
    data = r.json()

    if data.get("code") != 0:
        raise RuntimeError(f"BingX API error: {data}")

    candles = []
    for k in data["data"]:
        candles.append({
            "time": int(k["time"]),
            "open": float(k["open"]),
            "high": float(k["high"]),
            "low": float(k["low"]),
            "close": float(k["close"]),
            "volume": float(k["volume"]),
            "is_closed": True
        })
    return candles

def run_fractal_test():
    config = load_config()
    config["source"] = "api"  # force API mode for tests

    symbol = config["symbols"][0]
    interval = config["intervals"][0]
    limit = config["history_limit"]
    window = config["fractal_window"]
    debug = config.get("fractal_debug", False)

    print(f"[TEST] Source = {config['source'].upper()}")
    print(f"[TEST] Loading {limit} candles for {symbol} {interval} ...")

    candles = fetch_candles(symbol, interval, limit)
    print(f"[TEST] Got {len(candles)} candles")

    detector = FractalDetector(window=window)
    fractals = detector.detect(candles)

    if debug:
        print(f"[DEBUG] {len(fractals)} total fractals detected (before filtering)")
        for f in fractals[:10]:
            print(f)
            
    normal_fractals = filter_normal_fractals(fractals, candles)

    print(f"[TEST] {len(normal_fractals)} normal fractals detected ✅")
    for f in normal_fractals[:10]:
        print(f)

    out_path = "tests/test.json"
    with open(out_path, "w") as f:
        json.dump(normal_fractals, f, indent=2)
    print(f"[TEST] Results written to {out_path}")

if __name__ == "__main__":
    run_fractal_test()

# python tests/test_fractals.py