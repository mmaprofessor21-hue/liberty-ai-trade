import sys
sys.dont_write_bytecode = True

import argparse
import os
from pathlib import Path
from typing import Iterable, List

# Folders we never want to walk (too big / irrelevant)
EXCLUDED_DIRS = {
    ".git",
    "node_modules",
    "__pycache__",
    ".venv",
    "venv",
    "dist",
    "build",
    ".idea",
    ".vscode",
    "logs",
}

# File extensions we treat as binary and skip entirely
BINARY_EXTENSIONS = {
    ".png", ".jpg", ".jpeg", ".gif", ".bmp",
    ".ico", ".pdf", ".zip", ".gz", ".rar",
    ".7z", ".exe", ".dll", ".so", ".pyd",
    ".db", ".sqlite", ".sqlite3",
    ".ttf", ".otf", ".woff", ".woff2",
    ".mp3", ".wav", ".mp4", ".mov", ".avi",
}

# Default text/code extensions to include if user doesn't specify --ext
DEFAULT_TEXT_EXTENSIONS = {
    ".py", ".js", ".jsx", ".ts", ".tsx",
    ".json", ".yml", ".yaml", ".md",
    ".css", ".scss", ".sass",
    ".html", ".htm",
    ".txt",
}


def is_binary_file(path: Path) -> bool:
    return path.suffix.lower() in BINARY_EXTENSIONS


def should_include_file(path: Path, exts: Iterable[str]) -> bool:
    if is_binary_file(path):
        return False
    if not exts:
        return True
    return path.suffix.lower() in exts


def iter_source_files(root: Path, base: Path, exts: Iterable[str]) -> Iterable[Path]:
    """
    Yield all files under `base` that should be included, skipping excluded dirs.
    `root` is the project root so we can compute pretty relative paths.
    """
    for dirpath, dirnames, filenames in os.walk(base):
        # Strip excluded directories
        dirnames[:] = [d for d in dirnames if d not in EXCLUDED_DIRS]

        for name in filenames:
            file_path = Path(dirpath) / name
            if should_include_file(file_path, exts):
                yield file_path


def write_chunked_snapshot(
    files: List[Path],
    project_root: Path,
    out_prefix: Path,
    label: str,
    chunk_size_kb: int,
) -> List[Path]:
    """
    Write files into one or more snapshot txt files, each capped at approx chunk_size_kb.
    Returns list of created snapshot paths.
    """
    chunk_size_bytes = chunk_size_kb * 1024
    created_files: List[Path] = []

    if not files:
        return created_files

    chunk_index = 1
    bytes_in_chunk = 0
    out_path = out_prefix.with_name(f"{out_prefix.stem}_part{chunk_index}{out_prefix.suffix}")
    out = out_path.open("w", encoding="utf-8")
    created_files.append(out_path)

    out.write(f"=== {label} snapshot ===\n\n")

    for f in files:
        rel = f.relative_to(project_root)
        try:
            content = f.read_text(encoding="utf-8", errors="replace")
        except Exception as e:
            block = f"----- ERROR reading {rel.as_posix()}: {e} -----\n\n"
        else:
            block = f"===== {rel.as_posix()} =====\n{content}\n\n"

        block_bytes = len(block.encode("utf-8"))

        # If adding this block would exceed the chunk size, start a new file
        if bytes_in_chunk + block_bytes > chunk_size_bytes:
            out.close()
            chunk_index += 1
            bytes_in_chunk = 0
            out_path = out_prefix.with_name(
                f"{out_prefix.stem}_part{chunk_index}{out_prefix.suffix}"
            )
            out = out_path.open("w", encoding="utf-8")
            created_files.append(out_path)
            out.write(f"=== {label} snapshot (cont.) ===\n\n")

        out.write(block)
        bytes_in_chunk += block_bytes

    out.close()
    return created_files


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Export project snapshots (frontend/backend/folder) into small text chunks for ChatGPT."
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--backend", action="store_true", help="Export the Backend folder.")
    group.add_argument("--frontend", action="store_true", help="Export the Frontend folder.")
    group.add_argument(
        "--folder",
        type=str,
        help="Export a specific subfolder relative to project root (e.g. 'Backend/trading').",
    )

    parser.add_argument(
        "--ext",
        type=str,
        default="",
        help=(
            "Comma-separated list of file extensions to include "
            "(e.g. .py,.js,.jsx). If omitted, a default set of text/code "
            "extensions is used."
        ),
    )
    parser.add_argument(
        "--chunk-size-kb",
        type=int,
        default=256,
        help="Approximate maximum size of each snapshot chunk file in KB (default: 256).",
    )

    return parser.parse_args()


def main() -> None:
    args = parse_args()

    project_root = Path(__file__).resolve().parent
    frontend_dir = project_root / "Frontend"
    backend_dir = project_root / "Backend"

    # Logs dir (reusing existing convention)
    logs_dir = frontend_dir / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)

    # Parse extensions
    if args.ext:
        ext_list = [e.strip().lower() for e in args.ext.split(",") if e.strip()]
        allowed_exts = set(ext_list)
    else:
        allowed_exts = set(DEFAULT_TEXT_EXTENSIONS)

    if args.backend:
        base = backend_dir
        label = "Backend"
        out_prefix = logs_dir / "backend_snapshot.txt"

    elif args.frontend:
        base = frontend_dir
        label = "Frontend"
        out_prefix = logs_dir / "frontend_snapshot.txt"

    else:
        base = (project_root / args.folder).resolve()
        if not str(base).startswith(str(project_root)):
            print("[ERROR] --folder path must be inside the project root.")
            return
        label = f"Folder: {base.relative_to(project_root).as_posix()}"
        safe_name = "_".join(base.relative_to(project_root).parts)
        out_prefix = logs_dir / f"folder_snapshot_{safe_name}.txt"

    if not base.exists():
        print(f"[ERROR] Base path not found: {base}")
        return

    print(f"[SNAPSHOT] Project root: {project_root}")
    print(f"[SNAPSHOT] Base path:    {base}")
    print(f"[SNAPSHOT] Label:        {label}")
    print(f"[SNAPSHOT] Chunk size:   {args.chunk_size_kb} KB")
    if allowed_exts:
        print(f"[SNAPSHOT] Extensions:   {', '.join(sorted(allowed_exts))}")
    else:
        print("[SNAPSHOT] Extensions:   (all non-binary files)")

    files = list(iter_source_files(project_root, base, allowed_exts))
    files = sorted(files, key=lambda p: p.relative_to(project_root).as_posix())

    if not files:
        print("[SNAPSHOT] No matching files found to export.")
        return

    created = write_chunked_snapshot(
        files=files,
        project_root=project_root,
        out_prefix=out_prefix,
        label=label,
        chunk_size_kb=args.chunk_size_kb,
    )

    print("[SNAPSHOT] Created snapshot files:")
    for p in created:
        print(f"  - {p}")


if __name__ == "__main__":
    main()
