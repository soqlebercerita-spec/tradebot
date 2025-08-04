"""
Advanced Notification System
Real-time trading notifications via Telegram and WhatsApp
"""

import os
import requests
import json
from datetime import datetime
from twilio.rest import Client
import threading
import time

class AdvancedNotificationManager:
    def __init__(self):
        """Initialize notification system with multiple channels"""
        # Telegram configuration
        self.telegram_token = os.getenv('TELEGRAM_BOT_TOKEN')
        self.telegram_chat_id = os.getenv('TELEGRAM_CHAT_ID')
        
        # WhatsApp (Twilio) configuration
        self.twilio_sid = os.getenv('TWILIO_ACCOUNT_SID')
        self.twilio_token = os.getenv('TWILIO_AUTH_TOKEN')
        self.twilio_phone = os.getenv('TWILIO_PHONE_NUMBER')
        self.target_whatsapp = "+6285161603156"  # Target WhatsApp number
        
        # Initialize Twilio client
        try:
            if self.twilio_sid and self.twilio_token:
                self.twilio_client = Client(self.twilio_sid, self.twilio_token)
                self.whatsapp_enabled = True
            else:
                self.whatsapp_enabled = False
        except Exception as e:
            print(f"WhatsApp/Twilio initialization failed: {e}")
            self.whatsapp_enabled = False
        
        # Check Telegram availability
        self.telegram_enabled = bool(self.telegram_token and self.telegram_chat_id)
        
        # Notification queue for batch sending
        self.notification_queue = []
        self.queue_lock = threading.Lock()
        
        # Start notification processor
        self.processor_thread = threading.Thread(target=self._process_notifications, daemon=True)
        self.processor_thread.start()
        
        print(f"✅ Notification system initialized")
        print(f"📱 Telegram: {'Enabled' if self.telegram_enabled else 'Disabled'}")
        print(f"📱 WhatsApp: {'Enabled' if self.whatsapp_enabled else 'Disabled'}")
    
    def send_trade_notification(self, trade_data):
        """Send trading notification"""
        symbol = trade_data.get('symbol', 'Unknown')
        action = trade_data.get('action', 'Unknown')
        price = trade_data.get('price', 0)
        lot_size = trade_data.get('lot_size', 0)
        confidence = trade_data.get('confidence', 0)
        mode = trade_data.get('mode', 'Unknown')
        
        # Create formatted message
        message = f"""🚀 TRADING SIGNAL EXECUTED

📊 Symbol: {symbol}
📈 Action: {action}
💰 Price: {price:.5f}
📏 Lot Size: {lot_size}
🎯 Confidence: {confidence:.1%}
⚙️ Mode: {mode}
🕐 Time: {datetime.now().strftime('%H:%M:%S')}

#TradingBot #Profit #MT5"""
        
        self._queue_notification(message, priority='high')
    
    def send_profit_notification(self, profit_data):
        """Send profit/loss notification"""
        profit = profit_data.get('profit', 0)
        symbol = profit_data.get('symbol', 'Unknown')
        action = profit_data.get('action', 'Unknown')
        
        emoji = "💰" if profit > 0 else "⚠️"
        status = "PROFIT" if profit > 0 else "LOSS"
        
        message = f"""{emoji} TRADE {status}

📊 Symbol: {symbol}
📈 Action: {action}
💵 P/L: ${profit:.2f}
🕐 Time: {datetime.now().strftime('%H:%M:%S')}

#Trading{status} #MT5"""
        
        self._queue_notification(message, priority='high')
    
    def send_daily_summary(self, summary_data):
        """Send daily trading summary"""
        total_trades = summary_data.get('total_trades', 0)
        winning_trades = summary_data.get('winning_trades', 0)
        total_profit = summary_data.get('total_profit', 0)
        win_rate = (winning_trades / total_trades * 100) if total_trades > 0 else 0
        
        message = f"""📊 DAILY TRADING SUMMARY

📈 Total Trades: {total_trades}
✅ Winning Trades: {winning_trades}
🎯 Win Rate: {win_rate:.1f}%
💰 Total Profit: ${total_profit:.2f}
📅 Date: {datetime.now().strftime('%Y-%m-%d')}

#DailySummary #TradingStats"""
        
        self._queue_notification(message, priority='medium')
    
    def send_alert(self, alert_message, alert_type='info'):
        """Send general alert"""
        emoji_map = {
            'info': 'ℹ️',
            'warning': '⚠️',
            'error': '❌',
            'success': '✅'
        }
        
        emoji = emoji_map.get(alert_type, 'ℹ️')
        
        message = f"""{emoji} TRADING ALERT

{alert_message}

🕐 Time: {datetime.now().strftime('%H:%M:%S')}"""
        
        priority = 'high' if alert_type in ['error', 'warning'] else 'medium'
        self._queue_notification(message, priority)
    
    def send_system_status(self, status_data):
        """Send system status update"""
        connection_status = status_data.get('connection_status', 'Unknown')
        balance = status_data.get('balance', 0)
        running_time = status_data.get('running_time', 0)
        
        message = f"""⚙️ SYSTEM STATUS

🔗 MT5 Connection: {connection_status}
💰 Account Balance: ${balance:.2f}
⏱️ Running Time: {running_time} minutes
🕐 Last Update: {datetime.now().strftime('%H:%M:%S')}

#SystemStatus #MT5Bot"""
        
        self._queue_notification(message, priority='low')
    
    def _queue_notification(self, message, priority='medium'):
        """Add notification to queue"""
        with self.queue_lock:
            self.notification_queue.append({
                'message': message,
                'priority': priority,
                'timestamp': datetime.now()
            })
    
    def _process_notifications(self):
        """Process notification queue"""
        while True:
            try:
                with self.queue_lock:
                    if self.notification_queue:
                        # Sort by priority (high, medium, low)
                        priority_order = {'high': 0, 'medium': 1, 'low': 2}
                        self.notification_queue.sort(key=lambda x: priority_order.get(x['priority'], 1))
                        
                        notification = self.notification_queue.pop(0)
                        
                        # Send notification
                        self._send_to_all_channels(notification['message'])
                
                time.sleep(2)  # Process every 2 seconds
                
            except Exception as e:
                print(f"Notification processing error: {e}")
                time.sleep(5)
    
    def _send_to_all_channels(self, message):
        """Send message to all available channels"""
        # Send to Telegram
        if self.telegram_enabled:
            self._send_telegram(message)
        
        # Send to WhatsApp (only for high priority)
        if self.whatsapp_enabled:
            self._send_whatsapp(message)
    
    def _send_telegram(self, message):
        """Send message via Telegram"""
        try:
            url = f"https://api.telegram.org/bot{self.telegram_token}/sendMessage"
            data = {
                'chat_id': self.telegram_chat_id,
                'text': message,
                'parse_mode': 'HTML'
            }
            
            response = requests.post(url, data=data, timeout=10)
            
            if response.status_code == 200:
                print("✅ Telegram notification sent")
            else:
                print(f"❌ Telegram failed: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Telegram error: {e}")
    
    def _send_whatsapp(self, message):
        """Send message via WhatsApp (Twilio)"""
        try:
            if not self.whatsapp_enabled:
                return
            
            # Format message for WhatsApp
            whatsapp_message = message.replace('#', '').replace('📊', '').replace('📈', '')
            
            message_obj = self.twilio_client.messages.create(
                body=whatsapp_message,
                from_=f'whatsapp:{self.twilio_phone}',
                to=f'whatsapp:{self.target_whatsapp}'
            )
            
            print("✅ WhatsApp notification sent")
            
        except Exception as e:
            print(f"❌ WhatsApp error: {e}")
    
    def test_notifications(self):
        """Test all notification channels"""
        test_message = f"""🧪 NOTIFICATION TEST

All systems operational!
Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

#Test #TradingBot"""
        
        print("🧪 Testing notification channels...")
        self._send_to_all_channels(test_message)
        
        return {
            'telegram': self.telegram_enabled,
            'whatsapp': self.whatsapp_enabled
        }

# Global notification manager instance
notification_manager = AdvancedNotificationManager()