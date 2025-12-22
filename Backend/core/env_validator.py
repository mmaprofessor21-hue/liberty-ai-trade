import os
from typing import List, Dict

CRITICAL_KEYS = [
    "JWT_SECRET_KEY",
    "SOLANA_RPC_URL",
    "REDIS_URL",
]

OPTIONAL_KEYS = [
    "DEXSCREENER_API_KEY",
    "TELEGRAM_BOT_TOKEN",
    "TELEGRAM_CHAT_ID",
    "OPENAI_API_KEY",
]


def _read_env_file(path: str) -> str:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return ""


def _append_placeholder_env(path: str, keys: List[str]):
    # Append commented placeholders for missing keys (do NOT write secrets)
    try:
        with open(path, "a", encoding="utf-8") as f:
            f.write("\n# --- Added by env_validator (placeholders) ---\n")
            for k in keys:
                f.write(f"# {k}=\n")
    except Exception:
        # Never raise here; validator should be safe at startup
        pass


def validate_env(append_placeholders: bool = True, env_path: str = ".env") -> Dict[str, str]:
    """
    Check presence of required environment keys without printing their values.

    Returns a dict mapping key -> 'FOUND'|'MISSING'. Also adds a top-level
    'mode' value: 'ok' or 'degraded' or 'fail' when critical keys are missing.
    """
    result = {}
    missing = []

    for k in CRITICAL_KEYS + OPTIONAL_KEYS:
        if os.environ.get(k) is not None:
            result[k] = "FOUND"
        else:
            result[k] = "MISSING"
            missing.append(k)

    # Determine overall mode
    critical_missing = any(k for k in CRITICAL_KEYS if result.get(k) == "MISSING")
    if critical_missing:
        mode = "fail"
    elif missing:
        mode = "degraded"
    else:
        mode = "ok"

    result["mode"] = mode

    # Append placeholders to env file for missing keys (safe: placeholders only)
    if append_placeholders and missing:
        current = _read_env_file(env_path)
        # Only append keys that don't already exist commented/uncommented
        to_append = [k for k in missing if k not in current]
        if to_append:
            _append_placeholder_env(env_path, to_append)

    return result
