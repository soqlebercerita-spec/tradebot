@echo off
echo ===============================================
echo 🚀 ULTIMATE TRADING BOT - INSTALLER & LAUNCHER
echo ===============================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python tidak ditemukan!
    echo Silakan install Python 3.8+ terlebih dahulu dari:
    echo https://www.python.org/downloads/
    pause
    exit /b 1
)

echo ✅ Python ditemukan
echo.

REM Install required packages
echo 📦 Installing required packages...
pip install numpy psutil requests MetaTrader5

if errorlevel 1 (
    echo ⚠️ Beberapa package mungkin gagal install
    echo Mencoba install satu per satu...
    pip install numpy
    pip install psutil 
    pip install requests
    pip install MetaTrader5
)

echo.
echo ✅ Installation completed!
echo.

REM Start the Ultimate Trading Bot
echo 🚀 Starting Ultimate Trading Bot...
echo.
python enhanced_windows_trading_bot.py

if errorlevel 1 (
    echo.
    echo ❌ Bot gagal start. Trying alternative...
    python trading_bot_windows.py
)

echo.
echo 👋 Bot session ended
pause