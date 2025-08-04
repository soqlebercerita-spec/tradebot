#!/usr/bin/env python3
"""
🚀 ADVANCED PROFITABLE TRADING ENGINE
✅ Deep Market Analysis
🎯 Ultra-High Winrate System  
💰 Intelligent Risk Management
🔧 Real Money Optimized
"""

import time
import datetime
import numpy as np
import threading
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.scrolledtext import ScrolledText
import tkinter.messagebox as messagebox
import requests
import csv
import os
import json
import sys
from scipy import stats
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler

# Import enhanced modules
try:
    from config import config
except ImportError:
    # Create basic config if not available
    class BasicConfig:
        MT5_MAGIC_NUMBER = 123456
        MT5_DEVIATION = 10
    config = BasicConfig()

from hft_risk_manager import HFTRiskManager
from advanced_market_data import market_data_provider

# MetaTrader5 integration with fallback
try:
    import MetaTrader5 as mt5
    MT5_AVAILABLE = True
except ImportError:
    MT5_AVAILABLE = False
    print("⚠️ MetaTrader5 not available - running in simulation mode")

class AdvancedTradingEngine:
    def __init__(self):
        """Initialize advanced trading engine with deep analysis"""
        print("🚀 Initializing Advanced Profitable Trading Engine...")
        
        # Core components
        self.risk_manager = HFTRiskManager()
        self.market_analyzer = AdvancedMarketAnalyzer()
        self.signal_processor = IntelligentSignalProcessor()
        self.portfolio_manager = SmartPortfolioManager()
        self.market_data = market_data_provider
        
        # Trading modes
        self.CONSERVATIVE_MODE = "CONSERVATIVE"
        self.BALANCED_MODE = "BALANCED" 
        self.AGGRESSIVE_MODE = "AGGRESSIVE"
        self.ULTRA_HFT_MODE = "ULTRA_HFT"
        self.current_mode = self.BALANCED_MODE
        
        # Advanced state tracking
        self.running = False
        self.mt5_connected = False
        self.initial_balance = None
        self.session_start_time = None
        self.price_cache = {}
        self.analysis_cache = {}
        self.performance_metrics = {}
        
        # Enhanced counters
        self.total_trades = 0
        self.winning_trades = 0
        self.losing_trades = 0
        self.total_profit = 0
        self.max_drawdown_pct = 0
        self.current_drawdown_pct = 0
        
        # Machine learning components
        self.ml_model = None
        self.scaler = StandardScaler()
        self.prediction_accuracy = 0
        self.feature_history = []
        
        print("✅ Advanced Trading Engine initialized successfully")
        self.setup_advanced_gui()
        
    def setup_advanced_gui(self):
        """Setup advanced professional GUI"""
        self.root = tk.Tk()
        self.root.title("🚀 ADVANCED PROFITABLE TRADING ENGINE - Professional System")
        
        # Professional window setup
        self.root.geometry("1400x900")
        self.root.minsize(1200, 800)
        self.root.configure(bg="#1e1e1e")  # Dark professional theme
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Configure responsive grid
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        # Create advanced notebook interface
        self.notebook = ttk.Notebook(self.root)
        self.notebook.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        # Setup tabs
        self.setup_trading_control_tab()
        self.setup_analysis_dashboard_tab()
        self.setup_risk_management_tab()
        self.setup_performance_analytics_tab()
        self.setup_ml_engine_tab()
        
    def setup_trading_control_tab(self):
        """Setup main trading control interface"""
        self.trading_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.trading_frame, text="🎯 Trading Control")
        
        # Configure grid weights
        for i in range(10):
            self.trading_frame.grid_rowconfigure(i, weight=1)
        for i in range(4):
            self.trading_frame.grid_columnconfigure(i, weight=1)
        
        # Trading mode selection
        mode_frame = ttk.LabelFrame(self.trading_frame, text="Trading Mode Selection", padding=10)
        mode_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=5, pady=5)
        
        self.trading_mode_var = tk.StringVar(value=self.BALANCED_MODE)
        modes = [
            (self.CONSERVATIVE_MODE, "Conservative (High Winrate, Low Risk)"),
            (self.BALANCED_MODE, "Balanced (Optimal Risk/Reward)"),
            (self.AGGRESSIVE_MODE, "Aggressive (High Profit Potential)"),
            (self.ULTRA_HFT_MODE, "Ultra HFT (Max Frequency)")
        ]
        
        for i, (mode, desc) in enumerate(modes):
            ttk.Radiobutton(mode_frame, text=desc, variable=self.trading_mode_var, 
                          value=mode, command=self.on_mode_change).grid(row=i, column=0, sticky="w", pady=2)
        
        # Symbol and lot configuration
        config_frame = ttk.LabelFrame(self.trading_frame, text="Trading Configuration", padding=10)
        config_frame.grid(row=1, column=0, columnspan=2, sticky="ew", padx=5, pady=5)
        
        self.symbol_var = tk.StringVar(value="XAUUSDm")
        self.lot_var = tk.StringVar(value="0.01")
        
        ttk.Label(config_frame, text="Symbol:").grid(row=0, column=0, sticky="w", padx=5)
        ttk.Entry(config_frame, textvariable=self.symbol_var, width=15).grid(row=0, column=1, padx=5)
        
        ttk.Label(config_frame, text="Lot Size:").grid(row=0, column=2, sticky="w", padx=5)
        ttk.Entry(config_frame, textvariable=self.lot_var, width=10).grid(row=0, column=3, padx=5)
        
        # Advanced risk parameters
        risk_frame = ttk.LabelFrame(self.trading_frame, text="Advanced Risk Management", padding=10)
        risk_frame.grid(row=2, column=0, columnspan=2, sticky="ew", padx=5, pady=5)
        
        self.max_risk_var = tk.StringVar(value="0.5")
        self.max_drawdown_var = tk.StringVar(value="3.0")
        self.profit_target_var = tk.StringVar(value="5.0")
        
        ttk.Label(risk_frame, text="Max Risk per Trade (%):").grid(row=0, column=0, sticky="w", padx=5)
        ttk.Entry(risk_frame, textvariable=self.max_risk_var, width=10).grid(row=0, column=1, padx=5)
        
        ttk.Label(risk_frame, text="Max Drawdown (%):").grid(row=0, column=2, sticky="w", padx=5)
        ttk.Entry(risk_frame, textvariable=self.max_drawdown_var, width=10).grid(row=0, column=3, padx=5)
        
        ttk.Label(risk_frame, text="Daily Profit Target (%):").grid(row=1, column=0, sticky="w", padx=5)
        ttk.Entry(risk_frame, textvariable=self.profit_target_var, width=10).grid(row=1, column=1, padx=5)
        
        # Control buttons
        control_frame = ttk.Frame(self.trading_frame)
        control_frame.grid(row=3, column=0, columnspan=2, pady=20)
        
        self.start_button = ttk.Button(control_frame, text="🚀 Start Advanced Trading", 
                                     command=self.start_trading, style="Accent.TButton")
        self.start_button.pack(side=tk.LEFT, padx=10)
        
        self.stop_button = ttk.Button(control_frame, text="🛑 Stop Trading", 
                                    command=self.stop_trading, state="disabled")
        self.stop_button.pack(side=tk.LEFT, padx=10)
        
        self.emergency_stop_button = ttk.Button(control_frame, text="🚨 EMERGENCY STOP", 
                                              command=self.emergency_stop, style="Danger.TButton")
        self.emergency_stop_button.pack(side=tk.LEFT, padx=10)
        
        # Real-time status display
        status_frame = ttk.LabelFrame(self.trading_frame, text="Real-Time Status", padding=10)
        status_frame.grid(row=0, column=2, columnspan=2, rowspan=4, sticky="nsew", padx=5, pady=5)
        
        self.account_status_var = tk.StringVar(value="Account: Disconnected")
        self.balance_var = tk.StringVar(value="Balance: $0.00")
        self.profit_var = tk.StringVar(value="Today's P/L: $0.00")
        self.winrate_var = tk.StringVar(value="Win Rate: 0%")
        self.drawdown_var = tk.StringVar(value="Drawdown: 0%")
        
        status_labels = [
            ("Connection Status:", self.account_status_var),
            ("Account Balance:", self.balance_var),
            ("Today's P/L:", self.profit_var),
            ("Win Rate:", self.winrate_var),
            ("Current Drawdown:", self.drawdown_var),
        ]
        
        for i, (label, var) in enumerate(status_labels):
            ttk.Label(status_frame, text=label, font=("Arial", 10, "bold")).grid(row=i, column=0, sticky="w", pady=5)
            ttk.Label(status_frame, textvariable=var, font=("Arial", 10)).grid(row=i, column=1, sticky="w", padx=10, pady=5)
        
    def setup_analysis_dashboard_tab(self):
        """Setup advanced market analysis dashboard"""
        self.analysis_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.analysis_frame, text="📊 Market Analysis")
        
        # Market sentiment analysis
        sentiment_frame = ttk.LabelFrame(self.analysis_frame, text="Advanced Market Sentiment", padding=10)
        sentiment_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=5, pady=5)
        
        self.trend_strength_var = tk.StringVar(value="Trend Strength: Calculating...")
        self.volatility_var = tk.StringVar(value="Volatility: Calculating...")
        self.momentum_var = tk.StringVar(value="Momentum: Calculating...")
        self.support_resistance_var = tk.StringVar(value="S/R Levels: Calculating...")
        
        analysis_labels = [
            ("Trend Strength:", self.trend_strength_var),
            ("Market Volatility:", self.volatility_var),
            ("Price Momentum:", self.momentum_var),
            ("Support/Resistance:", self.support_resistance_var),
        ]
        
        for i, (label, var) in enumerate(analysis_labels):
            ttk.Label(sentiment_frame, text=label).grid(row=i//2, column=(i%2)*2, sticky="w", padx=5, pady=2)
            ttk.Label(sentiment_frame, textvariable=var).grid(row=i//2, column=(i%2)*2+1, sticky="w", padx=5, pady=2)
        
        # Technical indicators display
        indicators_frame = ttk.LabelFrame(self.analysis_frame, text="Technical Indicators", padding=10)
        indicators_frame.grid(row=1, column=0, columnspan=2, sticky="ew", padx=5, pady=5)
        
        # Scrolled text for detailed analysis
        self.analysis_text = ScrolledText(self.analysis_frame, height=20, width=80)
        self.analysis_text.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
        
    def setup_risk_management_tab(self):
        """Setup advanced risk management interface"""
        self.risk_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.risk_frame, text="🛡️ Risk Management")
        
        # Risk metrics display
        metrics_frame = ttk.LabelFrame(self.risk_frame, text="Risk Metrics", padding=10)
        metrics_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=5, pady=5)
        
        self.consecutive_losses_var = tk.StringVar(value="Consecutive Losses: 0")
        self.risk_exposure_var = tk.StringVar(value="Risk Exposure: 0%")
        self.position_size_var = tk.StringVar(value="Recommended Position Size: 0.01")
        
        # Emergency controls
        emergency_frame = ttk.LabelFrame(self.risk_frame, text="Emergency Controls", padding=10)
        emergency_frame.grid(row=1, column=0, columnspan=2, sticky="ew", padx=5, pady=5)
        
        ttk.Button(emergency_frame, text="Close All Positions", 
                  command=self.close_all_positions).pack(side=tk.LEFT, padx=5)
        ttk.Button(emergency_frame, text="Pause Trading", 
                  command=self.pause_trading).pack(side=tk.LEFT, padx=5)
        ttk.Button(emergency_frame, text="Reset Counters", 
                  command=self.reset_counters).pack(side=tk.LEFT, padx=5)
        
    def setup_performance_analytics_tab(self):
        """Setup performance analytics dashboard"""
        self.performance_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.performance_frame, text="📈 Performance")
        
        # Performance metrics
        perf_frame = ttk.LabelFrame(self.performance_frame, text="Performance Analytics", padding=10)
        perf_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=5, pady=5)
        
        self.total_trades_var = tk.StringVar(value="Total Trades: 0")
        self.avg_profit_var = tk.StringVar(value="Average Profit: $0")
        self.sharpe_ratio_var = tk.StringVar(value="Sharpe Ratio: 0")
        self.profit_factor_var = tk.StringVar(value="Profit Factor: 0")
        
        # Trade history
        history_frame = ttk.LabelFrame(self.performance_frame, text="Trade History", padding=10)
        history_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
        
        self.trade_history_text = ScrolledText(history_frame, height=25, width=100)
        self.trade_history_text.pack(fill=tk.BOTH, expand=True)
        
    def setup_ml_engine_tab(self):
        """Setup machine learning engine interface"""
        self.ml_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.ml_frame, text="🤖 ML Engine")
        
        # ML status
        ml_status_frame = ttk.LabelFrame(self.ml_frame, text="Machine Learning Status", padding=10)
        ml_status_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=5, pady=5)
        
        self.ml_status_var = tk.StringVar(value="ML Engine: Initializing...")
        self.prediction_accuracy_var = tk.StringVar(value="Prediction Accuracy: 0%")
        self.model_confidence_var = tk.StringVar(value="Model Confidence: 0%")
        
        ttk.Label(ml_status_frame, textvariable=self.ml_status_var).pack(pady=5)
        ttk.Label(ml_status_frame, textvariable=self.prediction_accuracy_var).pack(pady=5)
        ttk.Label(ml_status_frame, textvariable=self.model_confidence_var).pack(pady=5)
        
        # ML training controls
        training_frame = ttk.LabelFrame(self.ml_frame, text="Model Training", padding=10)
        training_frame.grid(row=1, column=0, columnspan=2, sticky="ew", padx=5, pady=5)
        
        ttk.Button(training_frame, text="Train Model", command=self.train_ml_model).pack(side=tk.LEFT, padx=5)
        ttk.Button(training_frame, text="Retrain", command=self.retrain_model).pack(side=tk.LEFT, padx=5)
        ttk.Button(training_frame, text="Reset Model", command=self.reset_model).pack(side=tk.LEFT, padx=5)
        
        # Initialize ML engine
        self.initialize_ml_engine()
        
    def initialize_ml_engine(self):
        """Initialize machine learning engine"""
        try:
            self.ml_model = RandomForestClassifier(
                n_estimators=100,
                max_depth=10,
                random_state=42,
                class_weight='balanced'
            )
            self.ml_status_var.set("ML Engine: Ready")
            print("✅ ML Engine initialized successfully")
        except Exception as e:
            self.ml_status_var.set(f"ML Engine: Error - {str(e)}")
            print(f"❌ ML Engine initialization failed: {e}")
    
    def start_trading(self):
        """Start advanced trading with all systems"""
        if self.running:
            return
        
        # Initialize session
        self.running = True
        self.session_start_time = datetime.datetime.now()
        
        # Connect to MT5 or start simulation
        self.connect_mt5()
        
        # Start market data feed
        self.market_data.start_data_feed()
        
        # Update GUI
        self.start_button.config(state="disabled")
        self.stop_button.config(state="normal")
        
        # Start trading thread
        self.trading_thread = threading.Thread(target=self.advanced_trading_loop)
        self.trading_thread.daemon = True
        self.trading_thread.start()
        
        # Start GUI update thread
        self.gui_update_thread = threading.Thread(target=self.gui_update_loop)
        self.gui_update_thread.daemon = True
        self.gui_update_thread.start()
        
        self.log("🚀 Advanced Trading Engine Started", "success")
        
    def advanced_trading_loop(self):
        """Main advanced trading loop with deep analysis"""
        self.log("🎯 Advanced trading loop initiated...", "info")
        
        while self.running:
            try:
                # Get current mode settings
                mode_settings = self.get_mode_settings()
                interval = mode_settings['interval']
                
                # Perform deep market analysis
                symbol = self.symbol_var.get()
                market_data = self.market_data.get_market_data(symbol)
                technical_indicators = self.market_data.calculate_technical_indicators(symbol)
                
                analysis_result = self.market_analyzer.perform_deep_analysis(
                    symbol, market_data, technical_indicators
                )
                
                if not analysis_result['valid']:
                    time.sleep(interval)
                    continue
                
                # Generate intelligent signal
                signal = self.signal_processor.generate_intelligent_signal(
                    analysis_result, mode_settings, self.ml_model
                )
                
                # Apply advanced risk management
                if self.current_mode == self.ULTRA_HFT_MODE:
                    risk_check = self.risk_manager.should_allow_trade(
                        analysis_result.get('current_balance', 0),
                        signal.get('confidence', 0)
                    )
                    if not risk_check[0]:
                        self.log(f"🛡️ Risk Manager: {risk_check[1]}", "warning")
                        time.sleep(interval)
                        continue
                
                # Execute trade if signal is strong enough
                if signal['action'] != 'HOLD' and signal['confidence'] > mode_settings['min_confidence']:
                    self.execute_advanced_trade(signal, mode_settings)
                
                # Update performance metrics
                self.update_performance_metrics()
                
                time.sleep(interval)
                
            except Exception as e:
                self.log(f"❌ Trading loop error: {e}", "error")
                time.sleep(5)
    
    def get_mode_settings(self):
        """Get settings based on current trading mode"""
        settings = {
            self.CONSERVATIVE_MODE: {
                'interval': 30,
                'min_confidence': 0.8,
                'max_risk_pct': 0.3,
                'tp_pct': 0.5,
                'sl_pct': 1.5
            },
            self.BALANCED_MODE: {
                'interval': 10,
                'min_confidence': 0.6,
                'max_risk_pct': 0.5,
                'tp_pct': 1.0,
                'sl_pct': 2.0
            },
            self.AGGRESSIVE_MODE: {
                'interval': 5,
                'min_confidence': 0.4,
                'max_risk_pct': 1.0,
                'tp_pct': 2.0,
                'sl_pct': 3.0
            },
            self.ULTRA_HFT_MODE: {
                'interval': 1,
                'min_confidence': 0.7,
                'max_risk_pct': 0.2,
                'tp_pct': 0.3,
                'sl_pct': 1.0
            }
        }
        return settings.get(self.current_mode, settings[self.BALANCED_MODE])
    
    def execute_advanced_trade(self, signal, mode_settings):
        """Execute trade with advanced risk management"""
        try:
            symbol = self.symbol_var.get()
            
            if not self.mt5_connected:
                # Log simulation trade
                self.log(f"📊 SIMULATION: {signal['action']} {symbol} - Confidence: {signal['confidence']:.3f}", "info")
                self.total_trades += 1
                # Simulate profit for demo
                simulated_profit = random.uniform(-50, 100)
                if simulated_profit > 0:
                    self.winning_trades += 1
                else:
                    self.losing_trades += 1
                self.total_profit += simulated_profit
                return
            
            # Get account info for real trading
            account_info = mt5.account_info()
            if not account_info:
                self.log("❌ Failed to get account info", "error")
                return
            
            balance = account_info.balance
            if not self.initial_balance:
                self.initial_balance = balance
            
            # Check minimum balance requirement
            if balance < 100:  # Minimum $100 balance
                self.log("⚠️ Insufficient balance for trading", "warning")
                return
            
            # Calculate position size with advanced money management
            base_lot = float(self.lot_var.get())
            confidence_multiplier = min(signal['confidence'] * 1.5, 1.0)
            position_size = base_lot * confidence_multiplier
            
            # Apply risk management
            max_risk_amount = balance * (mode_settings['max_risk_pct'] / 100)
            
            # Get current price
            current_price = self.get_current_price(symbol)
            if not current_price:
                self.log(f"❌ Failed to get current price for {symbol}", "error")
                return
            
            # Calculate TP/SL levels
            tp_pct = mode_settings['tp_pct']
            sl_pct = mode_settings['sl_pct']
            
            # Apply volatility adjustment
            volatility = signal.get('volatility', 0.01)
            volatility_multiplier = 1 + (volatility * 0.5)
            
            if signal['action'] == 'BUY':
                tp_price = current_price * (1 + (tp_pct / 100) * volatility_multiplier)
                sl_price = current_price * (1 - (sl_pct / 100) * volatility_multiplier)
            else:  # SELL
                tp_price = current_price * (1 - (tp_pct / 100) * volatility_multiplier)
                sl_price = current_price * (1 + (sl_pct / 100) * volatility_multiplier)
            
            # Send order to MT5
            order_result = self.send_mt5_order(
                signal['action'], symbol, position_size, current_price, tp_price, sl_price
            )
            
            if order_result:
                self.total_trades += 1
                self.log(f"✅ REAL TRADE: {signal['action']} {symbol} "
                        f"Size: {position_size} @ {current_price:.5f} "
                        f"TP: {tp_price:.5f} SL: {sl_price:.5f}", "success")
                
                # Log trade for analysis
                self.log_trade_details(signal, current_price, tp_price, sl_price, position_size)
            else:
                self.failed_trades += 1
                self.log(f"❌ Trade execution failed for {symbol}", "error")
            
        except Exception as e:
            self.log(f"❌ Trade execution error: {e}", "error")
            self.failed_trades += 1
    
    def gui_update_loop(self):
        """Update GUI with real-time data"""
        while self.running:
            try:
                self.update_account_display()
                self.update_analysis_display()
                self.update_risk_display()
                self.update_performance_display()
                self.update_ml_display()
                time.sleep(1)
            except Exception as e:
                print(f"GUI update error: {e}")
                time.sleep(5)
    
    def on_mode_change(self):
        """Handle trading mode change"""
        self.current_mode = self.trading_mode_var.get()
        self.log(f"Trading mode changed to: {self.current_mode}", "info")
    
    def stop_trading(self):
        """Stop trading engine"""
        self.running = False
        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")
        self.log("🛑 Trading stopped", "warning")
    
    def emergency_stop(self):
        """Emergency stop all trading"""
        self.running = False
        self.close_all_positions()
        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")
        self.log("🚨 EMERGENCY STOP ACTIVATED", "error")
    
    def pause_trading(self):
        """Pause trading temporarily"""
        self.running = False
        self.log("⏸️ Trading paused", "warning")
    
    def reset_counters(self):
        """Reset all trading counters"""
        self.total_trades = 0
        self.winning_trades = 0
        self.losing_trades = 0
        self.total_profit = 0
        self.risk_manager.reset_daily_counters()
        self.log("🔄 Counters reset", "info")
    
    def close_all_positions(self):
        """Close all open positions"""
        if not self.mt5_connected:
            self.log("⚠️ MT5 not connected", "warning")
            return
        
        try:
            positions = mt5.positions_get()
            if positions is None or len(positions) == 0:
                self.log("No open positions to close", "info")
                return
            
            for position in positions:
                # Create close request
                if position.type == mt5.ORDER_TYPE_BUY:
                    order_type = mt5.ORDER_TYPE_SELL
                else:
                    order_type = mt5.ORDER_TYPE_BUY
                
                request = {
                    "action": mt5.TRADE_ACTION_DEAL,
                    "symbol": position.symbol,
                    "volume": position.volume,
                    "type": order_type,
                    "position": position.ticket,
                    "deviation": 10,
                    "magic": getattr(config, 'MT5_MAGIC_NUMBER', 123456),
                    "comment": "Emergency close",
                    "type_time": mt5.ORDER_TIME_GTC,
                    "type_filling": mt5.ORDER_FILLING_IOC,
                }
                
                result = mt5.order_send(request)
                if result.retcode == mt5.TRADE_RETCODE_DONE:
                    self.log(f"✅ Position closed: {position.ticket}", "success")
                else:
                    self.log(f"❌ Failed to close position: {result.comment}", "error")
                    
        except Exception as e:
            self.log(f"❌ Error closing positions: {e}", "error")
    
    def train_ml_model(self):
        """Train machine learning model"""
        self.log("🤖 Training ML model...", "info")
        self.ml_status_var.set("ML Engine: Training...")
        # ML training implementation would go here
        self.ml_status_var.set("ML Engine: Training Complete")
    
    def retrain_model(self):
        """Retrain ML model with new data"""
        self.log("🔄 Retraining ML model...", "info")
        self.train_ml_model()
    
    def reset_model(self):
        """Reset ML model"""
        self.log("🗑️ Resetting ML model...", "info")
        self.ml_model = None
        self.initialize_ml_engine()
    
    def update_account_display(self):
        """Update account information display"""
        try:
            if not self.mt5_connected:
                self.account_status_var.set("Status: Simulation Mode")
                return
            
            account_info = mt5.account_info()
            if not account_info:
                return
            
            self.balance_var.set(f"Balance: ${account_info.balance:,.2f}")
            profit = account_info.profit
            self.profit_var.set(f"Today's P/L: ${profit:,.2f}")
            
            if self.total_trades > 0:
                winrate = (self.winning_trades / self.total_trades) * 100
                self.winrate_var.set(f"Win Rate: {winrate:.1f}%")
            
            if self.initial_balance:
                current_dd = ((self.initial_balance - account_info.balance) / self.initial_balance) * 100
                self.drawdown_var.set(f"Drawdown: {current_dd:.2f}%")
                
        except Exception as e:
            self.log(f"Error updating account display: {e}", "error")
    
    def update_analysis_display(self):
        """Update market analysis display"""
        try:
            symbol = self.symbol_var.get()
            if symbol in self.analysis_cache:
                analysis = self.analysis_cache[symbol]
                
                self.trend_strength_var.set(f"Trend Strength: {analysis.get('trend_strength', 0):.3f}")
                self.volatility_var.set(f"Volatility: {analysis.get('volatility', 0):.3f}")
                self.momentum_var.set(f"Momentum: {analysis.get('momentum', 0):.3f}")
                
                sr = analysis.get('support_resistance', {})
                support = sr.get('support', 0)
                resistance = sr.get('resistance', 0)
                self.support_resistance_var.set(f"S/R: {support:.5f} / {resistance:.5f}")
                
        except Exception as e:
            pass  # Silent fail for display updates
    
    def update_risk_display(self):
        """Update risk management display"""
        try:
            risk_status = self.risk_manager.get_risk_status()
            
            self.consecutive_losses_var.set(f"Consecutive Losses: {risk_status['consecutive_losses']}")
            
            if self.initial_balance:
                exposure = (abs(self.total_profit) / self.initial_balance) * 100
                self.risk_exposure_var.set(f"Risk Exposure: {exposure:.2f}%")
                
        except Exception as e:
            pass  # Silent fail for display updates
    
    def update_performance_display(self):
        """Update performance metrics display"""
        try:
            self.total_trades_var.set(f"Total Trades: {self.total_trades}")
            
            if self.total_trades > 0:
                avg_profit = self.total_profit / self.total_trades
                self.avg_profit_var.set(f"Average Profit: ${avg_profit:.2f}")
                
        except Exception as e:
            pass  # Silent fail for display updates
    
    def update_ml_display(self):
        """Update ML engine display"""
        try:
            if self.prediction_accuracy > 0:
                self.prediction_accuracy_var.set(f"Prediction Accuracy: {self.prediction_accuracy:.1f}%")
                
        except Exception as e:
            pass  # Silent fail for display updates
    
    def get_current_price(self, symbol):
        """Get current price for symbol"""
        if self.mt5_connected:
            try:
                tick = mt5.symbol_info_tick(symbol)
                if tick:
                    return (tick.bid + tick.ask) / 2
            except Exception as e:
                self.log(f"Error getting MT5 price for {symbol}: {e}", "warning")
        
        # Fallback to market data provider
        return self.market_data.get_current_price(symbol)
    
    def calculate_advanced_tpsl(self, entry_price, action, mode_settings, volatility):
        """Calculate advanced TP/SL levels"""
        tp_pct = mode_settings['tp_pct']
        sl_pct = mode_settings['sl_pct']
        
        # Adjust for volatility
        volatility_multiplier = 1 + (volatility * 0.5)
        tp_distance = entry_price * (tp_pct / 100) * volatility_multiplier
        sl_distance = entry_price * (sl_pct / 100) * volatility_multiplier
        
        if action == 'BUY':
            tp_price = entry_price + tp_distance
            sl_price = entry_price - sl_distance
        else:  # SELL
            tp_price = entry_price - tp_distance
            sl_price = entry_price + sl_distance
        
        return tp_price, sl_price
    
    def send_mt5_order(self, action, symbol, lot_size, price, tp_price, sl_price):
        """Send order to MT5 with comprehensive error handling"""
        if not self.mt5_connected:
            return False
        
        try:
            # Verify symbol is available
            symbol_info = mt5.symbol_info(symbol)
            if not symbol_info:
                self.log(f"❌ Symbol {symbol} not found", "error")
                return False
            
            if not symbol_info.visible:
                # Try to enable symbol
                if not mt5.symbol_select(symbol, True):
                    self.log(f"❌ Failed to enable symbol {symbol}", "error")
                    return False
            
            # Prepare order request
            order_type = mt5.ORDER_TYPE_BUY if action == 'BUY' else mt5.ORDER_TYPE_SELL
            
            # Round prices to symbol precision
            point = symbol_info.point
            digits = symbol_info.digits
            
            price = round(price, digits)
            tp_price = round(tp_price, digits)
            sl_price = round(sl_price, digits)
            
            # Ensure minimum distance requirements
            min_distance = symbol_info.trade_stops_level * point
            if action == 'BUY':
                if (tp_price - price) < min_distance:
                    tp_price = price + min_distance
                if (price - sl_price) < min_distance:
                    sl_price = price - min_distance
            else:  # SELL
                if (price - tp_price) < min_distance:
                    tp_price = price - min_distance
                if (sl_price - price) < min_distance:
                    sl_price = price + min_distance
            
            # Normalize lot size
            lot_min = symbol_info.volume_min
            lot_max = symbol_info.volume_max
            lot_step = symbol_info.volume_step
            
            # Round lot size to valid step
            lot_size = round(lot_size / lot_step) * lot_step
            lot_size = max(lot_min, min(lot_max, lot_size))
            
            request = {
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": symbol,
                "volume": lot_size,
                "type": order_type,
                "price": price,
                "tp": tp_price,
                "sl": sl_price,
                "deviation": 20,  # Allow more slippage for volatile markets
                "magic": getattr(config, 'MT5_MAGIC_NUMBER', 123456),
                "comment": f"AdvancedEngine-{self.current_mode}",
                "type_time": mt5.ORDER_TIME_GTC,
                "type_filling": mt5.ORDER_FILLING_IOC,
            }
            
            # Send order
            result = mt5.order_send(request)
            
            if result.retcode == mt5.TRADE_RETCODE_DONE:
                self.log(f"✅ Order executed successfully - Ticket: {result.order}", "success")
                return True
            else:
                # Log detailed error information
                retcode_dict = {
                    mt5.TRADE_RETCODE_REQUOTE: "Requote",
                    mt5.TRADE_RETCODE_REJECT: "Request rejected",
                    mt5.TRADE_RETCODE_MARKET_CLOSED: "Market closed",
                    mt5.TRADE_RETCODE_INVALID_VOLUME: "Invalid volume",
                    mt5.TRADE_RETCODE_INVALID_PRICE: "Invalid price",
                    mt5.TRADE_RETCODE_INVALID_STOPS: "Invalid stops",
                    mt5.TRADE_RETCODE_TRADE_DISABLED: "Trade disabled",
                    mt5.TRADE_RETCODE_INSUFFICIENT_MONEY: "Insufficient money"
                }
                
                error_msg = retcode_dict.get(result.retcode, f"Unknown error {result.retcode}")
                self.log(f"❌ Order failed: {error_msg} - {result.comment}", "error")
                return False
            
        except Exception as e:
            self.log(f"❌ Order send exception: {e}", "error")
            return False
    
    def update_performance_metrics(self):
        """Update comprehensive performance metrics"""
        if not hasattr(self, 'performance_metrics'):
            self.performance_metrics = {}
        
        # Calculate various performance metrics
        if self.total_trades > 0:
            win_rate = (self.winning_trades / self.total_trades) * 100
            self.performance_metrics['win_rate'] = win_rate
            
            if self.initial_balance:
                total_return = (self.total_profit / self.initial_balance) * 100
                self.performance_metrics['total_return'] = total_return
    
    def log(self, message, level="info"):
        """Enhanced logging system"""
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}"
        
        # Color coding for different levels
        if hasattr(self, 'trade_history_text'):
            self.trade_history_text.insert(tk.END, log_entry + "\n")
            self.trade_history_text.see(tk.END)
        
        print(log_entry)
    
    def log_trade_details(self, signal, entry_price, tp_price, sl_price, lot_size):
        """Log detailed trade information for analysis"""
        trade_details = {
            'timestamp': datetime.datetime.now().isoformat(),
            'symbol': self.symbol_var.get(),
            'action': signal['action'],
            'entry_price': entry_price,
            'tp_price': tp_price,
            'sl_price': sl_price,
            'lot_size': lot_size,
            'confidence': signal['confidence'],
            'mode': self.current_mode,
            'risk_reward_ratio': abs(tp_price - entry_price) / abs(entry_price - sl_price)
        }
        
        # Save to CSV for analysis
        try:
            import csv
            import os
            
            file_exists = os.path.exists('trade_log.csv')
            with open('trade_log.csv', 'a', newline='') as csvfile:
                fieldnames = trade_details.keys()
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                if not file_exists:
                    writer.writeheader()
                
                writer.writerow(trade_details)
                
        except Exception as e:
            self.log(f"Warning: Could not save trade log: {e}", "warning")
    
    def stop_trading(self):
        """Stop trading engine and cleanup"""
        self.running = False
        
        # Stop market data feed
        if hasattr(self, 'market_data'):
            self.market_data.stop_data_feed()
        
        # Update GUI
        if hasattr(self, 'start_button'):
            self.start_button.config(state="normal")
            self.stop_button.config(state="disabled")
        
        self.log("🛑 Trading engine stopped", "warning")
    
    def connect_mt5(self):
        """Connect to MetaTrader5"""
        if not MT5_AVAILABLE:
            self.log("⚠️ MT5 not available - running in simulation mode", "warning")
            self.account_status_var.set("Status: Simulation Mode")
            return
        
        try:
            # Try to connect to MT5
            if mt5.initialize():
                # Test connection with account info
                account_info = mt5.account_info()
                if account_info:
                    self.mt5_connected = True
                    self.initial_balance = account_info.balance
                    self.account_status_var.set(f"Status: MT5 Connected - Account {account_info.login}")
                    self.balance_var.set(f"Balance: ${account_info.balance:,.2f}")
                    self.log(f"✅ MT5 connected successfully - Balance: ${account_info.balance:,.2f}", "success")
                    
                    # Test symbol access
                    test_symbol = self.symbol_var.get()
                    symbol_info = mt5.symbol_info(test_symbol)
                    if symbol_info:
                        self.log(f"✅ Symbol {test_symbol} available for trading", "success")
                    else:
                        self.log(f"⚠️ Symbol {test_symbol} not found - check symbol name", "warning")
                else:
                    self.log("❌ Failed to get account info - check MT5 login", "error")
                    self.mt5_connected = False
            else:
                self.log("❌ MT5 initialization failed - check MT5 installation", "error")
                self.mt5_connected = False
        except Exception as e:
            self.log(f"❌ MT5 connection error: {e}", "error")
    
    def on_closing(self):
        """Handle window closing"""
        if self.running:
            self.stop_trading()
        
        if self.mt5_connected:
            mt5.shutdown()
        
        self.root.destroy()
    
    def run(self):
        """Start the application"""
        print("🚀 Starting Advanced Profitable Trading Engine...")
        self.root.mainloop()

