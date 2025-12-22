import sys; sys.dont_write_bytecode = True

import shutil
from datetime import datetime
from pathlib import Path

def backup_updates(updates_dir, backend_dir):
    """Create backup of the drop-zone directory."""
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    backup_dir = Path(backend_dir) / "backups"
    backup_dir.mkdir(parents=True, exist_ok=True)

    backup_file = backup_dir / f"updates_backup_{timestamp}.zip"
    
    # Create backup excluding logs and backups subdirectories
    shutil.make_archive(str(backup_file).replace(".zip", ""), 'zip', updates_dir)
    print(f"[BACKUP] Created: {backup_file}")
    
    return backup_file