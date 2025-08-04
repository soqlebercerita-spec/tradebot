@echo off
echo ===============================================
echo 🧹 ULTIMATE TRADING BOT - CLEANUP SCRIPT
echo ===============================================
echo.
echo ⚠️  WARNING: This will delete redundant files
echo Make sure you have backup if needed
echo.
pause

echo 🗑️  Deleting old bot versions...
del /f /q trading_bot_integrated.py 2>nul
del /f /q trading_bot_windows.py 2>nul
del /f /q trading_bot_real.py 2>nul
del /f /q trading_bot_hft.py 2>nul
del /f /q trading_bot_launcher.py 2>nul

echo 🗑️  Deleting old launchers...
del /f /q START_TRADING_BOT.py 2>nul
del /f /q main.py 2>nul
del /f /q run.py 2>nul

echo 🗑️  Deleting old advanced features...
del /f /q adaptive_indicators.py 2>nul
del /f /q advanced_risk_manager.py 2>nul
del /f /q ml_engine.py 2>nul
del /f /q advanced_trading_engine.py 2>nul

echo 🗑️  Deleting utility files...
del /f /q auto_updater.py 2>nul
del /f /q config_manager.py 2>nul
del /f /q test_enhanced_trading.py 2>nul
del /f /q trading_strategies.py 2>nul
del /f /q hft_config.py 2>nul

echo 🗑️  Deleting old batch files...
del /f /q INSTALL_WINDOWS.bat 2>nul
del /f /q START_TRADING_BOT_WINDOWS.bat 2>nul
del /f /q install_requirements_windows.txt 2>nul

echo 🗑️  Deleting cache and logs...
rmdir /s /q __pycache__ 2>nul
del /f /q trading_log.txt 2>nul
del /f /q session_summary.txt 2>nul
del /f /q uv.lock 2>nul

echo 🗑️  Deleting attached assets...
rmdir /s /q attached_assets 2>nul

echo.
echo ✅ Cleanup completed!
echo.
echo 📁 Remaining files:
echo   🚀 enhanced_windows_trading_bot.py (MAIN BOT)
echo   ⚙️  Configuration files
echo   🤖 Advanced feature modules  
echo   🎮 Batch launchers
echo   📖 Documentation
echo.
echo 🎯 Your project is now clean and organized!
echo.
pause