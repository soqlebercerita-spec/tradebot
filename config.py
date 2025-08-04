"""
Core Configuration - Essential Settings
"""

class Config:
    # MetaTrader5 Settings
    MT5_MAGIC_NUMBER = 123456789
    MT5_DEVIATION = 10
    MT5_TIMEOUT = 10000
    
    # Trading Parameters
    MAX_ORDER_PER_SESSION = 50
    MAX_ORDER_PER_SESSION_HFT = 100
    
    # Risk Management
    MAX_RISK_PER_TRADE = 0.5
    MAX_DRAWDOWN = 3.0
    STOP_LOSS_PERSEN_BALANCE = 2.0
    TAKE_PROFIT_PERSEN_BALANCE = 1.0
    
    # Signal Processing
    SIGNAL_CONFIDENCE_THRESHOLD = 0.6
    SIGNAL_CONFIDENCE_THRESHOLD_HFT = 0.8
    
    # HFT Protection
    HFT_MAX_CONSECUTIVE_LOSSES = 3
    HFT_COOLDOWN_MINUTES = 15

config = Config()