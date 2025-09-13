from datetime import datetime, timezone
import pytz
from src.settings import config

LOCAL_TZ = pytz.timezone(config.get("timezone", "UTC"))
DATETIME_FMT = config.get("datetime_format", "%Y-%m-%d %H:%M:%S")

def now_ms() -> int:
    """Return current Unix timestamp in milliseconds."""
    return int(datetime.now(tz=timezone.utc).timestamp() * 1000)

def to_datetime(ts: int) -> datetime:
    """Convert Unix ms timestamp to Europe/Madrid local time."""
    dt_utc = datetime.fromtimestamp(ts / 1000, tz=timezone.utc)
    return dt_utc.astimezone(LOCAL_TZ)

def format_dt(dt: datetime) -> str:
    """Format datetime globally with config settings."""
    return dt.strftime(DATETIME_FMT)