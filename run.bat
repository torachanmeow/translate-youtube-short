@echo off
setlocal

if not exist "venv\Scripts\activate.bat" (
    echo [ERROR] Python virtual environment not found.
    echo Please follow these setup steps first:
    echo   1. python -m venv venv
    echo   2. venv\Scripts\activate.bat
    echo   3. pip install -r requirements.txt
    pause
    exit /b
)

call venv\Scripts\activate.bat
python translate_youtube_short.py
pause