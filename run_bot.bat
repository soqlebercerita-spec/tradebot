@echo off
echo ========================================
echo    ADVANCED TRADING BOT LAUNCHER
echo ========================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from python.org
    pause
    exit /b 1
)

echo Python detected, launching trading bot...
echo.

REM Try to run the advanced trading engine
python launch_trading_bot.py

if errorlevel 1 (
    echo.
    echo ERROR: Failed to launch trading bot
    echo Check the error messages above for troubleshooting
)

echo.
pause