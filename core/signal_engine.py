from datetime import datetime, timezone, timedelta
import pytz

def format_message(symbol: str, interval: str, candle: dict, config: dict) -> str:
    """
    Build a human-readable message with configurable timezone.
    - Shows only the closing time of the last candle.
    - Time is formatted as HH:MM in the local timezone from config.json.
    """
    tz_name = config.get("timezone", "UTC")
    try:
        local_tz = pytz.timezone(tz_name)
    except Exception:
        local_tz = pytz.UTC

    # candle["timestamp"] is usually the OPEN time → add interval length to get CLOSE time
    ts_open = datetime.fromtimestamp(candle["timestamp"] / 1000, tz=timezone.utc)
    if interval.endswith("h"):
        hours = int(interval.replace("h", ""))
        ts_close = ts_open + timedelta(hours=hours)
    elif interval.endswith("m"):
        minutes = int(interval.replace("m", ""))
        ts_close = ts_open + timedelta(minutes=minutes)
    else:
        ts_close = ts_open

    # Convert to local timezone
    local_time = ts_close.astimezone(local_tz)

    return (
        f"Symbol: {symbol}\n"
        f"Interval: {interval}\n"
        f"Last confirmed Close: {candle['close']}\n"
        f"Time: {local_time.strftime('%H:%M')}"
    )
