@echo off
:: ──────────────────────────────────────────────────────────────
:: Liberty AI Trade  –  Updater Launcher  (Windows only)
:: Calls the updater with the fully-qualified import path:
::     python -m update_engine.updater_core.update_manager --force
:: ──────────────────────────────────────────────────────────────

rem 1) Scope environment variables to this script only
setlocal

rem 2) Optional: clean up any stray __pycache__ folders
for /d /r %%d in (__pycache__) do if exist "%%d" rd /s /q "%%d"

rem 3) Launch the updater; forward any extra CLI args to Python
python -m update_engine.updater_core.update_manager --force %*

rem 4) End local environment scope
endlocal
