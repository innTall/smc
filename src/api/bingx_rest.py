import hmac
import requests
import logging
from hashlib import sha256
from typing import List, Optional

from src.types.models import Candle
from src.utils.timeutils import unix_to_local, now_ms

APIURL = "https://open-api.bingx.com"

class BingXRestClient:
    def __init__(self, api_key: str, secret_key: str, timezone: str = "UTC"):
        self.api_key = api_key
        self.secret_key = secret_key
        self.timezone = timezone
        self.logger = logging.getLogger(__name__)
        self.base_url = APIURL

    def _sign(self, payload: str) -> str:
        return hmac.new(
            self.secret_key.encode("utf-8"),
            payload.encode("utf-8"),
            digestmod=sha256
        ).hexdigest()

    def _build_url(self, path: str, params: dict) -> str:
        params = {k: v for k, v in params.items() if v is not None}
        sorted_keys = sorted(params.keys())
        params_str = "&".join([f"{k}={params[k]}" for k in sorted_keys])
        if params_str:
            params_str += f"&timestamp={now_ms()}"
        else:
            params_str = f"timestamp={now_ms()}"
        signature = self._sign(params_str)
        return f"{self.base_url}{path}?{params_str}&signature={signature}"

    def get_klines(
        self,
        symbol: str,
        interval: str,
        limit: int,
        start_time: Optional[int] = None,
        end_time: Optional[int] = None
    ) -> List[Candle]:
        """
        Fetch kline/candlestick data from BingX.
        """
        path = "/openApi/swap/v3/quote/klines"
        params = {
            "symbol": symbol,
            "interval": interval,
            "limit": limit,
            "startTime": start_time,
            "endTime": end_time,
        }
        url = self._build_url(path, params)
        headers = {"X-BX-APIKEY": self.api_key}

        self.logger.info(f"Fetching klines: {symbol} {interval} limit={limit}")
        resp = requests.get(url, headers=headers, timeout=10)
        resp.raise_for_status()
        data = resp.json()

        # Unwrap "data" if present
        if isinstance(data, dict) and "data" in data:
            data = data["data"]

        if not isinstance(data, list):
            raise ValueError(f"Unexpected response: {data}")

        candles = []
        for item in data:
            candles.append(
                Candle(
                    symbol=symbol,
                    interval=interval,
                    open=float(item["open"]),
                    high=float(item["high"]),
                    low=float(item["low"]),
                    close=float(item["close"]),
                    volume=float(item["volume"]),
                    time=unix_to_local(int(item["time"]), self.timezone),
                )
            )

        return candles
