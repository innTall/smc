import json
import time
import zlib
import websocket
import threading
from utils.logger import setup_logger

class WebSocketManager:
    def __init__(self, config, engine):
        self.config = config
        self.engine = engine
        self.url = "wss://open-api-swap.bingx.com/swap-market"
        self.ws = None
        self.logger = setup_logger(config["logging"]["level"])
        self.stop_flag = False

    def _on_message(self, ws, message):
        try:
            # decompress if needed
            if isinstance(message, bytes):
                try:
                    message = zlib.decompress(message, 16 + zlib.MAX_WBITS).decode("utf-8")
                except Exception:
                # sometimes it's already plain text
                    message = message.decode("utf-8", errors="ignore")
            
            if not message.strip():
                return

            try:
                data = json.loads(message)
            except Exception:
                self.logger.debug(f"Ignored non-JSON message: {message[:50]}")
                return

            # Only process kline messages
            if data.get("code") != 0 or not data.get("data") or not data.get("s"):
                return

            symbol = data["s"].replace("-", "")  # optional: normalize symbol to match config
            interval = data["dataType"].split("_")[-1]  # e.g., "15m", "1h"
            
            for k in data["data"]:
                candle = {
                    "time": k["T"],
                    "open": float(k["o"]),
                    "high": float(k["h"]),
                    "low": float(k["l"]),
                    "close": float(k["c"]),
                    "volume": float(k["v"]),
                    "is_closed": True,  # always True for public kline feed
                }

                # Prevent duplicate processing
                last_candle_time = self.engine.candles.get_last_time(symbol, interval)
                
                # Only handle new candles
                if last_candle_time is None or candle["time"] > last_candle_time:
                    self.logger.info(f"[CLOSED] {symbol} {interval} close={candle['close']}")
                    self.engine.handle_candle(symbol, interval, candle)
                    
        except Exception as e:
            self.logger.error(f"Error parsing message: {e}")

    def _on_error(self, ws, error):
        self.logger.error(f"WebSocket error: {error}")

    def _on_close(self, ws, close_status_code, close_msg):
        self.logger.warning("WebSocket closed. Attempting reconnect...")

    def _on_open(self, ws):
        self.logger.info("WebSocket connected.")

        # Subscribe to kline streams for each symbol & interval
        for sym in self.config["symbols"]:
            # BingX expects dash in symbol
            sym_dash = sym.replace("USDT", "-USDT")
            for interval in self.config["intervals"]:
                sub = {
                    "id": f"{sym}_{interval}_kline",
                    "reqType": "sub",
                    "dataType": f"{sym_dash}@kline_{interval}"
                }
                ws.send(json.dumps(sub))
                self.logger.info(f"Subscribed to {sub['dataType']}")

    def _run(self):
        while not self.stop_flag:
            try:
                self.ws = websocket.WebSocketApp(
                    self.url,
                    on_message=self._on_message,
                    on_error=self._on_error,
                    on_close=self._on_close,
                    on_open=self._on_open
                )
                self.ws.run_forever(ping_interval=20, ping_timeout=10)
            except Exception as e:
                self.logger.error(f"WebSocket run_forever exception: {e}")
            self.logger.info("Reconnecting in 5s...")
            time.sleep(5)

    def run_forever(self):
        thread = threading.Thread(target=self._run, daemon=True)
        thread.start()
        while True:
            time.sleep(1)

    def stop(self):
        self.stop_flag = True
        if self.ws:
            self.ws.close()

# python core/websocket_manager.py