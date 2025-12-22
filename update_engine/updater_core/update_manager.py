#!/usr/bin/env python3
import sys; sys.dont_write_bytecode = True

import os
import time
import argparse
import subprocess
from datetime import datetime
from pathlib import Path

def get_next_cycle_number():
    """Get the next update cycle number."""
    counter_file = Path("update_engine/update_counter.dat")
    if counter_file.exists():
        try:
            count = int(counter_file.read_text().strip())
            return count + 1
        except (ValueError, FileNotFoundError):
            return 1
    return 1

def save_cycle_number(cycle_num):
    """Save the current cycle number."""
    counter_file = Path("update_engine/update_counter.dat")
    counter_file.write_text(str(cycle_num))

def create_backup():
    """Create backup of current drop-zone."""
    import shutil
    from pathlib import Path
    
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    backup_dir = Path("Backend/backups")
    backup_dir.mkdir(parents=True, exist_ok=True)
    
    updates_dir = Path("update_engine/updates")
    if updates_dir.exists():
        backup_file = backup_dir / f"updates_backup_{timestamp}.zip"
        shutil.make_archive(str(backup_file).replace(".zip", ""), 'zip', updates_dir)
        print(f"[BACKUP] Created: {backup_file}")

def execute_bulk_update():
    """Execute bulk_update.py and capture its output."""
    bulk_file = Path("update_engine/updates/bulk_update.py")
    if not bulk_file.exists():
        print("[ERROR] bulk_update.py not found in drop-zone")
        return False
    
    print("[BULK] Executing bulk_update.py ...")
    
    try:
        result = subprocess.run([
            sys.executable, str(bulk_file)
        ], capture_output=True, text=True, cwd=".")
        
        if result.returncode != 0:
            print(f"[ERROR] bulk_update.py failed: {result.stderr}")
            return False
        
        for line in result.stdout.splitlines():
            if line.strip():
                print(line)
        
        return True
    except Exception as e:
        print(f"[ERROR] Failed to execute bulk_update.py: {e}")
        return False

def sync_files():
    """Sync files from drop-zone to live directories."""
    import shutil

    synced_count = 0
    updates_dir = Path("update_engine/updates")

    # Sync Frontend files
    frontend_src = updates_dir / "Frontend"
    frontend_dst = Path("Frontend")

    if frontend_src.exists():
        for item in frontend_src.rglob("*"):
            if not item.is_file():
                continue

            rel_path = item.relative_to(frontend_src)
            dest_file = frontend_dst / rel_path
            dest_file.parent.mkdir(parents=True, exist_ok=True)

            suffix = item.suffix.lower()

            # --- Binary files: copy raw ---
            if suffix in ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.zip', '.tar', '.gz', '.pdf', '.ico']:
                try:
                    shutil.copy2(item, dest_file)
                    synced_count += 1
                except Exception as e:
                    print(f"[SYNC ERROR] Failed to copy binary {item}: {e}")
                continue

            # --- Text files: attempt UTF-8 read, fallback on failure ---
            try:
                content = item.read_text(encoding='utf-8')
            except UnicodeDecodeError:
                try:
                    shutil.copy2(item, dest_file)
                    synced_count += 1
                except Exception as e:
                    print(f"[SYNC ERROR] Failed to copy file {item}: {e}")
                continue

            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

            # Inject placeholders
            if suffix == '.py':
                content = content.replace("# TIMESTAMP: ", f"# TIMESTAMP: {timestamp}")
            elif suffix in ['.js', '.jsx', '.css']:
                content = content.replace("/* TIMESTAMP: */", f"/* TIMESTAMP: {timestamp} */")
            # JSON and other text files remain unchanged

            try:
                dest_file.write_text(content, encoding='utf-8')
                synced_count += 1
            except Exception as e:
                print(f"[SYNC ERROR] Failed to write {dest_file}: {e}")

    # Sync Backend files  
    backend_src = updates_dir / "Backend"
    backend_dst = Path("Backend")

    if backend_src.exists():
        for item in backend_src.rglob("*"):
            if not item.is_file():
                continue

            rel_path = item.relative_to(backend_src)
            # Avoid live config/__init__.py conflict
            if rel_path == Path("config/__init__.py"):
                continue

            dest_file = backend_dst / rel_path
            dest_file.parent.mkdir(parents=True, exist_ok=True)

            suffix = item.suffix.lower()

            if suffix in ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.zip', '.tar', '.gz', '.pdf', '.ico']:
                try:
                    shutil.copy2(item, dest_file)
                    synced_count += 1
                except Exception as e:
                    print(f"[SYNC ERROR] Failed to copy binary {item}: {e}")
                continue

            try:
                content = item.read_text(encoding='utf-8')
            except UnicodeDecodeError:
                try:
                    shutil.copy2(item, dest_file)
                    synced_count += 1
                except Exception as e:
                    print(f"[SYNC ERROR] Failed to copy file {item}: {e}")
                continue

            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

            if suffix == '.py':
                content = content.replace("# TIMESTAMP: ", f"# TIMESTAMP: {timestamp}")
            elif suffix in ['.js', '.jsx', '.css']:
                content = content.replace("/* TIMESTAMP: */", f"/* TIMESTAMP: {timestamp} */")

            try:
                dest_file.write_text(content, encoding='utf-8')
                synced_count += 1
            except Exception as e:
                print(f"[SYNC ERROR] Failed to write {dest_file}: {e}")

    print(f"[SYNC] File synchronization completed ({synced_count} file(s))")
    return synced_count

def create_update_log(cycle_num):
    """Create update log in Frontend/logs/."""
    import json

    logs_dir = Path("Frontend/logs")
    logs_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_file = logs_dir / f"update_log_{timestamp}.json"

    log_data = {
        "cycle": cycle_num,
        "timestamp": timestamp,
        "status": "completed"
    }

    log_file.write_text(json.dumps(log_data, indent=2))
    print(f"[LOG]  {log_file}")

def main():
    parser = argparse.ArgumentParser(description="Liberty AI Trade Updater")
    parser.add_argument('--force', action='store_true', help='Force update execution')
    args = parser.parse_args()

    start_time = time.time()

    # Get cycle number
    cycle_num = get_next_cycle_number()
    print(f"[INFO] Forcing update cycle #{cycle_num:04d}")

    # Step 1: Create backup
    create_backup()

    # Step 2: Execute bulk_update.py
    if not execute_bulk_update():
        print("[ERROR] Update failed during bulk generation")
        return 1

    # Step 3: Sync files
    synced_count = sync_files()

    # Step 4: Update counters and logs
    save_cycle_number(cycle_num)
    print(f"[COUNTER] Cycle: #{cycle_num:04d}")

    create_update_log(cycle_num)

    # Step 5: Summary
    elapsed = time.time() - start_time
    print(f"[INFO] Core update completed: {synced_count} files updated")
    print(f"[DONE] Update completed in {elapsed:.1f} s")

    return 0

if __name__ == "__main__":
    sys.exit(main())
