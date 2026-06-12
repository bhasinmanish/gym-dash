@echo off
title Gym Dash
chcp 65001 >nul 2>&1
echo.
echo  =========================================
echo   GYM DASH - Personal Progress Tracker
echo  =========================================
echo.

:: Check that Python is available
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo  [ERROR] Python is not installed or not in PATH.
    echo.
    echo  Please install Python 3 from:
    echo    https://www.python.org/downloads/
    echo.
    echo  During install, check the box:
    echo    "Add Python to PATH"
    echo.
    pause
    exit /b 1
)

:: Print Python version for sanity check
for /f "tokens=*" %%v in ('python --version 2^>^&1') do echo  Python: %%v
echo.

:: Open the browser after a 2-second delay (gives server time to start)
start "" cmd /c "timeout /t 2 /nobreak >nul && start http://localhost:8181"

echo  Server starting at http://localhost:8181
echo  Your browser will open automatically.
echo.
echo  Press Ctrl+C (then Y) to stop the server.
echo  =========================================
echo.

:: Run server from the same directory as this .bat file
python "%~dp0server.py"

echo.
echo  Server stopped.
pause
