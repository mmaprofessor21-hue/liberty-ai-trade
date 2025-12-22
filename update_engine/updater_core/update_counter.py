import sys; sys.dont_write_bytecode = True
import os
import json
from datetime import datetime

UPDATE_COUNTER_FILE = os.path.join("update_engine", "updater_core", "last_run.dat")

def get_next_update_count():
    """Read the current update counter from the file or initialize it."""
    if not os.path.exists(UPDATE_COUNTER_FILE):
        return "001"

    try:
        with open(UPDATE_COUNTER_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        current_count = int(data.get("count", 0))
    except (json.JSONDecodeError, ValueError, KeyError):
        current_count = 0

    next_count = current_count + 1
    return f"{next_count:03}"

def increment_update_counter(log):
    """Increment and save the update counter to file."""
    current = get_next_update_count()
    data = {
        "count": int(current),
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    try:
        with open(UPDATE_COUNTER_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        log.info(f"[COUNTER] Updated to #{current}")
    except Exception as e:
        log.error(f"[COUNTER ERROR] Failed to update counter: {e}")
