@echo off
echo ===============================================
echo 📦 TRADING BOT - REQUIREMENTS INSTALLER
echo ===============================================
echo.

echo 🔧 Installing Python packages...
echo.

REM Core packages
echo Installing core packages...
pip install --upgrade pip
pip install numpy>=1.21.0
pip install psutil>=7.0.0  
pip install requests>=2.25.0

echo.
echo 📊 Installing MetaTrader5...
pip install MetaTrader5

echo.
echo 🤖 Installing optional AI packages...
pip install scikit-learn
pip install pandas
pip install matplotlib

echo.
echo ✅ All packages installed!
echo.
echo 🚀 Ready to start trading bot
echo Run START_ULTIMATE_BOT.bat to start
echo.
pause