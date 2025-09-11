from datetime import datetime

# --- Fake candle data (time, open, high, low, close) ---
candles = [
    {"time": 1, "open": 100, "high": 110, "low": 95, "close": 105},
    {"time": 2, "open": 106, "high": 115, "low": 104, "close": 110},
    {"time": 3, "open": 111, "high": 120, "low": 109, "close": 115},  # center
    {"time": 4, "open": 114, "high": 118, "low": 112, "close": 116},
    {"time": 5, "open": 117, "high": 119, "low": 115, "close": 121},  # breakout
]

window = 3
half = window // 2
eps = 0.0001

fractals = []

# --- Detect fractals ---
for i in range(half, len(candles) - half):
    center = candles[i]
    left = candles[i - half:i]
    right = candles[i + 1:i + 1 + half]

    if all(center["high"] > n["high"] + eps for n in left + right):
        fractals.append(
            {"type": "HFractal", "time": center["time"], "price": center["high"], "broken": False}
        )
    elif all(center["low"] < n["low"] - eps for n in left + right):
        fractals.append(
            {"type": "LFractal", "time": center["time"], "price": center["low"], "broken": False}
        )

print("Detected fractals:")
for f in fractals:
    print(f)

# --- Detect breakout (using high/low only) ---
for f in fractals:
    if f["type"] == "HFractal":
        for c in candles:
            if c["time"] > f["time"] and c["high"] > f["price"]:
                print(f"HBreak at {datetime.fromtimestamp(c['time'])}, high={c['high']}")
                f["broken"] = True
                break
    elif f["type"] == "LFractal":
        for c in candles:
            if c["time"] > f["time"] and c["low"] < f["price"]:
                print(f"LBreak at {datetime.fromtimestamp(c['time'])}, low={c['low']}")
                f["broken"] = True
                break

# --- Print normal (not broken) fractals ---
normal_fractals = [f for f in fractals if not f["broken"]]
print("\nNormal (not broken) fractals:")
for f in normal_fractals:
    print(f)

# python -m tests.test_fractal_break