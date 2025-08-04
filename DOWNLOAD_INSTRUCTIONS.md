# 📥 DOWNLOAD & SETUP INSTRUCTIONS

## Download Files untuk Windows

Untuk menjalankan bot di Windows, download semua file berikut dan simpan dalam folder yang sama:

### Core Files (WAJIB)
1. `advanced_trading_engine.py` - Trading engine utama
2. `advanced_market_data.py` - Market data provider
3. `advanced_notifications.py` - Sistem notifikasi
4. `hft_risk_manager.py` - Risk management
5. `config.py` - Konfigurasi sistem

### Launcher Files (RECOMMENDED)
6. `launch_trading_bot.py` - Python launcher
7. `run_bot.bat` - Windows batch launcher (double-click untuk start)

### Documentation
8. `WINDOWS_INSTALLATION.md` - Panduan instalasi Windows
9. `NOTIFICATION_SETUP.md` - Setup notifikasi
10. `DOWNLOAD_INSTRUCTIONS.md` - File ini

## Quick Setup

### 1. Download Semua File
- Klik kanan pada setiap file di Replit → "Download"
- Atau copy-paste content ke notepad dan save dengan nama yang sama

### 2. Struktur Folder
```
C:\TradingBot\
├── advanced_trading_engine.py
├── advanced_market_data.py  
├── advanced_notifications.py
├── hft_risk_manager.py
├── config.py
├── launch_trading_bot.py
├── run_bot.bat
└── [documentation files]
```

### 3. Install Python Dependencies
Buka Command Prompt dan jalankan:
```bash
pip install numpy pandas scikit-learn requests twilio MetaTrader5
```

### 4. Setup Environment Variables
Buat file `.env` dalam folder yang sama:
```
TELEGRAM_BOT_TOKEN=8365734234:AAH2uTaZPDD47Lnm3y_Tcr6aj3xGL-bVsgk
TELEGRAM_CHAT_ID=5061106648
TWILIO_ACCOUNT_SID=your_twilio_sid
TWILIO_AUTH_TOKEN=your_twilio_token  
TWILIO_PHONE_NUMBER=your_twilio_whatsapp_number
```

### 5. Run the Bot
Double-click `run_bot.bat` atau jalankan:
```bash
python launch_trading_bot.py
```

## Troubleshooting

**File tidak ada di Windows:**
- Download ulang file yang missing
- Pastikan semua file dalam folder yang sama
- Cek nama file tidak ada typo

**Python error:**
- Install Python 3.8+ dari python.org
- Install dependencies: `pip install numpy pandas scikit-learn requests twilio MetaTrader5`

**MT5 connection error:**
- Install dan jalankan MetaTrader5
- Login ke akun trading
- Enable "Allow automated trading"

**Notification error:**
- Setup environment variables dengan benar
- Test koneksi internet
- Verify API keys

## Alternative Files

Jika file lama masih ada di Windows, rename atau hapus:
- `enhanced_windows_trading_bot.py`
- `trading_bot_windows.py` 
- `trading_bot_integrated.py`

File-file ini sudah diganti dengan sistem yang lebih advanced.

## Support

Jika masih ada error, periksa:
1. Semua file sudah didownload dengan lengkap
2. Python dan dependencies terinstall
3. MetaTrader5 running dan login
4. Environment variables setup dengan benar

Sistem baru ini jauh lebih advanced dengan:
- Better error handling
- Real-time notifications
- Advanced risk management  
- Multi-timeframe analysis
- Machine learning integration