@echo off
title TRUSTSCAN - Forensic & Scam Verification Engine
echo =====================================================================
echo  TRUSTSCAN: Don't Just Trust. Verify.
echo  Starting local server on http://127.0.0.1:8000
echo =====================================================================
set PYTHONIOENCODING=utf-8
cd /d "%~dp0backend"
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
pause
