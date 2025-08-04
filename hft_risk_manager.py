"""
HFT Risk Manager - Advanced Protection System
Designed to prevent consecutive losses and improve winrate
"""

import datetime
from config import config

class HFTRiskManager:
    def __init__(self):
        self.consecutive_losses = 0
        self.cooldown_until = None
        self.daily_loss_amount = 0
        self.session_profit = 0
        self.trade_history = []
        self.last_trade_result = None
        self.starting_balance = None
        
        # Enhanced risk parameters
        self.max_consecutive_losses = 2  # Even stricter than config
        self.cooldown_minutes = 15       # Longer cooldown
        self.max_daily_loss_pct = 3      # Max 3% daily loss
        self.max_session_loss = 500      # Max $500 session loss
        
    def should_allow_trade(self, current_balance, signal_confidence):
        """Check if HFT trade should be allowed"""
        now = datetime.datetime.now()
        
        # Initialize starting balance
        if not self.starting_balance:
            self.starting_balance = current_balance
        
        # 1. Check cooldown period
        if self.cooldown_until and now < self.cooldown_until:
            return False, "Cooldown period active"
        
        # 2. Check consecutive losses (stricter than config)
        if self.consecutive_losses >= self.max_consecutive_losses:
            self.cooldown_until = now + datetime.timedelta(minutes=self.cooldown_minutes)
            return False, f"{self.max_consecutive_losses} consecutive losses - cooldown activated"
        
        # 3. Check daily loss limit
        daily_loss_pct = (self.daily_loss_amount / self.starting_balance) * 100
        if daily_loss_pct > self.max_daily_loss_pct:
            return False, f"Daily loss limit reached ({daily_loss_pct:.1f}%)"
        
        # 4. Check session loss limit
        if self.session_profit < -self.max_session_loss:
            return False, f"Session loss limit reached (${abs(self.session_profit):.2f})"
        
        # 5. Check signal quality - HFT needs high confidence
        if signal_confidence < config.SIGNAL_CONFIDENCE_THRESHOLD_HFT:
            return False, f"Signal confidence too low ({signal_confidence:.3f})"
        
        # 6. Check if last 3 trades were losses (extra protection)
        if len(self.trade_history) >= 3:
            last_3_results = [t['profit_loss'] for t in self.trade_history[-3:]]
            if all(pl < 0 for pl in last_3_results):
                return False, "Last 3 trades were losses - protection active"
        
        return True, "Trade allowed"
    
    def record_trade_result(self, profit_loss):
        """Record trade result and update protection counters"""
        self.trade_history.append({
            'timestamp': datetime.datetime.now(),
            'profit_loss': profit_loss,
            'balance_impact': (profit_loss / self.starting_balance) * 100 if self.starting_balance else 0
        })
        
        # Update counters
        self.session_profit += profit_loss
        
        if profit_loss < 0:
            self.consecutive_losses += 1
            self.daily_loss_amount += abs(profit_loss)
            self.last_trade_result = 'LOSS'
        else:
            self.consecutive_losses = 0  # Reset on any profit
            self.last_trade_result = 'PROFIT'
        
        # Keep only last 50 trades
        if len(self.trade_history) > 50:
            self.trade_history = self.trade_history[-50:]
    
    def get_risk_status(self):
        """Get current risk status summary"""
        now = datetime.datetime.now()
        cooldown_remaining = 0
        
        if self.cooldown_until and now < self.cooldown_until:
            cooldown_remaining = (self.cooldown_until - now).total_seconds() / 60
        
        daily_loss_pct = 0
        if self.starting_balance:
            daily_loss_pct = (self.daily_loss_amount / self.starting_balance) * 100
        
        return {
            'consecutive_losses': self.consecutive_losses,
            'max_consecutive_losses': self.max_consecutive_losses,
            'cooldown_remaining_minutes': cooldown_remaining,
            'daily_loss_amount': self.daily_loss_amount,
            'daily_loss_percentage': daily_loss_pct,
            'session_profit': self.session_profit,
            'last_trade_result': self.last_trade_result,
            'total_trades': len(self.trade_history)
        }
    
    def reset_daily_counters(self):
        """Reset daily counters (call at start of new day)"""
        self.daily_loss_amount = 0
        self.session_profit = 0
        self.consecutive_losses = 0
        self.cooldown_until = None
        self.trade_history = []
    
    def calculate_safe_lot_size(self, balance, base_lot_size, signal_confidence):
        """Calculate safer lot size based on current risk factors"""
        risk_multiplier = 1.0
        
        # Reduce lot size after losses
        if self.consecutive_losses > 0:
            risk_multiplier *= (1.0 - (self.consecutive_losses * 0.2))  # 20% reduction per loss
        
        # Reduce lot size if session is negative
        if self.session_profit < 0:
            risk_multiplier *= 0.8  # 20% reduction when session is negative
        
        # Reduce lot size for low confidence signals
        if signal_confidence < 0.5:
            risk_multiplier *= 0.7  # 30% reduction for low confidence
        
        # Ensure minimum lot size
        safe_lot = max(base_lot_size * risk_multiplier, 0.01)
        
        return round(safe_lot, 2)