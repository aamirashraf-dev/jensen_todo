from __future__ import annotations
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "db.json"

DATA_DIR.mkdir(parents=True, exist_ok=True)

def read_db() -> list[dict]:
    """Read db.json. Returns empty list if file doesn't exist or is invalid."""
    if not DB_PATH.exists():
        return []
    try:
        with open(DB_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, list) else []
    except (json.JSONDecodeError, IOError):
        return []

def write_db(items: list[dict]) -> None:
    """Write items to db.json."""
    if not isinstance(items, list):
        raise ValueError("Database must be a list")
    with open(DB_PATH, "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=2)
