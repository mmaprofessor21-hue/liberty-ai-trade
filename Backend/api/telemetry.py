from fastapi import APIRouter
from core.control_router import trading_state, ai_state, system_state
from execution.wallet import wallet_manager
import time
import psutil

router = APIRouter(prefix="/telemetry", tags=["telemetry"])

@router.get("/status")
async def get_system_telemetry():
    """
    Returns aggregated system health and performance metrics.
    """
    wallet_status = await wallet_manager.get_status()
    
    return {
        "timestamp": time.time(),
        "system": {
            "status": system_state.status,
            "emergency": system_state.emergency,
            "execution_mode": system_state.execution_mode
        },
        "wallet": {
            "connected": wallet_status.connected,
            "safe": wallet_status.is_safe,
            "balance": wallet_status.balance_sol
        },
        "trading": {
            "strategy": trading_state.strategy,
            "active_risk": trading_state.risk_level
        },
        "ai": {
            "mode": ai_state.mode,
            "confidence_threshold": ai_state.confidence_threshold
        },
        "performance": {
            "cpu_usage": psutil.cpu_percent(),
            "memory_usage": psutil.virtual_memory().percent,
            "uptime": time.time() - psutil.boot_time() # Mock uptime logic
        }
    }
