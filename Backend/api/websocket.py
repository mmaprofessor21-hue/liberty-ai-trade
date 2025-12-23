from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from data.engine import data_engine
import asyncio
import os
import time
import jwt
from execution.wallet import wallet_manager
from core.control_router import system_state, trading_state, ai_state
from core.rate_limiter import check_rate_for_key

ADMIN_API_KEY = os.environ.get("ADMIN_API_KEY")
JWT_SECRET = os.environ.get("JWT_SECRET_KEY")


router = APIRouter(prefix="/ws", tags=["websocket"])

@router.websocket("/market_data")
async def websocket_endpoint(websocket: WebSocket):
    # Auth: allow anonymous read-only clients, allow admin clients with API key or JWT.
    headers = websocket.headers
    api_key = headers.get("x-api-key") or headers.get("X-API-KEY")
    auth_header = headers.get("authorization") or headers.get("Authorization")
    is_admin = False

    # Check API Key
    try:
        if api_key and ADMIN_API_KEY and api_key == ADMIN_API_KEY:
            is_admin = True
    except Exception:
        is_admin = False

    # If not API key, try JWT
    if not is_admin and auth_header and auth_header.lower().startswith("bearer ") and JWT_SECRET:
        token = auth_header.split(None, 1)[1]
        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"]) if token else None
            roles = payload.get("roles") or payload.get("role") or []
            if isinstance(roles, str):
                roles = [roles]
            if payload and "admin" in roles:
                is_admin = True
        except Exception:
            is_admin = False

    # Apply rate limits (per-key for admin, per-host for anonymous)
    client_host = websocket.client.host if websocket.client else "unknown"
    try:
        if is_admin:
            key = api_key or f"admin:{client_host}"
            check_rate_for_key(key, max_calls=120, period_seconds=60)
        else:
            key = f"anon:{client_host}"
            check_rate_for_key(key, max_calls=30, period_seconds=60)
    except Exception:
        # Close with policy violation / rate limit
        await websocket.close(code=1008)
        return

    # Accept the connection after auth/rate checks
    await websocket.accept()
    queue = data_engine.subscribe()
    try:
        while True:
            data = await queue.get()
            await websocket.send_json(data)
    except WebSocketDisconnect:
        data_engine.unsubscribe(queue)
        print("Client disconnected")

# Startup event to launch the background task
async def start_data_engine():
    # Configure demo/data-feed behavior from env
    demo_flag = os.environ.get("ENABLE_DEMO_DATA", "false").lower()
    data_engine.allow_demo = demo_flag in ("1", "true", "yes")
    asyncio.create_task(data_engine.start_streaming())

    # Start periodic telemetry broadcaster for system.health and wallet.status
    async def telemetry_broadcaster():
        while True:
            try:
                wallet_status = await wallet_manager.get_status()
                payload = {
                    "event": "system.health",
                    "payload": {
                        "system": {
                            "status": system_state.status,
                            "emergency": system_state.emergency,
                        },
                        "wallet": {
                            "connected": wallet_status.connected,
                            "safe": wallet_status.is_safe,
                            "balance": wallet_status.balance_sol,
                        },
                        "trading": {"strategy": trading_state.strategy, "risk": trading_state.risk_level},
                        "ai": {"mode": ai_state.mode, "confidence": ai_state.confidence_threshold},
                        "timestamp": time.time(),
                    },
                }
                for q in getattr(data_engine, "listeners", []):
                    try:
                        # Prefer non-blocking put to avoid stalling broadcaster
                        # If the queue cannot accept immediately, schedule a put task
                        try:
                            q.put_nowait(payload)
                        except Exception:
                            # Some queue types may block; schedule asynchronously
                            try:
                                asyncio.create_task(q.put(payload))
                            except Exception:
                                # As a last resort, ignore to keep broadcaster alive
                                pass
                    except Exception:
                        pass
            except Exception:
                pass
            await asyncio.sleep(5)

    asyncio.create_task(telemetry_broadcaster())
