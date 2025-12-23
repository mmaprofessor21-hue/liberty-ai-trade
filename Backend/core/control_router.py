from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from enum import Enum
from typing import Optional
import time
from fastapi import status as http_status

router = APIRouter(prefix="/controls", tags=["controls"])

# --- Enums matching Frontend ---

class LoggingMode(str, Enum):
    OFF = "OFF"
    NORMAL = "NORMAL"
    VERBOSE = "VERBOSE"

class RiskLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"

class Strategy(str, Enum):
    STANDARD = "STANDARD"
    SCALP = "SCALP"
    TREND = "TREND"
    RANGE = "RANGE"
    AI = "AI"

class AIMode(str, Enum):
    AUTO = "AUTO"
    MANUAL = "MANUAL"
    OFF = "OFF"

class AIStrategy(str, Enum):
    MOMENTUM = "MOMENTUM"
    CONTRARIAN = "CONTRARIAN"
    HYBRID = "HYBRID"

class AIConfidence(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"

# --- State Models ---

class TradingConfig(BaseModel):
    logging_mode: LoggingMode = LoggingMode.NORMAL
    risk_level: RiskLevel = RiskLevel.MEDIUM
    sniping_mode: bool = False
    strategy: Strategy = Strategy.STANDARD

class AIConfig(BaseModel):
    mode: AIMode = AIMode.AUTO
    strategy: AIStrategy = AIStrategy.MOMENTUM
    confidence_threshold: AIConfidence = AIConfidence.MEDIUM

from .system_state import SystemStatus, SystemState, system_state
from execution.engine import execution_engine
from data.engine import data_engine
from core.auth import require_admin
from core.rate_limiter import rate_limit
from data.engine import data_engine
import json

class SystemConfig(BaseModel):
    status: SystemStatus = SystemStatus.STOPPED
    emergency: bool = False

# --- Global In-Memory State (for now) ---

trading_state = TradingConfig()
ai_state = AIConfig()
# Use the canonical shared SystemState instance from core.system_state
# Do NOT rebind a separate local copy — import the single source of truth.
# `system_state` below refers to the shared Pydantic instance.

# system_state imported from core.system_state above


class CommandRequest(BaseModel):
    command: str
    params: Optional[dict] = None


def _build_system_snapshot():
    """Construct a canonical system snapshot dict combining core.system_state and engine state."""
    try:
        halted = bool(getattr(execution_engine, "is_halted")() if hasattr(execution_engine, "is_halted") else getattr(execution_engine, "halted", False))
    except Exception:
        halted = bool(getattr(execution_engine, "halted", False))

    try:
        halted_since = getattr(execution_engine, "halted_since", None)
    except Exception:
        halted_since = None

    try:
        active_orders = execution_engine.get_active_orders() if hasattr(execution_engine, "get_active_orders") else list(getattr(execution_engine, "_active_orders", []) or [])
    except Exception:
        active_orders = []

    snapshot = {
        "status": system_state.status,
        "emergency": bool(getattr(system_state, "emergency", False)),
        "halted": halted,
        "halted_since": halted_since,
        "active_orders": active_orders,
        "active_order_count": len(active_orders) if active_orders is not None else 0,
        "timestamp": time.time(),
        "provenance": getattr(system_state, "provenance", None),
    }
    return snapshot


def _broadcast_event(event_name: str, payload: dict):
    """Best-effort non-blocking broadcast to websocket listeners via data_engine listeners."""
    for q in getattr(data_engine, "listeners", []):
        try:
            # envelope
            msg = {"event": event_name, "payload": payload, "timestamp": time.time()}
            try:
                q.put_nowait(msg)
            except Exception:
                # schedule async put if queue blocks
                try:
                    import asyncio

                    asyncio.create_task(q.put(msg))
                except Exception:
                    pass
        except Exception:
            pass

# --- Endpoints ---

@router.get("/trading")
async def get_trading_config():
    return trading_state

@router.post("/trading")
async def update_trading_config(config: TradingConfig, _auth=Depends(require_admin), _rl=Depends(rate_limit(30,60))):
    global trading_state
    trading_state = config
    # Logic to trigger Trading Engine update would go here
    # Broadcast controls state to websocket listeners
    try:
        msg = {"event": "controls.state", "payload": {"trading": trading_state.model_dump()}}
        for q in getattr(data_engine, "listeners", []):
            try:
                q.put_nowait(msg)
            except Exception:
                pass
    except Exception:
        pass

    return {"status": "updated", "config": trading_state}

@router.get("/ai")
async def get_ai_config():
    return ai_state

@router.post("/ai")
async def update_ai_config(config: AIConfig, _auth=Depends(require_admin), _rl=Depends(rate_limit(30,60))):
    global ai_state
    ai_state = config
    try:
        msg = {"event": "controls.state", "payload": {"ai": ai_state.model_dump()}}
        for q in getattr(data_engine, "listeners", []):
            try:
                q.put_nowait(msg)
            except Exception:
                pass
    except Exception:
        pass
    return {"status": "updated", "config": ai_state}

@router.get("/system")
async def get_system_config():
    # Return canonical snapshot combining core system_state and execution engine state
    return {"system": _build_system_snapshot()}


@router.post("/command")
async def control_command(req: CommandRequest, _auth=Depends(require_admin), _rl=Depends(rate_limit(5,60))):
    cmd = (req.command or "").strip().upper()

    # Helper to build snapshot and respond
    def resp_ack(message: str):
        snap = _build_system_snapshot()
        return {"result": "ACK", "command": cmd, "message": message, "system": snap}

    def resp_reject(reason: str, http_code=http_status.HTTP_409_CONFLICT):
        snap = _build_system_snapshot()
        raise HTTPException(status_code=http_code, detail={"result": "REJECT", "command": cmd, "reason": reason, "system": snap})

    # Validate command
    if cmd not in ("START", "STOP", "EMERGENCY_STOP", "RESET_HALT"):
        raise HTTPException(status_code=http_status.HTTP_400_BAD_REQUEST, detail={"result": "ERROR", "reason": "Unknown command", "command": cmd})

    # EMERGENCY_STOP: use existing trigger (idempotent)
    if cmd == "EMERGENCY_STOP":
        from .emergency import trigger_emergency_stop

        changed = False
        try:
            changed = trigger_emergency_stop()
        except Exception:
            # best-effort; return error
            raise HTTPException(status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR, detail={"result": "ERROR", "reason": "Failed to trigger emergency"})

        snap = _build_system_snapshot()
        # broadcast events
        _broadcast_event("emergency_triggered", snap)
        _broadcast_event("system_state_change", snap)

        msg = "Emergency activated" if changed else "Emergency already active"
        return resp_ack(msg)

    # START
    if cmd == "START":
        if getattr(system_state, "emergency", False):
            return resp_reject("Cannot start while emergency is active")
        # Do not implicitly reset halted state; require explicit RESET_HALT
        if hasattr(execution_engine, "is_halted") and execution_engine.is_halted():
            return resp_reject("Execution engine halted; call RESET_HALT first")

        try:
            system_state.status = SystemStatus.RUNNING
        except Exception:
            pass

        snap = _build_system_snapshot()
        _broadcast_event("trading_started", {"status": "RUNNING", "timestamp": time.time()})
        _broadcast_event("system_state_change", snap)
        return resp_ack("Trading started")

    # STOP
    if cmd == "STOP":
        try:
            system_state.status = SystemStatus.STOPPED
        except Exception:
            pass
        snap = _build_system_snapshot()
        _broadcast_event("trading_stopped", {"status": "STOPPED", "timestamp": time.time()})
        _broadcast_event("system_state_change", snap)
        return resp_ack("Trading stopped")

    # RESET_HALT
    if cmd == "RESET_HALT":
        if getattr(system_state, "emergency", False):
            return resp_reject("Cannot reset halt while emergency is active")
        try:
            if hasattr(execution_engine, "reset_halt"):
                execution_engine.reset_halt()
        except Exception:
            raise HTTPException(status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR, detail={"result": "ERROR", "reason": "Failed to reset halt"})

        snap = _build_system_snapshot()
        _broadcast_event("system_state_change", snap)
        _broadcast_event("active_orders_updated", {"active_orders": snap.get("active_orders", []), "active_order_count": snap.get("active_order_count", 0)})
        return resp_ack("Halt reset")

@router.post("/system")
async def update_system_config(config: SystemConfig, _auth=Depends(require_admin), _rl=Depends(rate_limit(10,60))):
    global system_state
    
    # Handle Emergency Stop specifically
    if config.emergency:
        # Trigger Emergency Logic
        from .emergency import trigger_emergency_stop
        trigger_emergency_stop()
    # Apply incoming config to the shared SystemState instance (do not rebind)
    try:
        # map fields conservatively
        system_state.status = config.status
        system_state.emergency = config.emergency
    except Exception:
        # best-effort: do not raise for API callers
        pass

    try:
        msg = {"event": "controls.state", "payload": {"system": system_state.model_dump()}}
        for q in getattr(data_engine, "listeners", []):
            try:
                q.put_nowait(msg)
            except Exception:
                pass
    except Exception:
        pass

    return {"status": "updated", "config": system_state}
