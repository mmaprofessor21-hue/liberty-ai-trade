import sys; sys.dont_write_bytecode = True

import os
import time
import shutil
from datetime import datetime
from updater_core.utils import collect_all_files, read_file_safe, write_file_safe, is_binary_file

FRONTEND_DIR = "Frontend"
BACKEND_DIR = "Backend"
UPDATES_DIR = "update_engine/updates"

TIMESTAMP_MARKERS = ["# TIMESTAMP:", "// TIMESTAMP:"]

def inject_timestamp(content):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    for marker in TIMESTAMP_MARKERS:
        if marker in content:
            content = content.replace(marker, f"{marker} {current_time}")
    return content

def update_file(src, dst, log):
    if is_binary_file(src):
        return False
    src_content = read_file_safe(src)
    if src_content is None:
        return False
    new_content = inject_timestamp(src_content)
    old_content = read_file_safe(dst) if os.path.exists(dst) else ""
    if new_content != old_content:
        write_file_safe(dst, new_content)
        rel_path = os.path.relpath(dst)
        if "test_update" in os.path.basename(dst).lower():
            log.write(f"[TEST UPDATED] {rel_path}\n")
        elif "bulk_update" in os.path.basename(dst).lower():
            log.write(f"[BULK WRITTEN] {rel_path}\n")
        else:
            log.write(f"[UPDATED] {rel_path}\n")
        return True
    return False

def run_core_updates(log, force=False):
    updated_files = 0
    for folder in ['Frontend', 'Backend']:
        src_root = os.path.join(UPDATES_DIR, folder)
        dst_root = folder
        all_files = collect_all_files(src_root)
        for src_file in all_files:
            rel_path = os.path.relpath(src_file, src_root)
            dst_file = os.path.join(dst_root, rel_path)
            os.makedirs(os.path.dirname(dst_file), exist_ok=True)
            if force or update_file(src_file, dst_file, log):
                updated_files += 1
    if updated_files == 0:
        log.write("[CORE] No core updates applied.\n")
