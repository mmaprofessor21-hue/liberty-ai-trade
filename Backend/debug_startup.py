import sys
import os
sys.path.append(os.getcwd())

import logging

logger = logging.getLogger(__name__)

logger.info("Attempting main.py logic...")
try:
    from fastapi import FastAPI
    from fastapi.middleware.cors import CORSMiddleware
    from api.api_routes import router
    from core.control_router import router as control_router
    from api.websocket import router as ws_router, start_data_engine
    
    app = FastAPI(title="Liberty AI Trade API")
    app.include_router(router, prefix="/api")
    app.include_router(control_router, prefix="/api/v1")
    app.include_router(ws_router)
    
    logger.info("App created successfully.")
except Exception as e:
    import traceback
    traceback.print_exc()
