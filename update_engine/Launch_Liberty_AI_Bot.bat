@echo off
setlocal enabledelayedexpansion

REM ========================================
REM  🚀 Launch Liberty AI Bot (Frontend + Backend)
REM  Place this file in: update_engine\Launch_Liberty_AI_Bot.bat
REM ========================================

cd /d "%~dp0"
cd ..

echo ----------------------------------------
echo Starting Liberty AI Bot...
echo ----------------------------------------

REM Start Backend
start "Backend" cmd /k "cd Backend && python main.py"

REM Start Frontend
start "Frontend" cmd /k "cd Frontend && npm start"

echo Liberty AI Bot launch sequence complete.
exit
