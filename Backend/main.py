# TIMESTAMP: 2025-12-21_15-01-22
from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from api.api_routes import router
import os

from api.websocket import router as ws_router, start_data_engine
from api.telemetry import router as telemetry_router


@asynccontextmanager
async def lifespan(app):
    # startup
    # Ensure execution engine is in a clean state on startup (helps tests)
    try:
        from execution.engine import execution_engine
        if hasattr(execution_engine, "reset_halt"):
            execution_engine.reset_halt()
    except Exception:
        pass

    await start_data_engine()

    # Ensure a final reset after any startup side-effects
    try:
        from execution.engine import execution_engine
        if hasattr(execution_engine, "reset_halt"):
            execution_engine.reset_halt()
    except Exception:
        pass
    try:
        yield
    finally:
        # TODO: graceful shutdown tasks if needed
        pass


app = FastAPI(title="Liberty AI Trade API", lifespan=lifespan)

# Secure default CORS handling: prefer explicit allowed origins.
# - In DEBUG/local dev allow localhost:3000 by default.
# - In production set ALLOWED_ORIGINS env var (comma-separated).
debug_env = os.environ.get("DEBUG", "true").lower()
DEBUG = debug_env in ("1", "true", "yes")
if DEBUG:
    allowed = ["http://localhost:3000", "http://127.0.0.1:3000"]
else:
    raw = os.environ.get("ALLOWED_ORIGINS", "")
    allowed = [o.strip() for o in raw.split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api")

from core.control_router import router as control_router
app.include_router(control_router, prefix="/api/v1")


@app.get("/")
async def root():
    return {"status": "ok", "service": "Liberty AI Trade API"}


app.include_router(ws_router)
app.include_router(telemetry_router, prefix="/api/v1")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
