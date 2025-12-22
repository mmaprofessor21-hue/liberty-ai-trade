# TIMESTAMP: 2025-12-21_15-01-22
from fastapi import APIRouter
import os
import time
from typing import Dict

from core.env_validator import validate_env
from data.engine import data_engine
from core.control_router import system_state as control_system_state
import importlib.util
import inspect


# Safely load the standalone `config.py` file (avoid package name collision with config/)
def _load_config_module():
    try:
        base = os.path.dirname(os.path.dirname(__file__))
        cfg_path = os.path.join(base, "config.py")
        cfg_path = os.path.normpath(cfg_path)
        if os.path.exists(cfg_path):
            spec = importlib.util.spec_from_file_location("backend_config", cfg_path)
            cfg = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(cfg)
            return cfg
    except Exception:
        return None


_cfg = _load_config_module()

router = APIRouter()


@router.get("/health")
async def health() -> Dict:
    """Extended health endpoint.

    - Reports env validation (FOUND/MISSING; does not expose secret values)
    - Returns version and build timestamp
    - Reports websocket/data engine status
    - Exposes current strategy/system state
    """
    # Env validation (do not expose secrets)
    env_summary = validate_env()

    # Version/project read from standalone config.py (if available)
    try:
        version = getattr(_cfg, "VERSION", None) if _cfg else None
        project = getattr(_cfg, "PROJECT_NAME", None) if _cfg else None
    except Exception:
        version = None
        project = None

    # Build timestamp: use main.py mtime as an approximate build timestamp
    try:
        import main as _main
        build_ts = os.path.getmtime(_main.__file__)
        build_timestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(build_ts))
    except Exception:
        build_timestamp = None

    # Websocket / data engine status
    ws_status = {
        "running": bool(getattr(data_engine, "running", False)),
        "listeners": len(getattr(data_engine, "listeners", [])),
    }

    return {
        "status": "ok" if env_summary.get("mode") == "ok" else "degraded",
        "project": project,
        "version": version,
        "build_timestamp": build_timestamp,
        "env": {"mode": env_summary.get("mode"), "summary": {k: env_summary[k] for k in env_summary if k != "mode"}},
        "websocket": ws_status,
        "strategy_state": control_system_state,
    }
