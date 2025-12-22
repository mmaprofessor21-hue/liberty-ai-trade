#!/usr/bin/env python3
import sys; sys.dont_write_bytecode = True

import os

def collect_all_files(directory):
    """
    Recursively collect all file paths within the given directory.
    Returns a list of absolute paths.
    """
    file_paths = []
    for root, _, files in os.walk(directory):
        for name in files:
            file_paths.append(os.path.join(root, name))
    return file_paths

def read_file_safe(file_path, mode='r'):
    """
    Reads a file safely using UTF-8 encoding.
    """
    try:
        with open(file_path, mode, encoding='utf-8') as file:
            return file.read()
    except UnicodeDecodeError:
        return None
    except Exception:
        return None

def write_file_safe(file_path, content, mode='w'):
    """
    Writes content to a file using UTF-8 encoding.
    """
    try:
        with open(file_path, mode, encoding='utf-8') as file:
            file.write(content)
        return True
    except Exception:
        return False

def is_binary_file(filepath):
    """
    Detect if a file is binary.
    """
    try:
        with open(filepath, 'rb') as file:
            chunk = file.read(1024)
            return b'\0' in chunk
    except Exception:
        return False
