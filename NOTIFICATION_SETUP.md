# 📱 NOTIFICATION SYSTEM SETUP

## Overview
Sistem notifikasi advanced untuk trading bot dengan dukungan Telegram dan WhatsApp untuk real-time alerts.

## Setup Environment Variables
Secret keys sudah diatur dalam Replit Secrets:

### Telegram Configuration
- `TELEGRAM_BOT_TOKEN`: 8365734234:AAH2uTaZPDD47Lnm3y_Tcr6aj3xGL-bVsgk
- `TELEGRAM_CHAT_ID`: 5061106648

### WhatsApp Configuration (via Twilio)
- `TWILIO_ACCOUNT_SID`: [Your Twilio Account SID]
- `TWILIO_AUTH_TOKEN`: [Your Twilio Auth Token]  
- `TWILIO_PHONE_NUMBER`: [Your Twilio WhatsApp Number]
- Target WhatsApp: +6285161603156

## Notification Types

### 1. Trading Signals
Dikirim saat ada signal trading baru:
```
🚀 TRADING SIGNAL EXECUTED
📊 Symbol: XAUUSDm
📈 Action: BUY
💰 Price: 2650.45
📏 Lot Size: 0.01
🎯 Confidence: 85%
⚙️ Mode: BALANCED
🕐 Time: 14:30:25
```

### 2. Profit/Loss Notifications
Dikirim saat trade selesai:
```
💰 TRADE PROFIT
📊 Symbol: XAUUSDm
📈 Action: BUY
💵 P/L: $125.50
🕐 Time: 14:45:30
```

### 3. Daily Summary
Ringkasan harian trading:
```
📊 DAILY TRADING SUMMARY
📈 Total Trades: 15
✅ Winning Trades: 12
🎯 Win Rate: 80.0%
💰 Total Profit: $750.25
📅 Date: 2025-08-04
```

### 4. System Alerts
Peringatan sistem penting:
```
⚠️ TRADING ALERT
MT5 Connection Lost - Switching to simulation mode
🕐 Time: 15:20:15
```

### 5. System Status
Update status sistem:
```
⚙️ SYSTEM STATUS
🔗 MT5 Connection: Connected
💰 Account Balance: $10,000.00
⏱️ Running Time: 120 minutes
🕐 Last Update: 15:30:45
```

## Features

### Advanced Notification Queue
- Priority-based messaging (high, medium, low)
- Automatic batching untuk mencegah spam
- Error handling dan retry logic

### Multi-Channel Support
- **Telegram**: Real-time notifications dengan formatting
- **WhatsApp**: High-priority alerts only (untuk menghemat costs)

### Notification Controls
- Test button untuk mengecek koneksi
- Manual daily summary trigger
- Emergency notification untuk sistem alerts

## Usage

### Test Notifications
Click button "🧪 Test Notifications" di GUI atau:
```python
notification_manager.test_notifications()
```

### Send Manual Summary
Click button "📊 Send Summary" di GUI atau:
```python
notification_manager.send_daily_summary({
    'total_trades': 10,
    'winning_trades': 8,
    'total_profit': 500.0
})
```

### Send Custom Alert
```python
notification_manager.send_alert("Custom message", alert_type='info')
```

## Error Handling
- Automatic fallback jika satu channel gagal
- Logging untuk troubleshooting
- Graceful degradation jika notification service tidak tersedia

## Security
- Secret keys disimpan aman di environment variables
- Tidak ada sensitive data di logs
- Rate limiting untuk mencegah abuse

## Integration dengan Trading Engine
Notification system terintegrasi otomatis dengan:
- Trade execution notifications
- MT5 connection status updates
- Profit/loss tracking
- System alerts dan warnings
- Daily performance summaries