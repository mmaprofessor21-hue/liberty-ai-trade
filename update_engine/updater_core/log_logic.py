import sys; sys.dont_write_bytecode = True
import os
from datetime import datetime

LOGS_DIR = os.path.join("Frontend", "logs")
LOG_FILE_PATH = os.path.join(LOGS_DIR, "update_log.txt")

def start_logger(update_cycle_id):
    """Start logger and return a file object for logging."""
    os.makedirs(LOGS_DIR, exist_ok=True)

    try:
        log_file = open(LOG_FILE_PATH, "a", encoding="utf-8")
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_file.write(f"\n\n=== Update Cycle {update_cycle_id} Started: {timestamp} ===\n")
        log_file.flush()
        return log_file
    except Exception as e:
        print(f"[LOGGER ERROR] Failed to start logger: {e}")
        return None

def stop_logger(log):
    """Safely close the logger."""
    if log:
        try:
            log.write(f"\n=== Update Cycle Completed ===\n")
            log.flush()
            log.close()
        except Exception as e:
            print(f"[LOGGER ERROR] Failed to close logger: {e}")
