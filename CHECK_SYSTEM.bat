@echo off
echo ===============================================
echo 🔍 SYSTEM CHECK - TRADING BOT REQUIREMENTS
echo ===============================================
echo.

REM Check Python
echo 🐍 Checking Python...
python --version
if errorlevel 1 (
    echo ❌ Python tidak ditemukan
    echo Install Python dari: https://www.python.org/downloads/
) else (
    echo ✅ Python OK
)

echo.
REM Check pip
echo 📦 Checking pip...
pip --version
if errorlevel 1 (
    echo ❌ pip tidak ditemukan
) else (
    echo ✅ pip OK
)

echo.
REM Check packages
echo 📊 Checking required packages...

python -c "import numpy; print('✅ numpy:', numpy.__version__)" 2>nul || echo ❌ numpy missing
python -c "import psutil; print('✅ psutil:', psutil.__version__)" 2>nul || echo ❌ psutil missing  
python -c "import requests; print('✅ requests:', requests.__version__)" 2>nul || echo ❌ requests missing
python -c "import MetaTrader5; print('✅ MetaTrader5: OK')" 2>nul || echo ❌ MetaTrader5 missing

echo.
REM Check MetaTrader5
echo 🏦 Checking MetaTrader5...
tasklist /FI "IMAGENAME eq terminal64.exe" 2>NUL | find /I /N "terminal64.exe">NUL
if "%ERRORLEVEL%"=="0" (
    echo ✅ MetaTrader5 running
) else (
    echo ⚠️ MetaTrader5 not running
)

echo.
REM Check bot files
echo 🤖 Checking bot files...
if exist "enhanced_windows_trading_bot.py" (
    echo ✅ Ultimate Trading Bot found
) else (
    echo ❌ Ultimate Trading Bot missing
)

if exist "trading_bot_windows.py" (
    echo ✅ Windows Trading Bot found
) else (
    echo ❌ Windows Trading Bot missing
)

if exist "config.py" (
    echo ✅ Configuration file found
) else (
    echo ❌ Configuration file missing
)

echo.
echo ===============================================
echo System check completed
echo ===============================================
pause