# Fractal Bot – Design & Roadmap

## Overview
**Exchange:** BingX  
**Market:** USDT-M perpetual futures (swap)  

The bot analyzes OHLC candles and detects fractals + breakouts using **confirmed closes** from REST.  
- **REST = source of truth** (deterministic, testable)  
- **WS = optional event trigger** (for faster reaction, not data validation)  

---

## Roadmap

### Step 0 – Preparation
- Keep repository clean and structured.
- Set up config, tests, and folder layout.

### Step 1 – Confirmed Closure via REST
- Deterministic retrieval of last confirmed candles.
- Test that REST always returns the confirmed close (not partial).
- **Output:** close values to Telegram.

### Step 2 – Fractal Detection
- Use confirmed candles only.
- Detect high/low fractals using a fixed window (odd length).
- Unit tests on synthetic data.

### Step 3 – Filtering Normal Fractals
- Exclude fractals already broken by later closes (or optionally wicks).
- Return only **normal (unbroken)** fractals.
- Unit tests on synthetic data.

### Step 4 – Breakout Detection
- Mark breakouts when confirmed closes cross fractal levels.
- Capture the candle that triggered the breakout.
- Unit tests: ensure correct breakout type (H/L, bullish/bearish).

### Step 5 – Signal Engine Integration
- Track active fractals and breakouts.
- Avoid duplicate signals.
- Send formatted signals to Telegram.
- Integration tests with simulated candles.

### Step 6 – WebSocket Trigger (Optional)
- Use WS to detect new candle opening faster.
- On WS event → fetch data from REST.
- WS = trigger, REST = truth.
- Integration tests with simulated WS events.

### Step 7 – End-to-End & Deployment
- Run full bot with `config.json`.
- Send real-time breakout signals to Telegram.
- Final integration tests.

---

## Important Principles
- Fractals and breakouts are **structural patterns**, not tick trades.
- **Confirmed candles only** (not wicks, not live WS).
- Accuracy > speed: wrong signals are worse than delayed signals.
- Test **each step independently** before integration.
- WS is an optimization layer, never a replacement for REST.

---

## Project Structure

smc/
├─ config.json # Symbols, intervals, API keys
├─ .env # Secret keys (Telegram, API)
├─ main.py # Entry point (Step 1)
│
├─ utils/
│ └─ rest_api.py # REST functions
│
├─ core/
│ └─ telegram_bot.py # Telegram sender
│
├─ modules/
│ ├─ fractals.py # Fractal detection
│ └─ fractal_break.py # Breakout detection
│
├─ tests/
│ ├─ test_rest_confirmed.py
│ ├─ test_fractals.py
│ ├─ test_fractal_filter.py
│ ├─ test_breakouts.py
│ ├─ test_signal_engine.py
│ ├─ test_ws_trigger.py
│ └─ test_integration.py
│
└─ archive/

markdown
Copy code

---

## Step 1 – REST Confirmed Closure

### Purpose
Get the **last confirmed candle** for each symbol/interval in `config.json` and send its closing price to Telegram.  

Confirmed = `candles[-2]` (since the last one may still be forming).  

### Recommended Option
- Wait 30–60 seconds after candle close before reading REST.
- Ensures full closure + consistent API values.
- Small delay is acceptable (accuracy > urgency).

### Modules
- **`utils/rest_api.py`**
  - `get_last_confirmed_candle(symbol, interval) -> dict`
  - Fetch OHLC from BingX REST
- **`core/telegram_bot.py`**
  - `send_signal(message: str)`
  - Send message to Telegram channel
- **`main.py`**
  - Load `config.json`
  - Loop through symbols/intervals
  - Send formatted message with confirmed close

### Data Flow
config.json → main.py → REST API → last confirmed candle → Telegram

ruby
Copy code

### Tests
1. **Unit test `get_last_confirmed_candle()`**
   - Mock REST response → ensure it returns `candles[-2]`.
2. **Unit test `send_signal()`**
   - Mock Telegram API → check correct format.
3. **Integration test `main.py`**
   - Mock both REST + Telegram → verify end-to-end flow.

### Example Telegram Message
Symbol: BTCUSDT
Interval: 1h
Last Confirmed Close: 27345.67
Timestamp: 14:00

python
Copy code

*Future:* if TF labels overlap, only keep the higher TF  
- e.g. 13:15 = 15m, 14:00 = 1h (not 15m), 16:00 = 4h (not 1h/15m).

---

## API Example – BingX Klines

File: `scripts/get_bingx_klines.py`  
No API signature required for public klines.

```python
import time, requests, hmac
from hashlib import sha256

APIURL = "https://open-api.bingx.com"
APIKEY, SECRETKEY = "", ""

def get_sign(api_secret, payload):
    return hmac.new(api_secret.encode(), payload.encode(), sha256).hexdigest()

def parseParam(paramsMap):
    keys = sorted(paramsMap)
    paramsStr = "&".join([f"{x}={paramsMap[x]}" for x in keys])
    return paramsStr + "&timestamp=" + str(int(time.time() * 1000))

def send_request(method, path, paramsMap):
    urlpa = parseParam(paramsMap)
    sign = get_sign(SECRETKEY, urlpa)
    url = f"{APIURL}{path}?{urlpa}&signature={sign}"
    headers = {"X-BX-APIKEY": APIKEY}
    return requests.request(method, url, headers=headers).text

def demo():
    return send_request("GET", "/openApi/swap/v3/quote/klines", {
        "symbol": "KNC-USDT",
        "interval": "1h",
        "limit": "1000",
        "startTime": "1702717199998"
    })

if __name__ == "__main__":
    print("demo:", demo())
yaml
Copy code

---

Would you like me to also add a **timeline/priority checklist** (✅ Step 1 done, ⏳ Step 2 in progress, etc.) so you can track progress inside the README?
