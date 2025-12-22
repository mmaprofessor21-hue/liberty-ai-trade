#!/usr/bin/env python3
import sys; sys.dont_write_bytecode = True

import os
import shutil
from datetime import datetime
from pathlib import Path

def inject_timestamp(content, file_extension):
    """Inject timestamp into file content based on file type."""
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    
    if file_extension == '.py':
        content = content.replace("# TIMESTAMP: ", f"# TIMESTAMP: {timestamp}")
    elif file_extension in ['.js', '.jsx']:
        content = content.replace("/* TIMESTAMP: */", f"/* TIMESTAMP: {timestamp} */")
    elif file_extension in ['.css', '.scss']:
        content = content.replace("/* TIMESTAMP: */", f"/* TIMESTAMP: {timestamp} */")
    elif file_extension in ['.html', '.md']:
        content = content.replace("<!-- TIMESTAMP: -->", f"<!-- TIMESTAMP: {timestamp} -->")
    # JSON files get no timestamp injection (comments not allowed)
    
    return content

def sync_updates(log=None):
    """Sync files from drop-zone to live directories with timestamp injection."""
    synced_count = 0
    updates_dir = Path("update_engine/updates")
    
    # Sync Frontend files
    frontend_src = updates_dir / "Frontend"
    frontend_dst = Path("Frontend")
    
    if frontend_src.exists():
        for item in frontend_src.rglob("*"):
            if item.is_file():
                rel_path = item.relative_to(frontend_src)
                dest_file = frontend_dst / rel_path
                dest_file.parent.mkdir(parents=True, exist_ok=True)
                
                try:
                    content = item.read_text(encoding='utf-8')
                    
                    # Skip timestamp injection for JSON files
                    if item.suffix != '.json':
                        content = inject_timestamp(content, item.suffix)
                    
                    dest_file.write_text(content, encoding='utf-8')
                    synced_count += 1
                    
                    if log:
                        log.write(f"[SYNC] {dest_file}\n")
                        
                except Exception as e:
                    print(f"[SYNC ERROR] Failed to sync {item}: {e}")
    
    # Sync Backend files
    backend_src = updates_dir / "Backend"
    backend_dst = Path("Backend")
    
    if backend_src.exists():
        for item in backend_src.rglob("*"):
            if item.is_file():
                rel_path = item.relative_to(backend_src)
                dest_file = backend_dst / rel_path
                
                # Skip config/__init__.py to avoid namespace conflicts
                if rel_path == Path("config/__init__.py"):
                    continue
                
                dest_file.parent.mkdir(parents=True, exist_ok=True)
                
                try:
                    content = item.read_text(encoding='utf-8')
                    
                    # Skip timestamp injection for JSON files
                    if item.suffix != '.json':
                        content = inject_timestamp(content, item.suffix)
                    
                    dest_file.write_text(content, encoding='utf-8')
                    synced_count += 1
                    
                    if log:
                        log.write(f"[SYNC] {dest_file}\n")
                        
                except Exception as e:
                    print(f"[SYNC ERROR] Failed to sync {item}: {e}")
    
    return synced_count