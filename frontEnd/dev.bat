@echo off
REM dev.bat - Clean __pycache__, start FastAPI, open site

call clear_pycache.bat
cd backend
start http://127.0.0.1:8000
uvicorn main:app --reload --log-level debug
pause
