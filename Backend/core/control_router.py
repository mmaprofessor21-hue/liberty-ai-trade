from fastapi import APIRouter, Depends
from pydantic import BaseModel
from enum import Enum
from typing import Optional

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

from .system_state import SystemStatus
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
system_state = SystemConfig()

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
    return system_state

@router.post("/system")
async def update_system_config(config: SystemConfig, _auth=Depends(require_admin), _rl=Depends(rate_limit(10,60))):
    global system_state
    
    # Handle Emergency Stop specifically
    if config.emergency:
        # Trigger Emergency Logic
        from .emergency import trigger_emergency_stop
        trigger_emergency_stop()
        
    system_state = config
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
