# scan_logic.py
import datetime

def log_scan_message(log):
    """
    Logs that both Frontend and Backend folders are being scanned.
    """
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log.write(f"[{timestamp}] [SCAN] Scanning Frontend and Backend folders for updates...\n")
    log.flush()
