import sys; sys.dont_write_bytecode = True

import os
import shutil
from datetime import datetime
from pathlib import Path

def atomic_write(src, dest):
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dest)

def inject_timestamp(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            lines = f.readlines()

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        for i, line in enumerate(lines):
            if "# TIMESTAMP:" in line or "// TIMESTAMP:" in line:
                lines[i] = f"{line.split(':')[0]}: {timestamp}\n"
                with open(filepath, "w", encoding="utf-8") as f:
                    f.writelines(lines)
                break
    except Exception as e:
        print(f"[BULK WARNING] Timestamp injection failed: {e}")

def process_bulk_updates(logs_dir):
    updated_files = []
    bulk_path = Path("update_engine/updates/Frontend/src/tests/bulk_update.py")
    target_path = Path("Frontend/src/tests/bulk_update.py")

    if not bulk_path.exists():
        print("[BULK] No bulk_update.py found.")
        return updated_files

    try:
        atomic_write(bulk_path, target_path)
        inject_timestamp(target_path)
        updated_files.append(str(target_path))
        print(f"[BULK WRITTEN] {target_path}")
        with open(Path(logs_dir) / "update_log.txt", "a", encoding="utf-8") as log:
            log.write(f"[BULK WRITTEN] {target_path}\n")
    except Exception as e:
        print(f"[BULK ERROR] Failed to update bulk file: {e}")

    return updated_files
