from datetime import datetime, timezone
import pytz

def unix_to_local(unix_ms: int, tz: str) -> datetime:
    """
    Convert Unix timestamp in ms to localized datetime.
    """
    tzinfo = pytz.timezone(tz)
    dt = datetime.fromtimestamp(unix_ms / 1000, tz=timezone.utc)
    return dt.astimezone(tzinfo)

def now_ms() -> int:
    """Return current Unix timestamp in milliseconds."""
    return int(datetime.now(tz=timezone.utc).timestamp() * 1000)