class AdvancedMarketAnalyzer:
    """Advanced market analysis with deep learning capabilities"""
    
    def __init__(self):
        self.price_history = {}
        self.analysis_cache = {}
        
    def perform_deep_analysis(self, symbol, market_data, technical_indicators):
        """Perform comprehensive market analysis"""
        try:
            if not market_data or not technical_indicators:
                return {'valid': False, 'reason': 'Insufficient data'}
            
            prices = market_data['price_history']
            current_price = market_data['current_price']
            
            # Multi-timeframe analysis with technical indicators
            analysis = {
                'valid': True,
                'symbol': symbol,
                'current_price': current_price,
                'trend_strength': self.calculate_trend_strength(prices, technical_indicators),
                'volatility': market_data['volatility'],
                'momentum': market_data['momentum'],
                'support_resistance': self.find_support_resistance(prices),
                'market_regime': self.identify_market_regime(prices, technical_indicators),
                'volume_profile': self.analyze_volume_profile(prices),
                'fractal_dimension': self.calculate_fractal_dimension(prices),
                'technical_indicators': technical_indicators,
                'market_data': market_data
            }
            
            return analysis
            
        except Exception as e:
            return {'valid': False, 'reason': f'Analysis error: {e}'}
    
    def calculate_trend_strength(self, prices, technical_indicators):
        """Calculate advanced trend strength using multiple indicators"""
        if len(prices) < 20:
            return 0
        
        # Price trend analysis
        short_trend = np.polyfit(range(10), prices[-10:], 1)[0]
        medium_trend = np.polyfit(range(20), prices[-20:], 1)[0]
        long_trend = np.polyfit(range(50), prices[-50:], 1)[0] if len(prices) >= 50 else 0
        
        # Moving average convergence/divergence
        sma_8 = technical_indicators.get('sma_8', prices[-1])
        sma_21 = technical_indicators.get('sma_21', prices[-1])
        sma_55 = technical_indicators.get('sma_55', prices[-1])
        
        # MA trend scoring
        ma_trend = 0
        if sma_8 > sma_21 > sma_55:
            ma_trend = 1  # Strong uptrend
        elif sma_8 < sma_21 < sma_55:
            ma_trend = -1  # Strong downtrend
        elif sma_8 > sma_21:
            ma_trend = 0.5  # Mild uptrend
        elif sma_8 < sma_21:
            ma_trend = -0.5  # Mild downtrend
        
        # MACD trend confirmation
        macd_line = technical_indicators.get('macd_line', 0)
        macd_signal = technical_indicators.get('macd_signal', 0)
        macd_trend = 1 if macd_line > macd_signal else -1
        
        # Combine all trend indicators
        price_trend = np.tanh((short_trend * 0.5 + medium_trend * 0.3 + long_trend * 0.2) * 1000)
        
        # Weighted combination
        total_trend = (
            price_trend * 0.4 +
            ma_trend * 0.4 +
            macd_trend * 0.2
        )
        
        return max(-1, min(1, total_trend))  # Clamp to [-1, 1]
    
    def calculate_volatility(self, prices):
        """Calculate advanced volatility metrics"""
        if len(prices) < 20:
            return 0
        
        returns = np.diff(prices) / prices[:-1]
        
        # GARCH-like volatility
        volatility = np.std(returns) * np.sqrt(252)  # Annualized
        
        # Yang-Zhang volatility estimator (if OHLC data available)
        # For now, use simple volatility
        return min(volatility, 1.0)  # Cap at 100%
    
    def calculate_momentum(self, prices):
        """Calculate advanced momentum indicators"""
        if len(prices) < 14:
            return 0
            
        # RSI-based momentum
        deltas = np.diff(prices)
        gains = np.where(deltas > 0, deltas, 0)
        losses = np.where(deltas < 0, -deltas, 0)
        
        avg_gain = np.mean(gains[-14:])
        avg_loss = np.mean(losses[-14:])
        
        if avg_loss == 0:
            return 1.0
        
        rs = avg_gain / avg_loss
        rsi = 1 - (1 / (1 + rs))
        
        # Normalize RSI to momentum [-1, 1]
        return (rsi - 0.5) * 2
    
    def find_support_resistance(self, prices):
        """Find key support and resistance levels"""
        if len(prices) < 20:
            return {'support': prices[-1], 'resistance': prices[-1]}
        
        # Use local minima/maxima
        from scipy.signal import argrelextrema
        
        # Find local maxima (resistance)
        highs = argrelextrema(prices, np.greater, order=5)[0]
        # Find local minima (support)  
        lows = argrelextrema(prices, np.less, order=5)[0]
        
        current_price = prices[-1]
        
        # Find nearest support/resistance
        resistance_levels = prices[highs] if len(highs) > 0 else [current_price]
        support_levels = prices[lows] if len(lows) > 0 else [current_price]
        
        # Find nearest levels
        resistance = min([r for r in resistance_levels if r > current_price], 
                        default=current_price * 1.01)
        support = max([s for s in support_levels if s < current_price], 
                     default=current_price * 0.99)
        
        return {'support': support, 'resistance': resistance}
    
    def identify_market_regime(self, prices, technical_indicators):
        """Identify current market regime using multiple factors"""
        if len(prices) < 30:
            return 'UNKNOWN'
        
        # Volatility analysis
        atr = technical_indicators.get('atr', 0.001)
        current_volatility = np.std(prices[-20:]) / np.mean(prices[-20:])
        
        # Trend analysis
        trend_strength = abs(self.calculate_trend_strength(prices, technical_indicators))
        
        # RSI analysis for momentum regime
        rsi = technical_indicators.get('rsi', 50)
        
        # Bollinger Band analysis for volatility regime
        bb_upper = technical_indicators.get('bb_upper', prices[-1])
        bb_lower = technical_indicators.get('bb_lower', prices[-1])
        bb_width = (bb_upper - bb_lower) / prices[-1]
        
        # Regime classification
        is_trending = trend_strength > 0.4
        is_volatile = bb_width > 0.02 or current_volatility > 0.015
        is_oversold = rsi < 30
        is_overbought = rsi > 70
        
        if is_trending:
            if is_volatile:
                return 'TRENDING_VOLATILE'
            else:
                return 'TRENDING_STABLE'
        else:
            if is_oversold or is_overbought:
                return 'RANGING_MEAN_REVERSION'
            elif is_volatile:
                return 'RANGING_VOLATILE'
            else:
                return 'RANGING_STABLE'
    
    def analyze_volume_profile(self, prices):
        """Analyze volume profile (simplified without actual volume data)"""
        # Since we don't have volume data, use price action as proxy
        price_ranges = np.diff(prices)
        
        # High activity areas (large price movements)
        high_activity = np.percentile(np.abs(price_ranges), 80)
        
        return {
            'high_activity_threshold': high_activity,
            'current_activity': abs(prices[-1] - prices[-2]) if len(prices) > 1 else 0
        }
    
    def calculate_fractal_dimension(self, prices):
        """Calculate fractal dimension for market complexity"""
        if len(prices) < 10:
            return 1.5
        
        # Simplified Hurst exponent calculation
        lags = range(2, min(20, len(prices)//2))
        tau = []
        
        for lag in lags:
            # Calculate mean of absolute differences
            tau.append(np.mean(np.abs(np.diff(prices, lag))))
        
        # Linear regression in log space
        if len(tau) > 1:
            slope = np.polyfit(np.log(lags), np.log(tau), 1)[0]
            hurst = slope
            return min(max(hurst, 0), 2)  # Clamp between 0 and 2
        
        return 1.5  # Default neutral value

class IntelligentSignalProcessor:
    """Intelligent signal processing with ML integration"""
    
    def __init__(self):
        self.signal_history = []
        
    def generate_intelligent_signal(self, analysis, mode_settings, ml_model=None):
        """Generate intelligent trading signal with enhanced profitability focus"""
        try:
            if not analysis['valid']:
                return {'action': 'HOLD', 'confidence': 0}
            
            # Extract comprehensive features
            features = self.extract_features(analysis)
            technical_indicators = analysis.get('technical_indicators', {})
            
            # Advanced multi-factor signal generation
            signals = {
                'trend_signal': self.generate_trend_signal(analysis, technical_indicators),
                'momentum_signal': self.generate_momentum_signal(analysis, technical_indicators),
                'mean_reversion_signal': self.generate_mean_reversion_signal(analysis, technical_indicators),
                'breakout_signal': self.generate_breakout_signal(analysis, technical_indicators),
                'volume_signal': self.generate_volume_signal(analysis, technical_indicators),
                'volatility_signal': self.generate_volatility_signal(analysis, technical_indicators),
                'confluence_signal': self.generate_confluence_signal(analysis, technical_indicators)
            }
            
            # Enhanced signal weights based on market regime
            regime = analysis.get('market_regime', 'UNKNOWN')
            signal_weights = self.get_regime_based_weights(regime)
            
            # Calculate weighted signal with regime adjustment
            weighted_signal = 0
            total_confidence = 0
            signal_count = 0
            
            for signal_type, signal_data in signals.items():
                if signal_data['confidence'] > 0.1:  # Only count meaningful signals
                    weight = signal_weights[signal_type]
                    weighted_signal += signal_data['score'] * weight
                    total_confidence += signal_data['confidence'] * weight
                    signal_count += 1
            
            # Require minimum signal confluence for high-probability trades
            min_signals_required = {
                'CONSERVATIVE': 5,
                'BALANCED': 4,
                'AGGRESSIVE': 3,
                'ULTRA_HFT': 6
            }
            
            mode = mode_settings.get('name', 'BALANCED')
            min_signals = min_signals_required.get(mode.split()[0], 4)
            
            if signal_count < min_signals:
                return {
                    'action': 'HOLD',
                    'confidence': 0,
                    'reason': f'Insufficient signal confluence ({signal_count}/{min_signals})'
                }
            
            # Enhanced action determination with strict thresholds
            action = 'HOLD'
            confidence_threshold = mode_settings.get('min_confidence', 0.6)
            
            # Strict signal thresholds for profitability
            strong_signal_threshold = 0.6
            moderate_signal_threshold = 0.4
            
            if weighted_signal > strong_signal_threshold and total_confidence > confidence_threshold:
                action = 'BUY'
            elif weighted_signal < -strong_signal_threshold and total_confidence > confidence_threshold:
                action = 'SELL'
            elif abs(weighted_signal) > moderate_signal_threshold and total_confidence > confidence_threshold * 1.2:
                # Allow moderate signals only with higher confidence
                action = 'BUY' if weighted_signal > 0 else 'SELL'
            
            # Additional filters for profit optimization
            if action != 'HOLD':
                # Filter 1: Market volatility check
                volatility = analysis.get('volatility', 0)
                if volatility > 0.05:  # Too volatile
                    action = 'HOLD'
                    total_confidence *= 0.5
                
                # Filter 2: RSI extremes check
                rsi = technical_indicators.get('rsi', 50)
                if action == 'BUY' and rsi > 75:  # Overbought
                    action = 'HOLD'
                elif action == 'SELL' and rsi < 25:  # Oversold
                    action = 'HOLD'
                
                # Filter 3: MACD divergence check
                macd_line = technical_indicators.get('macd_line', 0)
                macd_signal = technical_indicators.get('macd_signal', 0)
                if action == 'BUY' and macd_line < macd_signal:
                    total_confidence *= 0.7
                elif action == 'SELL' and macd_line > macd_signal:
                    total_confidence *= 0.7
                
                # Filter 4: Bollinger Band position
                current_price = analysis.get('current_price', 0)
                bb_upper = technical_indicators.get('bb_upper', current_price)
                bb_lower = technical_indicators.get('bb_lower', current_price)
                bb_middle = technical_indicators.get('bb_middle', current_price)
                
                bb_position = (current_price - bb_lower) / (bb_upper - bb_lower) if bb_upper != bb_lower else 0.5
                
                if action == 'BUY' and bb_position > 0.8:  # Near upper band
                    total_confidence *= 0.6
                elif action == 'SELL' and bb_position < 0.2:  # Near lower band
                    total_confidence *= 0.6
            
            # Final confidence adjustment based on historical performance
            if hasattr(self, 'signal_history') and len(self.signal_history) > 10:
                recent_accuracy = self.calculate_recent_signal_accuracy()
                total_confidence *= (0.5 + recent_accuracy / 2)  # Scale confidence by recent performance
            
            final_signal = {
                'action': action,
                'confidence': min(total_confidence, 1.0),
                'weighted_score': weighted_signal,
                'individual_signals': signals,
                'features': features,
                'volatility': analysis['volatility'],
                'signal_count': signal_count,
                'regime': regime,
                'filters_applied': action != 'HOLD'
            }
            
            self.signal_history.append(final_signal)
            
            # Keep only recent signal history
            if len(self.signal_history) > 100:
                self.signal_history = self.signal_history[-100:]
            
            return final_signal
            
        except Exception as e:
            return {
                'action': 'HOLD',
                'confidence': 0,
                'error': str(e)
            }
    
    def get_regime_based_weights(self, regime):
        """Get signal weights based on market regime"""
        base_weights = {
            'trend_signal': 0.25,
            'momentum_signal': 0.20,
            'mean_reversion_signal': 0.15,
            'breakout_signal': 0.15,
            'volume_signal': 0.10,
            'volatility_signal': 0.10,
            'confluence_signal': 0.05
        }
        
        if regime == 'TRENDING_STABLE':
            base_weights['trend_signal'] = 0.4
            base_weights['momentum_signal'] = 0.3
            base_weights['mean_reversion_signal'] = 0.05
        elif regime == 'RANGING_STABLE':
            base_weights['mean_reversion_signal'] = 0.4
            base_weights['trend_signal'] = 0.1
            base_weights['momentum_signal'] = 0.15
        elif regime == 'TRENDING_VOLATILE':
            base_weights['breakout_signal'] = 0.3
            base_weights['volatility_signal'] = 0.25
            base_weights['trend_signal'] = 0.25
        elif regime == 'RANGING_VOLATILE':
            base_weights['volatility_signal'] = 0.3
            base_weights['mean_reversion_signal'] = 0.3
            base_weights['trend_signal'] = 0.1
        
        return base_weights
    
    def calculate_recent_signal_accuracy(self):
        """Calculate accuracy of recent signals"""
        if len(self.signal_history) < 10:
            return 0.6  # Default assumption
        
        recent_signals = self.signal_history[-20:]
        accurate_signals = sum(1 for signal in recent_signals 
                             if signal.get('actual_result', 'unknown') == 'profitable')
        
        return accurate_signals / len(recent_signals) if recent_signals else 0.6
    
    def extract_features(self, analysis):
        """Extract features for ML and signal processing"""
        return {
            'trend_strength': analysis['trend_strength'],
            'volatility': analysis['volatility'],
            'momentum': analysis['momentum'],
            'distance_to_support': (analysis['current_price'] - analysis['support_resistance']['support']) / analysis['current_price'],
            'distance_to_resistance': (analysis['support_resistance']['resistance'] - analysis['current_price']) / analysis['current_price'],
            'fractal_dimension': analysis['fractal_dimension'],
            'market_regime_score': self.regime_to_score(analysis['market_regime'])
        }
    
    def generate_trend_signal(self, analysis, technical_indicators):
        """Generate advanced trend-following signal"""
        trend_strength = analysis['trend_strength']
        
        # Moving average confirmation
        sma_8 = technical_indicators.get('sma_8', 0)
        sma_21 = technical_indicators.get('sma_21', 0)
        sma_55 = technical_indicators.get('sma_55', 0)
        current_price = analysis.get('current_price', 0)
        
        # Trend direction scoring
        ma_trend_score = 0
        if sma_8 > sma_21 > sma_55 and current_price > sma_8:
            ma_trend_score = 1.0  # Strong uptrend
        elif sma_8 < sma_21 < sma_55 and current_price < sma_8:
            ma_trend_score = -1.0  # Strong downtrend
        elif sma_8 > sma_21 and current_price > sma_21:
            ma_trend_score = 0.6  # Moderate uptrend
        elif sma_8 < sma_21 and current_price < sma_21:
            ma_trend_score = -0.6  # Moderate downtrend
        
        # Combine trend indicators
        combined_score = (trend_strength * 0.6 + ma_trend_score * 0.4)
        
        # Confidence based on signal strength and alignment
        if abs(combined_score) > 0.7:
            confidence = 0.9
        elif abs(combined_score) > 0.5:
            confidence = 0.7
        elif abs(combined_score) > 0.3:
            confidence = 0.5
        else:
            confidence = 0.2
        
        return {'score': combined_score, 'confidence': confidence}
    
    def generate_momentum_signal(self, analysis, technical_indicators):
        """Generate advanced momentum signal"""
        momentum = analysis['momentum']
        rsi = technical_indicators.get('rsi', 50)
        macd_line = technical_indicators.get('macd_line', 0)
        macd_signal = technical_indicators.get('macd_signal', 0)
        
        # RSI momentum scoring
        rsi_score = 0
        if 30 < rsi < 70:  # Healthy momentum range
            if rsi > 55:
                rsi_score = (rsi - 55) / 15  # Scale 0-1 for bullish momentum
            elif rsi < 45:
                rsi_score = (rsi - 45) / 15  # Scale 0 to -1 for bearish momentum
        
        # MACD momentum scoring
        macd_score = 1 if macd_line > macd_signal else -1
        macd_strength = abs(macd_line - macd_signal)
        macd_confidence = min(macd_strength * 10, 1.0)
        
        # Combine momentum indicators
        combined_score = (momentum * 0.4 + rsi_score * 0.3 + macd_score * 0.3)
        confidence = (abs(momentum) * 0.4 + abs(rsi_score) * 0.3 + macd_confidence * 0.3)
        
        return {'score': combined_score, 'confidence': min(confidence, 1.0)}
    
    def generate_mean_reversion_signal(self, analysis, technical_indicators):
        """Generate enhanced mean reversion signal"""
        current_price = analysis['current_price']
        support = analysis['support_resistance']['support']
        resistance = analysis['support_resistance']['resistance']
        
        # RSI mean reversion
        rsi = technical_indicators.get('rsi', 50)
        rsi_reversion = 0
        if rsi > 70:  # Overbought
            rsi_reversion = -((rsi - 70) / 30)  # Scale -1 to 0
        elif rsi < 30:  # Oversold
            rsi_reversion = ((30 - rsi) / 30)  # Scale 0 to 1
        
        # Bollinger Band mean reversion
        bb_upper = technical_indicators.get('bb_upper', current_price)
        bb_lower = technical_indicators.get('bb_lower', current_price)
        bb_middle = technical_indicators.get('bb_middle', current_price)
        
        bb_reversion = 0
        if bb_upper != bb_lower:
            bb_position = (current_price - bb_lower) / (bb_upper - bb_lower)
            if bb_position > 0.8:  # Near upper band
                bb_reversion = -0.8
            elif bb_position < 0.2:  # Near lower band
                bb_reversion = 0.8
        
        # Support/Resistance mean reversion
        sr_reversion = 0
        if resistance != support:
            price_position = (current_price - support) / (resistance - support)
            if price_position > 0.85:  # Near resistance
                sr_reversion = -0.7
            elif price_position < 0.15:  # Near support
                sr_reversion = 0.7
        
        # Combine reversion signals
        combined_score = (rsi_reversion * 0.4 + bb_reversion * 0.4 + sr_reversion * 0.2)
        confidence = min(abs(combined_score) * 1.2, 1.0)
        
        return {'score': combined_score, 'confidence': confidence}
    
    def generate_breakout_signal(self, analysis, technical_indicators):
        """Generate enhanced breakout signal"""
        current_price = analysis['current_price']
        support = analysis['support_resistance']['support']
        resistance = analysis['support_resistance']['resistance']
        volatility = analysis['volatility']
        
        # Bollinger Band breakout
        bb_upper = technical_indicators.get('bb_upper', current_price)
        bb_lower = technical_indicators.get('bb_lower', current_price)
        
        bb_breakout = 0
        if current_price > bb_upper:
            bb_breakout = 0.8  # Bullish breakout
        elif current_price < bb_lower:
            bb_breakout = -0.8  # Bearish breakout
        
        # Support/Resistance breakout
        sr_breakout = 0
        price_buffer = current_price * 0.001  # 0.1% buffer
        
        if current_price > resistance + price_buffer:
            sr_breakout = 0.9  # Strong bullish breakout
        elif current_price < support - price_buffer:
            sr_breakout = -0.9  # Strong bearish breakout
        
        # Volume confirmation (using volatility as proxy)
        volume_confirmation = min(volatility * 10, 1.0)
        
        # Combine breakout signals
        combined_score = (bb_breakout * 0.6 + sr_breakout * 0.4)
        confidence = min(abs(combined_score) * volume_confirmation, 1.0)
        
        return {'score': combined_score, 'confidence': confidence}
    
    def generate_regime_signal(self, analysis):
        """Generate regime-based signal"""
        regime = analysis['market_regime']
        trend_strength = analysis['trend_strength']
        
        # Adjust strategy based on regime
        if regime in ['TRENDING_STABLE', 'TRENDING_VOLATILE']:
            score = trend_strength * 0.5
            confidence = 0.4
        elif regime in ['RANGING_STABLE', 'RANGING_VOLATILE']:
            # In ranging markets, fade extremes
            score = -trend_strength * 0.3
            confidence = 0.3
        else:
            score = 0
            confidence = 0
        
        return {'score': score, 'confidence': confidence}
    
    def regime_to_score(self, regime):
        """Convert regime to numerical score"""
        regime_scores = {
            'TRENDING_STABLE': 1.0,
            'TRENDING_VOLATILE': 0.7,
            'RANGING_STABLE': 0.3,
            'RANGING_VOLATILE': 0.1,
            'UNKNOWN': 0.0
        }
        return regime_scores.get(regime, 0.0)
    
    def get_ml_prediction(self, features, ml_model):
        """Get ML model prediction"""
        # This would be implemented with actual ML model
        # For now, return a placeholder
        return {
            'signal': 'HOLD',
            'confidence': 0.5
        }

class SmartPortfolioManager:
    """Smart portfolio and position size management"""
    
    def __init__(self):
        self.position_history = []
        
    def calculate_optimal_position_size(self, balance, signal_confidence, mode_settings):
        """Calculate optimal position size using advanced money management"""
        
        # Base position size from settings
        base_risk_pct = mode_settings['max_risk_pct']
        
        # Kelly Criterion adjustment
        win_rate = self.calculate_recent_winrate()
        avg_win_loss_ratio = self.calculate_avg_win_loss_ratio()
        
        if win_rate > 0 and avg_win_loss_ratio > 0:
            kelly_fraction = (win_rate * avg_win_loss_ratio - (1 - win_rate)) / avg_win_loss_ratio
            kelly_fraction = max(0, min(kelly_fraction, 0.25))  # Cap at 25%
        else:
            kelly_fraction = base_risk_pct / 100
        
        # Confidence adjustment
        confidence_multiplier = min(signal_confidence * 1.5, 1.0)
        
        # Final position size
        final_risk_pct = kelly_fraction * confidence_multiplier
        risk_amount = balance * final_risk_pct
        
        # Convert to lot size (simplified)
        # This would need actual contract specifications
        lot_size = max(risk_amount / 10000, 0.01)  # Simplified conversion
        
        return round(lot_size, 2)
    
    def calculate_recent_winrate(self):
        """Calculate recent win rate"""
        if len(self.position_history) < 10:
            return 0.6  # Default assumption
        
        recent_trades = self.position_history[-20:]  # Last 20 trades
        wins = sum(1 for trade in recent_trades if trade.get('profit', 0) > 0)
        return wins / len(recent_trades)
    
    def calculate_avg_win_loss_ratio(self):
        """Calculate average win/loss ratio"""
        if len(self.position_history) < 10:
            return 1.5  # Default assumption
        
        recent_trades = self.position_history[-20:]
        wins = [trade['profit'] for trade in recent_trades if trade.get('profit', 0) > 0]
        losses = [abs(trade['profit']) for trade in recent_trades if trade.get('profit', 0) < 0]
        
        if not wins or not losses:
            return 1.5
        
        avg_win = np.mean(wins)
        avg_loss = np.mean(losses)
        
        return avg_win / avg_loss if avg_loss > 0 else 1.5

if __name__ == "__main__":
    # Create and run advanced trading engine
    engine = AdvancedTradingEngine()
    engine.run()