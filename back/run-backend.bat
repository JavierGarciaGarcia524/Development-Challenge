@echo off
REM
powershell -Command "Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass"

REM
call venv\Scripts\activate

REM
python run.py

pause