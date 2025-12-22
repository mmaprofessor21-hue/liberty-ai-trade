# 🚨 DO NOT MODIFY THIS FILE OUTSIDE THE RULES IN README_UPDATER.txt
# 🚫 NO IMPORT OVERRIDES | 🚫 NO PATH ASSUMPTIONS | ✅ ABSOLUTE STRUCTURE COMPLIANCE
# TIMESTAMP: 
"""Backend/app.py

Legacy-compatible launcher that exposes the FastAPI `app` object
from `main.py` so process managers or tooling expecting `app:app`
can still function.

This file intentionally keeps logic minimal and delegates to main.py.
"""
from main import app  # Re-use the primary FastAPI app defined in main.py


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host="0.0.0.0", port=8000)
