import json
from pathlib import Path

# Project root
BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_PATH = BASE_DIR / "config.json"

# Load config once for all modules
with open(CONFIG_PATH, "r", encoding="utf-8") as f:
    config = json.load(f)
