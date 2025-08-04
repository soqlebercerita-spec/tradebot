# 🪟 WINDOWS INSTALLATION GUIDE

## Quick Start
1. Download all files dari Replit ke folder Windows
2. Double-click `run_bot.bat` untuk menjalankan bot
3. Sistem akan otomatis check dependencies dan launch GUI

## File Structure Required
```
your_folder/
├── launch_trading_bot.py          # Main launcher
├── run_bot.bat                    # Windows batch launcher
├── advanced_trading_engine.py     # Core trading engine
├── advanced_market_data.py        # Market data provider
├── advanced_notifications.py     # Notification system
├── hft_risk_manager.py           # Risk management
├── config.py                     # Configuration
└── WINDOWS_INSTALLATION.md       # This guide
```

## Prerequisites

### 1. Python Installation
- Download Python 3.8+ from [python.org](https://python.org)
- During installation, check "Add Python to PATH"
- Verify installation: Open Command Prompt, type `python --version`

### 2. Required Python Packages
```bash
pip install numpy pandas scikit-learn requests twilio
pip install MetaTrader5  # For Windows only
```

### 3. MetaTrader5 Setup
- Install MetaTrader5 from [MetaQuotes](https://www.metatrader5.com)
- Login to your trading account
- Enable "Allow automated trading" in Tools > Options > Expert Advisors

## Environment Variables Setup

### Option 1: Windows Environment Variables
1. Open "Environment Variables" dari Control Panel
2. Add these variables:
   - `TELEGRAM_BOT_TOKEN` = 8365734234:AAH2uTaZPDD47Lnm3y_Tcr6aj3xGL-bVsgk
   - `TELEGRAM_CHAT_ID` = 5061106648
   - `TWILIO_ACCOUNT_SID` = [Your Twilio SID]
   - `TWILIO_AUTH_TOKEN` = [Your Twilio Token]
   - `TWILIO_PHONE_NUMBER` = [Your Twilio WhatsApp Number]

### Option 2: .env File (Recommended)
Create file `.env` in the same folder:
```
TELEGRAM_BOT_TOKEN=8365734234:AAH2uTaZPDD47Lnm3y_Tcr6aj3xGL-bVsgk
TELEGRAM_CHAT_ID=5061106648
TWILIO_ACCOUNT_SID=your_twilio_sid
TWILIO_AUTH_TOKEN=your_twilio_token
TWILIO_PHONE_NUMBER=your_twilio_whatsapp_number
```

## Running the Bot

### Method 1: Batch File (Easiest)
1. Double-click `run_bot.bat`
2. Bot will automatically start with GUI

### Method 2: Command Line
```bash
python launch_trading_bot.py
```

### Method 3: Direct Launch
```bash
python advanced_trading_engine.py
```

## Features Available

### Real Money Trading
- Connect to MetaTrader5 for live trading
- Advanced risk management and position sizing
- Real-time market analysis and signal generation

### Simulation Mode
- If MT5 not available, runs in simulation mode
- Perfect for testing strategies and learning
- All features work except actual trade execution

### Notification System
- Telegram notifications for trade signals
- WhatsApp alerts for important updates
- Real-time profit/loss tracking

## Troubleshooting

### Common Issues

**1. "Python not found"**
- Install Python and add to PATH
- Restart Command Prompt after installation

**2. "MetaTrader5 import error"**
- Install MT5: `pip install MetaTrader5`
- Only works on Windows with MT5 installed

**3. "Module not found" errors**
- Install missing packages: `pip install package_name`
- Check all files are in the same folder

**4. "MT5 connection failed"**
- Ensure MetaTrader5 is running and logged in
- Enable automated trading in MT5 settings
- Check if firewall is blocking connection

**5. "Notification errors"**
- Verify environment variables are set
- Check internet connection
- Test Telegram bot token and chat ID

### Performance Tips

1. **Close unnecessary programs** while trading
2. **Ensure stable internet** connection
3. **Monitor system resources** during operation
4. **Regular MT5 restarts** for optimal performance

## Support

If you encounter issues:
1. Check error messages in the console
2. Verify all prerequisites are met
3. Test in simulation mode first
4. Check log files for detailed error info

## Security Notes

- Never share your API keys or bot tokens
- Use environment variables for sensitive data
- Keep your trading account credentials secure
- Regularly update passwords and API keys