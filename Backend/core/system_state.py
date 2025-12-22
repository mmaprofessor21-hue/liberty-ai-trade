from enum import Enum
from pydantic import BaseModel
from typing import Optional

class SystemStatus(str, Enum):
    RUNNING = "RUNNING"
    STOPPED = "STOPPED"
    PAUSED = "PAUSED"
    EMERGENCY = "EMERGENCY"

class ExecutionMode(str, Enum):
    LOCAL = "LOCAL"
    TELEGRAM = "TELEGRAM"

class ConnectionState(str, Enum):
    CONNECTED = "CONNECTED"
    DISCONNECTED = "DISCONNECTED"
    CONNECTING = "CONNECTING"
    ERROR = "ERROR"

class SystemState(BaseModel):
    status: SystemStatus = SystemStatus.STOPPED
    execution_mode: ExecutionMode = ExecutionMode.LOCAL
    wallet_connection: ConnectionState = ConnectionState.DISCONNECTED
    # Health checks
    frontend_connected: bool = False
    backend_healthy: bool = True
    active_errors: list[str] = []
