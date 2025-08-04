@echo off
echo ===============================================
echo 🚀 ULTIMATE WINDOWS TRADING BOT - LAUNCHER
echo ===============================================
echo.
echo 🎯 3 Trading Modes: HFT, Normal, Scalping
echo 💰 Balance-based TP/SL System
echo 🔧 Optimized for Real Trading
echo.

REM Check if MetaTrader5 is running
tasklist /FI "IMAGENAME eq terminal64.exe" 2>NUL | find /I /N "terminal64.exe">NUL
if "%ERRORLEVEL%"=="0" (
    echo ✅ MetaTrader5 detected running
) else (
    echo ⚠️ MetaTrader5 tidak terdeteksi
    echo Pastikan MT5 sudah running untuk live trading
)

echo.
echo 🚀 Starting Ultimate Trading Bot...
echo.

python enhanced_windows_trading_bot.py

if errorlevel 1 (
    echo.
    echo ❌ Ultimate bot error, trying Windows bot...
    python trading_bot_windows.py
    
    if errorlevel 1 (
        echo.
        echo ❌ Windows bot error, trying integrated bot...
        python trading_bot_integrated.py
    )
)

echo.
echo 👋 Trading session ended
pause