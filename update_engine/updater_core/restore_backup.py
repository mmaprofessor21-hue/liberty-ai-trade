import sys; sys.dont_write_bytecode = True

import os
import shutil
from pathlib import Path

BACKUP_FOLDER = Path("Backend/backups")
UPDATES_FOLDER = Path("update_engine/updates")

def restore_backup():
    if not BACKUP_FOLDER.exists():
        print("[RESTORE] Backup folder does not exist.")
        return
    for item in BACKUP_FOLDER.rglob("*"):
        if item.is_file():
            rel_path = item.relative_to(BACKUP_FOLDER)
            dest_path = UPDATES_FOLDER / rel_path
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(item, dest_path)
            print(f"[RESTORE] Restored {dest_path}")
