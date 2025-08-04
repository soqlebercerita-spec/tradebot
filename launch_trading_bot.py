#!/usr/bin/env python3
"""
🚀 TRADING BOT LAUNCHER
Launches the Advanced Trading Engine with proper error handling
"""

import sys
import os
import subprocess

def main():
    """Main launcher function"""
    print("🚀 ADVANCED TRADING BOT LAUNCHER")
    print("=" * 50)
    
    # Try to launch the advanced trading engine
    try:
        print("📋 Launching Advanced Trading Engine...")
        
        # Import and run the advanced trading engine
        from advanced_trading_engine import AdvancedTradingEngine
        
        # Create and start the engine
        engine = AdvancedTradingEngine()
        
        # Start the GUI
        print("✅ Starting GUI...")
        engine.root.mainloop()
        
    except ImportError as e:
        print(f"❌ Import Error: {e}")
        print("💡 Make sure all required files are present:")
        print("   - advanced_trading_engine.py")
        print("   - advanced_market_data.py") 
        print("   - advanced_notifications.py")
        print("   - hft_risk_manager.py")
        print("   - config.py")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\n🔧 Troubleshooting:")
        print("1. Check if MetaTrader5 is installed and running")
        print("2. Verify environment variables are set")
        print("3. Ensure all dependencies are installed")
        
    finally:
        print("\n👋 Trading Bot session ended")
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()