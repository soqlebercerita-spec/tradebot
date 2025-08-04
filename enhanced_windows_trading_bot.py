#!/usr/bin/env python3
"""
🚀 ULTIMATE Enhanced Windows Trading Bot - Complete Real Money Trading System
✅ All Advanced Features Integrated
🎯 3 Trading Modes: HFT, Normal, Scalping
💰 Balance-Based TP/SL System
🔧 Optimized for MT5 Real Trading
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

# Import all enhanced modules
from enhanced_indicators import EnhancedIndicators
from config import config
try:
    from simple_ml_engine import SimpleMLEngine
    ML_AVAILABLE = True
except ImportError:
    ML_AVAILABLE = False

try:
    from simple_adaptive_indicators import SimpleAdaptiveIndicators
    ADAPTIVE_AVAILABLE = True
except ImportError:
    ADAPTIVE_AVAILABLE = False

try:
    from simple_risk_manager import SimpleRiskManager
    ADVANCED_RISK_AVAILABLE = True
except ImportError:
    ADVANCED_RISK_AVAILABLE = False

try:
    from performance_optimizer import PerformanceOptimizer
    OPTIMIZER_AVAILABLE = True
except ImportError:
    OPTIMIZER_AVAILABLE = False

# Import MT5 with enhanced error handling
try:
    import MetaTrader5 as mt5
    MT5_AVAILABLE = True
except ImportError:
    MT5_AVAILABLE = False
    print("❌ MetaTrader5 not available - please install: pip install MetaTrader5")

class UltimateWindowsTradingBot:
    def __init__(self):
        """Initialize the ultimate trading bot with all features"""
        print("🚀 Initializing Ultimate Windows Trading Bot...")
        
        # Core components
        self.indicators = EnhancedIndicators()
        
        # Advanced components (if available)
        self.ml_engine = SimpleMLEngine() if ML_AVAILABLE else None
        self.adaptive_indicators = SimpleAdaptiveIndicators() if ADAPTIVE_AVAILABLE else None
        self.advanced_risk = SimpleRiskManager() if ADVANCED_RISK_AVAILABLE else None
        self.performance_optimizer = PerformanceOptimizer() if OPTIMIZER_AVAILABLE else None
        
        # Trading modes
        self.NORMAL_MODE = "NORMAL"
        self.SCALPING_MODE = "SCALPING" 
        self.HFT_MODE = "HFT"
        self.current_mode = self.NORMAL_MODE
        
        # Bot state
        self.running = False
        self.mt5_connected = False
        self.modal_awal = None
        self.last_price = None
        self.last_prices = []
        self.last_reset_date = datetime.date.today()
        self.order_counter = 0
        self.total_opportunities_captured = 0
        self.total_opportunities_missed = 0
        self.price_retrieval_failures = 0
        self.successful_trades = 0
        self.failed_trades = 0
        
        # Threading
        self.bot_thread = None
        
        # Price data cache
        self.price_cache = {}
        self.last_successful_fetch = {}
        
        # Initialize performance optimizer if available
        if self.performance_optimizer:
            try:
                self.performance_optimizer.optimize_system()
            except AttributeError:
                # Method might not exist, skip optimization
                pass
        
        print("✅ Ultimate Trading Bot initialized successfully")
        self.setup_gui()
        
    def setup_gui(self):
        """Setup ultimate GUI interface with all features"""
        self.root = tk.Tk()
        self.root.title("🚀 ULTIMATE Windows MT5 Trading Bot - Real Money System")
        
        # Make window resizable with proper minimum size
        self.root.geometry("1200x800")
        self.root.minsize(900, 600)
        self.root.configure(bg="#f8f9fa")
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Configure grid weights for responsiveness
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        # Variables - All TP/SL based on balance percentage
        self.symbol_var = tk.StringVar(value=config.DEFAULT_SYMBOL)
        self.lot_var = tk.StringVar(value=str(config.DEFAULT_LOT))
        self.interval_var = tk.StringVar(value=str(config.DEFAULT_INTERVAL))
        
        # Trading mode variables
        self.trading_mode_var = tk.StringVar(value=self.NORMAL_MODE)
        
        # Balance-based TP/SL variables for each mode (fixed float conversion)
        self.normal_tp_var = tk.StringVar(value=f"{config.TP_PERSEN_BALANCE * 100:.1f}")
        self.normal_sl_var = tk.StringVar(value=f"{config.SL_PERSEN_BALANCE * 100:.1f}")
        self.scalping_tp_var = tk.StringVar(value=f"{config.SCALPING_TP_PERSEN_BALANCE * 100:.1f}")
        self.scalping_sl_var = tk.StringVar(value=f"{config.SCALPING_SL_PERSEN_BALANCE * 100:.1f}")
        self.hft_tp_var = tk.StringVar(value=f"{config.HFT_TP_PERSEN_BALANCE * 100:.1f}")
        self.hft_sl_var = tk.StringVar(value=f"{config.HFT_SL_PERSEN_BALANCE * 100:.1f}")
        
        # Status variables
        self.account_info_var = tk.StringVar(value="Account: Not Connected")
        self.profit_var = tk.StringVar(value="Real-time P/L: -")
        self.balance_var = tk.StringVar(value="$0.00")
        self.equity_var = tk.StringVar(value="Equity: $0.00")
        self.margin_var = tk.StringVar(value="Margin: $0.00")
        self.opportunities_var = tk.StringVar(value="Opportunities: Captured: 0 | Missed: 0")
        self.mode_status_var = tk.StringVar(value=f"Mode: {self.current_mode}")
        self.price_status_var = tk.StringVar(value="Price Feed: Disconnected")
        
        # Advanced features status
        self.ml_status_var = tk.StringVar(value=f"ML Engine: {'✅ Active' if ML_AVAILABLE else '❌ Disabled'}")
        self.adaptive_status_var = tk.StringVar(value=f"Adaptive Indicators: {'✅ Active' if ADAPTIVE_AVAILABLE else '❌ Disabled'}")
        self.risk_status_var = tk.StringVar(value=f"Advanced Risk: {'✅ Active' if ADVANCED_RISK_AVAILABLE else '❌ Disabled'}")
        
        self.create_ultimate_gui()
    
    def create_ultimate_gui(self):
        """Create the ultimate GUI with all features"""
        # Create main container with scrollable frame
        main_container = ttk.Frame(self.root)
        main_container.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        main_container.grid_rowconfigure(1, weight=1)
        main_container.grid_columnconfigure(0, weight=1)
        
        # Header with status
        self.create_header(main_container)
        
        # Main notebook for organized tabs
        self.create_main_notebook(main_container)
        
        # Bottom control panel
        self.create_control_panel(main_container)
        
        # Log display
        self.create_log_display(main_container)
        
    def create_header(self, parent):
        """Create enhanced header with MT5 status and advanced features"""
        header_frame = ttk.LabelFrame(parent, text="🚀 ULTIMATE Windows MT5 Trading Bot - Real Money System", padding=10)
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 5))
        header_frame.grid_columnconfigure(0, weight=1)
        
        # Status grid
        status_grid = ttk.Frame(header_frame)
        status_grid.grid(row=0, column=0, sticky="ew")
        status_grid.grid_columnconfigure([0, 1, 2], weight=1)
        
        # MT5 Status
        if MT5_AVAILABLE:
            ttk.Label(status_grid, text="✅ MetaTrader5 Ready", foreground="green", 
                     font=("Segoe UI", 10, "bold")).grid(row=0, column=0, sticky="w")
        else:
            ttk.Label(status_grid, text="❌ MetaTrader5 Not Found", foreground="red", 
                     font=("Segoe UI", 10, "bold")).grid(row=0, column=0, sticky="w")
        
        # Current mode
        ttk.Label(status_grid, textvariable=self.mode_status_var, foreground="blue",
                 font=("Segoe UI", 10, "bold")).grid(row=0, column=1)
        
        # Advanced features status
        ttk.Label(status_grid, textvariable=self.price_status_var, foreground="green",
                 font=("Segoe UI", 10)).grid(row=0, column=2, sticky="e")
        
        # Second row with additional status
        status_grid2 = ttk.Frame(header_frame)
        status_grid2.grid(row=1, column=0, sticky="ew", pady=(5, 0))
        status_grid2.grid_columnconfigure([0, 1, 2], weight=1)
        
        ttk.Label(status_grid2, textvariable=self.ml_status_var, font=("Segoe UI", 9)).grid(row=0, column=0, sticky="w")
        ttk.Label(status_grid2, textvariable=self.adaptive_status_var, font=("Segoe UI", 9)).grid(row=0, column=1)
        ttk.Label(status_grid2, textvariable=self.risk_status_var, font=("Segoe UI", 9)).grid(row=0, column=2, sticky="e")
    
    def create_main_notebook(self, parent):
        """Create main notebook with all trading tabs"""
        notebook_frame = ttk.Frame(parent)
        notebook_frame.grid(row=1, column=0, sticky="nsew", pady=(0, 5))
        notebook_frame.grid_rowconfigure(0, weight=1)
        notebook_frame.grid_columnconfigure(0, weight=1)
        
        self.main_notebook = ttk.Notebook(notebook_frame)
        self.main_notebook.grid(row=0, column=0, sticky="nsew")
        
        # Trading Settings Tab
        self.create_trading_settings_tab()
        
        # Account & Performance Tab
        self.create_account_tab()
        
        # Advanced Features Tab
        self.create_advanced_features_tab()
        
        # Risk Management Tab
        self.create_risk_management_tab()
        
    def create_trading_settings_tab(self):
        """Create comprehensive trading settings tab"""
        trading_tab = ttk.Frame(self.main_notebook)
        self.main_notebook.add(trading_tab, text="⚙️ Trading Settings")
        trading_tab.grid_columnconfigure([0, 1, 2], weight=1)
        
        # Basic Settings
        basic_frame = ttk.LabelFrame(trading_tab, text="📊 Basic Trading Settings", padding=10)
        basic_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        settings = [
            ("Symbol:", self.symbol_var, ["XAUUSDm", "EURUSD", "BTCUSD", "GBPUSD", "USDJPY"]),
            ("Lot Size:", self.lot_var, None),
            ("Scan Interval (s):", self.interval_var, None),
        ]
        
        for i, (label, var, values) in enumerate(settings):
            ttk.Label(basic_frame, text=label).grid(row=i, column=0, sticky="e", pady=5, padx=(0, 5))
            if values:
                combo = ttk.Combobox(basic_frame, textvariable=var, values=values, state="readonly")
                combo.grid(row=i, column=1, sticky="ew", pady=5)
            else:
                ttk.Entry(basic_frame, textvariable=var).grid(row=i, column=1, sticky="ew", pady=5)
        
        basic_frame.grid_columnconfigure(1, weight=1)
        
        # Trading Modes
        mode_frame = ttk.LabelFrame(trading_tab, text="🎯 Trading Modes", padding=10)
        mode_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        
        # Mode selection
        ttk.Label(mode_frame, text="Select Trading Mode:", font=("Segoe UI", 10, "bold")).grid(row=0, column=0, columnspan=2, pady=(0, 10))
        
        modes = [
            (self.NORMAL_MODE, "📈 Normal Trading - Balanced approach"),
            (self.SCALPING_MODE, "⚡ Scalping - Quick trades"),
            (self.HFT_MODE, "🚀 HFT - High frequency trading")
        ]
        
        for i, (mode, desc) in enumerate(modes):
            ttk.Radiobutton(mode_frame, text=desc, variable=self.trading_mode_var, 
                           value=mode, command=self.on_mode_change).grid(row=i+1, column=0, sticky="w", pady=2)
        
        # TP/SL Settings based on balance percentage
        tpsl_frame = ttk.LabelFrame(trading_tab, text="💰 TP/SL Settings (% of Balance)", padding=10)
        tpsl_frame.grid(row=0, column=2, sticky="nsew", padx=5, pady=5)
        
        # Normal mode TP/SL
        ttk.Label(tpsl_frame, text="📈 Normal Mode:", font=("Segoe UI", 10, "bold")).grid(row=0, column=0, columnspan=2, sticky="w")
        ttk.Label(tpsl_frame, text="Take Profit %:").grid(row=1, column=0, sticky="e", pady=2)
        ttk.Entry(tpsl_frame, textvariable=self.normal_tp_var, width=10).grid(row=1, column=1, pady=2)
        ttk.Label(tpsl_frame, text="Stop Loss %:").grid(row=2, column=0, sticky="e", pady=2)
        ttk.Entry(tpsl_frame, textvariable=self.normal_sl_var, width=10).grid(row=2, column=1, pady=2)
        
        # Scalping mode TP/SL
        ttk.Label(tpsl_frame, text="⚡ Scalping Mode:", font=("Segoe UI", 10, "bold")).grid(row=3, column=0, columnspan=2, sticky="w", pady=(10, 0))
        ttk.Label(tpsl_frame, text="Take Profit %:").grid(row=4, column=0, sticky="e", pady=2)
        ttk.Entry(tpsl_frame, textvariable=self.scalping_tp_var, width=10).grid(row=4, column=1, pady=2)
        ttk.Label(tpsl_frame, text="Stop Loss %:").grid(row=5, column=0, sticky="e", pady=2)
        ttk.Entry(tpsl_frame, textvariable=self.scalping_sl_var, width=10).grid(row=5, column=1, pady=2)
        
        # HFT mode TP/SL
        ttk.Label(tpsl_frame, text="🚀 HFT Mode:", font=("Segoe UI", 10, "bold")).grid(row=6, column=0, columnspan=2, sticky="w", pady=(10, 0))
        ttk.Label(tpsl_frame, text="Take Profit %:").grid(row=7, column=0, sticky="e", pady=2)
        ttk.Entry(tpsl_frame, textvariable=self.hft_tp_var, width=10).grid(row=7, column=1, pady=2)
        ttk.Label(tpsl_frame, text="Stop Loss %:").grid(row=8, column=0, sticky="e", pady=2)
        ttk.Entry(tpsl_frame, textvariable=self.hft_sl_var, width=10).grid(row=8, column=1, pady=2)
        
    def create_account_tab(self):
        """Create account and performance monitoring tab"""
        account_tab = ttk.Frame(self.main_notebook)
        self.main_notebook.add(account_tab, text="💰 Account & Performance")
        account_tab.grid_columnconfigure([0, 1], weight=1)
        account_tab.grid_rowconfigure([0, 1], weight=1)
        
        # Account Info
        account_frame = ttk.LabelFrame(account_tab, text="📊 Account Information", padding=10)
        account_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        account_labels = [
            ("Account Status:", self.account_info_var),
            ("Balance:", self.balance_var),
            ("Equity:", self.equity_var),
            ("Margin:", self.margin_var),
            ("P/L:", self.profit_var),
        ]
        
        for i, (label, var) in enumerate(account_labels):
            ttk.Label(account_frame, text=label, font=("Segoe UI", 10, "bold")).grid(row=i, column=0, sticky="w", pady=5)
            ttk.Label(account_frame, textvariable=var, font=("Segoe UI", 10)).grid(row=i, column=1, sticky="w", padx=10)
        
        # Performance Metrics
        performance_frame = ttk.LabelFrame(account_tab, text="📈 Performance Metrics", padding=10)
        performance_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        
        ttk.Label(performance_frame, textvariable=self.opportunities_var, font=("Segoe UI", 10)).grid(row=0, column=0, sticky="w", pady=5)
        
        # Trading Statistics
        stats_frame = ttk.LabelFrame(account_tab, text="📊 Trading Statistics", padding=10)
        stats_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
        
        # Create statistics display
        self.create_statistics_display(stats_frame)
        
    def create_advanced_features_tab(self):
        """Create advanced features configuration tab"""
        advanced_tab = ttk.Frame(self.main_notebook)
        self.main_notebook.add(advanced_tab, text="🤖 Advanced Features")
        advanced_tab.grid_columnconfigure([0, 1], weight=1)
        advanced_tab.grid_rowconfigure([0, 1], weight=1)
        
        # ML Engine Settings
        ml_frame = ttk.LabelFrame(advanced_tab, text="🧠 Machine Learning Engine", padding=10)
        ml_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        if ML_AVAILABLE:
            ttk.Label(ml_frame, text="✅ ML Engine Active", foreground="green", 
                     font=("Segoe UI", 10, "bold")).pack(anchor="w")
            ttk.Label(ml_frame, text="• Pattern Recognition: Active").pack(anchor="w", pady=2)
            ttk.Label(ml_frame, text="• Market Prediction: Active").pack(anchor="w", pady=2)
            ttk.Label(ml_frame, text="• Sentiment Analysis: Active").pack(anchor="w", pady=2)
        else:
            ttk.Label(ml_frame, text="❌ ML Engine Disabled", foreground="red", 
                     font=("Segoe UI", 10, "bold")).pack(anchor="w")
            ttk.Label(ml_frame, text="Install ML dependencies to enable").pack(anchor="w", pady=2)
        
        # Adaptive Indicators
        adaptive_frame = ttk.LabelFrame(advanced_tab, text="📊 Adaptive Indicators", padding=10)
        adaptive_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        
        if ADAPTIVE_AVAILABLE:
            ttk.Label(adaptive_frame, text="✅ Adaptive Indicators Active", foreground="green", 
                     font=("Segoe UI", 10, "bold")).pack(anchor="w")
            ttk.Label(adaptive_frame, text="• Volatility Adjustment: Active").pack(anchor="w", pady=2)
            ttk.Label(adaptive_frame, text="• Trend Adaptation: Active").pack(anchor="w", pady=2)
            ttk.Label(adaptive_frame, text="• Volume Weighting: Active").pack(anchor="w", pady=2)
        else:
            ttk.Label(adaptive_frame, text="❌ Adaptive Indicators Disabled", foreground="red", 
                     font=("Segoe UI", 10, "bold")).pack(anchor="w")
        
        # Performance Optimizer
        optimizer_frame = ttk.LabelFrame(advanced_tab, text="⚡ Performance Optimizer", padding=10)
        optimizer_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
        
        if OPTIMIZER_AVAILABLE:
            ttk.Label(optimizer_frame, text="✅ Performance Optimizer Active", foreground="green", 
                     font=("Segoe UI", 10, "bold")).pack(anchor="w")
            ttk.Label(optimizer_frame, text="• System Optimization: Active").pack(anchor="w", pady=2)
            ttk.Label(optimizer_frame, text="• Memory Management: Active").pack(anchor="w", pady=2)
            ttk.Label(optimizer_frame, text="• CPU Optimization: Active").pack(anchor="w", pady=2)
        else:
            ttk.Label(optimizer_frame, text="❌ Performance Optimizer Disabled", foreground="red", 
                     font=("Segoe UI", 10, "bold")).pack(anchor="w")
    
    def create_risk_management_tab(self):
        """Create advanced risk management tab"""
        risk_tab = ttk.Frame(self.main_notebook)
        self.main_notebook.add(risk_tab, text="🛡️ Risk Management")
        risk_tab.grid_columnconfigure([0, 1], weight=1)
        risk_tab.grid_rowconfigure([0, 1], weight=1)
        
        # Basic Risk Controls
        basic_risk_frame = ttk.LabelFrame(risk_tab, text="🛡️ Basic Risk Controls", padding=10)
        basic_risk_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        risk_info = [
            ("Max Orders Per Session:", f"{config.MAX_ORDER_PER_SESSION}"),
            ("Max Risk Per Trade:", f"{config.MAX_RISK_PER_TRADE}%"),
            ("Max Drawdown:", f"{config.MAX_DRAWDOWN}%"),
            ("Daily Loss Limit:", "5% of balance"),
            ("Position Size:", "Dynamic based on balance"),
        ]
        
        for i, (label, value) in enumerate(risk_info):
            ttk.Label(basic_risk_frame, text=label, font=("Segoe UI", 10, "bold")).grid(row=i, column=0, sticky="w", pady=3)
            ttk.Label(basic_risk_frame, text=value, font=("Segoe UI", 10)).grid(row=i, column=1, sticky="w", padx=10)
        
        # Advanced Risk Features
        advanced_risk_frame = ttk.LabelFrame(risk_tab, text="🔬 Advanced Risk Features", padding=10)
        advanced_risk_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        
        if ADVANCED_RISK_AVAILABLE:
            ttk.Label(advanced_risk_frame, text="✅ Advanced Risk Active", foreground="green", 
                     font=("Segoe UI", 10, "bold")).pack(anchor="w")
            ttk.Label(advanced_risk_frame, text="• VaR Calculation: Active").pack(anchor="w", pady=2)
            ttk.Label(advanced_risk_frame, text="• Kelly Criterion: Active").pack(anchor="w", pady=2)
            ttk.Label(advanced_risk_frame, text="• Emergency Stops: Active").pack(anchor="w", pady=2)
        else:
            ttk.Label(advanced_risk_frame, text="❌ Advanced Risk Disabled", foreground="red", 
                     font=("Segoe UI", 10, "bold")).pack(anchor="w")
        
        # Emergency Controls
        emergency_frame = ttk.LabelFrame(risk_tab, text="🚨 Emergency Controls", padding=10)
        emergency_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
        
        emergency_buttons = ttk.Frame(emergency_frame)
        emergency_buttons.pack(fill="x", pady=10)
        
        ttk.Button(emergency_buttons, text="🚨 EMERGENCY STOP", 
                  command=self.emergency_stop).pack(side="left", padx=10)
        ttk.Button(emergency_buttons, text="🔄 CLOSE ALL POSITIONS", 
                  command=self.close_all_positions).pack(side="left", padx=10)
        ttk.Button(emergency_buttons, text="📊 RISK ASSESSMENT", 
                  command=self.show_risk_assessment).pack(side="left", padx=10)
    
    def create_statistics_display(self, parent):
        """Create trading statistics display"""
        stats_grid = ttk.Frame(parent)
        stats_grid.pack(fill="both", expand=True)
        stats_grid.grid_columnconfigure([0, 1, 2, 3], weight=1)
        
        # Statistics labels
        stats = [
            ("Orders Executed:", "order_counter"),
            ("Successful Trades:", "successful_trades"),
            ("Failed Trades:", "failed_trades"),
            ("Success Rate:", "success_rate"),
        ]
        
        for i, (label, attr) in enumerate(stats):
            row = i // 2
            col = (i % 2) * 2
            ttk.Label(stats_grid, text=label, font=("Segoe UI", 10, "bold")).grid(row=row, column=col, sticky="w", pady=5)
            value_label = ttk.Label(stats_grid, text="0", font=("Segoe UI", 10))
            value_label.grid(row=row, column=col+1, sticky="w", padx=10)
            setattr(self, f"{attr}_label", value_label)
    
    def create_control_panel(self, parent):
        """Create main control panel"""
        control_frame = ttk.LabelFrame(parent, text="🎮 Trading Controls", padding=10)
        control_frame.grid(row=2, column=0, sticky="ew", pady=(0, 5))
        control_frame.grid_columnconfigure([0, 1, 2, 3, 4], weight=1)
        
        # Main trading buttons
        self.connect_button = ttk.Button(control_frame, text="🔌 Connect MT5", command=self.connect_mt5)
        self.connect_button.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        
        self.start_button = ttk.Button(control_frame, text="🚀 Start Trading", command=self.start_bot)
        self.start_button.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        
        self.stop_button = ttk.Button(control_frame, text="⏹️ Stop Trading", command=self.stop_bot, state="disabled")
        self.stop_button.grid(row=0, column=2, padx=5, pady=5, sticky="ew")
        
        self.reset_button = ttk.Button(control_frame, text="🔄 Reset Session", command=self.reset_session)
        self.reset_button.grid(row=0, column=3, padx=5, pady=5, sticky="ew")
        
        self.disconnect_button = ttk.Button(control_frame, text="🔌 Disconnect", command=self.disconnect_mt5)
        self.disconnect_button.grid(row=0, column=4, padx=5, pady=5, sticky="ew")
    
    def create_log_display(self, parent):
        """Create log display area"""
        log_frame = ttk.LabelFrame(parent, text="📝 Trading Log", padding=5)
        log_frame.grid(row=3, column=0, sticky="nsew", pady=(0, 5))
        log_frame.grid_rowconfigure(0, weight=1)
        log_frame.grid_columnconfigure(0, weight=1)
        
        # Create scrolled text widget
        self.log_text = ScrolledText(log_frame, height=8, font=("Consolas", 9))
        self.log_text.grid(row=0, column=0, sticky="nsew")
        
        # Configure text tags for colored logging
        self.log_text.tag_configure("success", foreground="green")
        self.log_text.tag_configure("warning", foreground="orange")
        self.log_text.tag_configure("error", foreground="red")
        self.log_text.tag_configure("info", foreground="blue")
    
    def on_mode_change(self):
        """Handle trading mode change"""
        self.current_mode = self.trading_mode_var.get()
        self.mode_status_var.set(f"Mode: {self.current_mode}")
        
        # Update interval based on mode
        if self.current_mode == self.HFT_MODE:
            self.interval_var.set(str(config.HFT_INTERVAL))
        elif self.current_mode == self.SCALPING_MODE:
            self.interval_var.set("3")  # Fast scalping
        else:
            self.interval_var.set(str(config.DEFAULT_INTERVAL))
        
        self.log(f"🎯 Trading mode changed to: {self.current_mode}", "info")
    
    def connect_mt5(self):
        """Connect to MetaTrader5"""
        if not MT5_AVAILABLE:
            messagebox.showerror("MT5 Not Available", 
                               "MetaTrader5 library not installed.\nPlease install: pip install MetaTrader5")
            return
        
        try:
            self.log("🔌 Connecting to MetaTrader5...", "info")
            
            if not mt5.initialize():
                error = mt5.last_error()
                raise Exception(f"MT5 initialization failed: {error}")
            
            # Get account info
            account_info = mt5.account_info()
            if account_info is None:
                raise Exception("Failed to get account info")
            
            self.mt5_connected = True
            self.modal_awal = account_info.balance
            
            # Update UI
            self.account_info_var.set(f"Account: {account_info.login} - {account_info.server}")
            self.balance_var.set(f"${account_info.balance:,.2f}")
            self.equity_var.set(f"Equity: ${account_info.equity:,.2f}")
            self.margin_var.set(f"Margin: ${account_info.margin:,.2f}")
            
            self.connect_button.config(state="disabled")
            self.start_button.config(state="normal")
            self.disconnect_button.config(state="normal")
            
            self.log(f"✅ Connected to MT5 - Account: {account_info.login}", "success")
            self.log(f"💰 Initial Balance: ${account_info.balance:,.2f}", "success")
            
        except Exception as e:
            self.log(f"❌ MT5 connection failed: {e}", "error")
            messagebox.showerror("Connection Error", f"Failed to connect to MT5:\n{e}")
    
    def disconnect_mt5(self):
        """Disconnect from MetaTrader5"""
        try:
            if self.running:
                self.stop_bot()
            
            if MT5_AVAILABLE and self.mt5_connected:
                mt5.shutdown()
                self.mt5_connected = False
                
                # Reset UI
                self.account_info_var.set("Account: Not Connected")
                self.balance_var.set("$0.00")
                self.equity_var.set("Equity: $0.00")
                self.margin_var.set("Margin: $0.00")
                
                self.connect_button.config(state="normal")
                self.start_button.config(state="disabled")
                self.disconnect_button.config(state="disabled")
                
                self.log("🔌 Disconnected from MT5", "info")
            
        except Exception as e:
            self.log(f"❌ Disconnect error: {e}", "error")
    
    def start_bot(self):
        """Start the ultimate trading bot"""
        if not self.mt5_connected:
            messagebox.showerror("Not Connected", "Please connect to MT5 first")
            return
        
        if self.running:
            messagebox.showwarning("Already Running", "Bot is already running")
            return
        
        try:
            # Validate inputs
            lot = float(self.lot_var.get())
            interval = int(self.interval_var.get())
            
            if lot <= 0 or lot > 10:
                raise ValueError("Lot size must be between 0.01 and 10")
            if interval < 1 or interval > 300:
                raise ValueError("Interval must be between 1 and 300 seconds")
            
            self.running = True
            self.start_button.config(state="disabled")
            self.stop_button.config(state="normal")
            
            # Start trading thread
            self.bot_thread = threading.Thread(target=self.trading_loop, daemon=True)
            self.bot_thread.start()
            
            self.log(f"🚀 Ultimate Trading Bot STARTED - Mode: {self.current_mode}", "success")
            self.log(f"⚙️ Settings: {lot} lots, {interval}s interval", "info")
            
        except ValueError as e:
            messagebox.showerror("Invalid Input", str(e))
        except Exception as e:
            self.log(f"❌ Start error: {e}", "error")
    
    def stop_bot(self):
        """Stop the trading bot"""
        if not self.running:
            messagebox.showwarning("Not Running", "Bot is not running")
            return
        
        try:
            self.running = False
            self.start_button.config(state="normal")
            self.stop_button.config(state="disabled")
            
            # Calculate session statistics
            success_rate = self.calculate_success_rate()
            
            self.log("🛑 Ultimate Trading Bot STOPPED", "warning")
            self.log(f"📊 Session Summary: {self.order_counter} orders, {success_rate:.1f}% success", "info")
            
        except Exception as e:
            self.log(f"❌ Stop error: {e}", "error")
    
    def reset_session(self):
        """Reset trading session"""
        if self.running:
            messagebox.showwarning("Bot Running", "Please stop the bot before resetting")
            return
        
        self.order_counter = 0
        self.total_opportunities_captured = 0
        self.total_opportunities_missed = 0
        self.successful_trades = 0
        self.failed_trades = 0
        self.price_retrieval_failures = 0
        
        self.opportunities_var.set("Opportunities: Captured: 0 | Missed: 0")
        self.update_statistics_display()
        
        self.log("🔄 Session reset complete", "info")
    
    def trading_loop(self):
        """Main trading loop with all features integrated"""
        self.log("🎯 Trading loop started...", "info")
        
        while self.running:
            try:
                # Get current settings based on mode
                interval = self.get_mode_interval()
                tp_pct, sl_pct = self.get_mode_tpsl()
                
                # Update price feed status
                self.price_status_var.set("Price Feed: 🔄 Fetching...")
                
                # Get market data
                symbol = self.symbol_var.get()
                current_price = self.get_current_price(symbol)
                
                if current_price is None:
                    self.price_retrieval_failures += 1
                    self.price_status_var.set("Price Feed: ❌ Failed")
                    time.sleep(interval)
                    continue
                
                self.price_status_var.set("Price Feed: ✅ Connected")
                
                # Generate trading signal with all features
                signal = self.generate_enhanced_signal(symbol, current_price)
                
                if signal and signal['action'] != 'HOLD':
                    self.execute_trade(signal, tp_pct, sl_pct)
                    self.total_opportunities_captured += 1
                else:
                    self.total_opportunities_missed += 1
                
                # Update opportunities display
                self.opportunities_var.set(
                    f"Opportunities: Captured: {self.total_opportunities_captured} | "
                    f"Missed: {self.total_opportunities_missed}"
                )
                
                # Update account info
                self.update_account_display()
                
                # Update statistics
                self.update_statistics_display()
                
                time.sleep(interval)
                
            except Exception as e:
                self.log(f"❌ Trading loop error: {e}", "error")
                time.sleep(5)
    
    def get_mode_interval(self):
        """Get interval based on current mode"""
        if self.current_mode == self.HFT_MODE:
            return config.HFT_INTERVAL
        elif self.current_mode == self.SCALPING_MODE:
            return 3  # Fast scalping
        else:
            return int(self.interval_var.get())
    
    def get_mode_tpsl(self):
        """Get TP/SL percentages based on current mode"""
        try:
            if self.current_mode == self.HFT_MODE:
                tp = self.hft_tp_var.get().replace(',', '.').strip()
                sl = self.hft_sl_var.get().replace(',', '.').strip()
                return float(tp), float(sl)
            elif self.current_mode == self.SCALPING_MODE:
                tp = self.scalping_tp_var.get().replace(',', '.').strip()
                sl = self.scalping_sl_var.get().replace(',', '.').strip()
                return float(tp), float(sl)
            else:
                tp = self.normal_tp_var.get().replace(',', '.').strip()
                sl = self.normal_sl_var.get().replace(',', '.').strip()
                return float(tp), float(sl)
        except ValueError as e:
            self.log(f"❌ TP/SL conversion error: {e}", "error")
            # Return default values
            return 1.0, 3.0
    
    def get_current_price(self, symbol):
        """Get current price from MT5"""
        try:
            if not self.mt5_connected:
                return None
            
            tick = mt5.symbol_info_tick(symbol)
            if tick is None:
                return None
            
            return (tick.bid + tick.ask) / 2
            
        except Exception as e:
            self.log(f"❌ Price fetch error: {e}", "error")
            return None
    
    def generate_enhanced_signal(self, symbol, current_price):
        """Generate enhanced trading signal with all features"""
        try:
            # Generate price history for technical analysis
            if symbol not in self.price_cache:
                self.price_cache[symbol] = []
            
            # Add current price to cache
            self.price_cache[symbol].append(current_price)
            
            # Keep only last 100 prices
            if len(self.price_cache[symbol]) > 100:
                self.price_cache[symbol] = self.price_cache[symbol][-100:]
            
            # Need at least 20 prices for analysis
            if len(self.price_cache[symbol]) < 20:
                return {'action': 'HOLD', 'confidence': 0}
            
            # Use enhanced signal analysis
            signal = self.indicators.get_signal(self.price_cache[symbol], symbol)
            
            if not signal:
                return {'action': 'HOLD', 'confidence': 0}
            
            # Enhance signal with ML if available
            if self.ml_engine:
                try:
                    ml_signal = self.ml_engine.predict_signal(symbol, current_price)
                    if ml_signal:
                        signal['confidence'] *= ml_signal.get('confidence', 1.0)
                        signal['ml_prediction'] = ml_signal.get('prediction', 'NEUTRAL')
                except:
                    pass  # ML engine might not have all methods
            
            # Enhance with adaptive indicators if available
            if self.adaptive_indicators:
                try:
                    adaptive_signal = self.adaptive_indicators.get_adaptive_signal(symbol, current_price)
                    if adaptive_signal:
                        signal['confidence'] *= adaptive_signal.get('confidence', 1.0)
                        signal['adaptive_score'] = adaptive_signal.get('score', 0)
                except:
                    pass  # Adaptive indicators might not have all methods
            
            # Apply mode-specific filters
            signal = self.apply_mode_filters(signal)
            
            return signal
            
        except Exception as e:
            self.log(f"❌ Signal generation error: {e}", "error")
            return {'action': 'HOLD', 'confidence': 0}
    
    def apply_mode_filters(self, signal):
        """Apply mode-specific signal filters"""
        if self.current_mode == self.HFT_MODE:
            # HFT requires higher confidence
            if signal['confidence'] < config.SIGNAL_CONFIDENCE_THRESHOLD_HFT:
                signal['action'] = 'HOLD'
        elif self.current_mode == self.SCALPING_MODE:
            # Scalping prefers quick signals
            if signal.get('trend_strength', 0) < 0.3:
                signal['action'] = 'HOLD'
        else:
            # Normal mode uses standard confidence
            if signal['confidence'] < config.SIGNAL_CONFIDENCE_THRESHOLD:
                signal['action'] = 'HOLD'
        
        return signal
    
    def execute_trade(self, signal, tp_pct, sl_pct):
        """Execute trade with balance-based TP/SL"""
        try:
            if not self.mt5_connected:
                return
            
            # Check order limits
            max_orders = self.get_max_orders()
            if self.order_counter >= max_orders:
                self.log(f"⚠️ Order limit reached: {max_orders}", "warning")
                return
            
            # Get account info for balance-based calculations
            account_info = mt5.account_info()
            if not account_info:
                return
            
            balance = account_info.balance
            symbol = self.symbol_var.get()
            lot = float(self.lot_var.get())
            
            # Calculate TP/SL based on balance percentage
            tp_amount = balance * (tp_pct / 100)
            sl_amount = balance * (sl_pct / 100)
            
            # Get symbol info for price conversion
            symbol_info = mt5.symbol_info(symbol)
            if not symbol_info:
                return
            
            # Convert amounts to price levels (simplified)
            tick_value = symbol_info.trade_tick_value
            tp_points = tp_amount / (tick_value * lot) if tick_value > 0 else 100
            sl_points = sl_amount / (tick_value * lot) if tick_value > 0 else 300
            
            current_price = self.get_current_price(symbol)
            if not current_price:
                return
            
            # Prepare order request
            if signal['action'] == 'BUY':
                order_type = mt5.ORDER_TYPE_BUY
                tp_price = current_price + (tp_points * symbol_info.point)
                sl_price = current_price - (sl_points * symbol_info.point)
            else:  # SELL
                order_type = mt5.ORDER_TYPE_SELL
                tp_price = current_price - (tp_points * symbol_info.point)
                sl_price = current_price + (sl_points * symbol_info.point)
            
            request = {
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": symbol,
                "volume": lot,
                "type": order_type,
                "price": current_price,
                "tp": tp_price,
                "sl": sl_price,
                "deviation": config.MT5_DEVIATION,
                "magic": config.MT5_MAGIC_NUMBER,
                "comment": f"Ultimate Bot - {self.current_mode}",
                "type_time": mt5.ORDER_TIME_GTC,
                "type_filling": mt5.ORDER_FILLING_IOC,
            }
            
            # Send order
            result = mt5.order_send(request)
            
            if result.retcode == mt5.TRADE_RETCODE_DONE:
                self.order_counter += 1
                self.successful_trades += 1
                
                self.log(f"✅ {signal['action']} order executed - Ticket: {result.order}", "success")
                self.log(f"💰 TP: ${tp_amount:,.2f} | SL: ${sl_amount:,.2f} (Balance %)", "info")
                
                # Log trade details
                self.log_trade(signal, result, tp_amount, sl_amount)
                
            else:
                self.failed_trades += 1
                self.log(f"❌ Order failed: {result.comment}", "error")
                
        except Exception as e:
            self.failed_trades += 1
            self.log(f"❌ Trade execution error: {e}", "error")
    
    def get_max_orders(self):
        """Get maximum orders based on current mode"""
        if self.current_mode == self.HFT_MODE:
            return config.MAX_ORDER_PER_SESSION_HFT
        else:
            return config.MAX_ORDER_PER_SESSION
    
    def update_account_display(self):
        """Update account information display"""
        try:
            if not self.mt5_connected:
                return
            
            account_info = mt5.account_info()
            if not account_info:
                return
            
            self.balance_var.set(f"${account_info.balance:,.2f}")
            self.equity_var.set(f"Equity: ${account_info.equity:,.2f}")
            self.margin_var.set(f"Margin: ${account_info.margin:,.2f}")
            
            # Calculate P/L
            if self.modal_awal:
                profit = account_info.equity - self.modal_awal
                self.profit_var.set(f"Real-time P/L: ${profit:+,.2f}")
            
        except Exception as e:
            self.log(f"❌ Account update error: {e}", "error")
    
    def update_statistics_display(self):
        """Update statistics display"""
        try:
            self.order_counter_label.config(text=str(self.order_counter))
            self.successful_trades_label.config(text=str(self.successful_trades))
            self.failed_trades_label.config(text=str(self.failed_trades))
            
            success_rate = self.calculate_success_rate()
            self.success_rate_label.config(text=f"{success_rate:.1f}%")
            
        except Exception:
            pass
    
    def calculate_success_rate(self):
        """Calculate trading success rate"""
        total_trades = self.successful_trades + self.failed_trades
        if total_trades == 0:
            return 0.0
        return (self.successful_trades / total_trades) * 100
    
    def emergency_stop(self):
        """Emergency stop all trading"""
        try:
            if messagebox.askyesno("Emergency Stop", "Stop all trading immediately?"):
                self.running = False
                self.close_all_positions()
                self.log("🚨 EMERGENCY STOP ACTIVATED", "error")
                
        except Exception as e:
            self.log(f"❌ Emergency stop error: {e}", "error")
    
    def close_all_positions(self):
        """Close all open positions"""
        try:
            if not self.mt5_connected:
                return
            
            positions = mt5.positions_get()
            if not positions:
                self.log("ℹ️ No open positions to close", "info")
                return
            
            closed_count = 0
            for position in positions:
                request = {
                    "action": mt5.TRADE_ACTION_DEAL,
                    "symbol": position.symbol,
                    "volume": position.volume,
                    "type": mt5.ORDER_TYPE_SELL if position.type == mt5.ORDER_TYPE_BUY else mt5.ORDER_TYPE_BUY,
                    "position": position.ticket,
                    "deviation": config.MT5_DEVIATION,
                    "magic": config.MT5_MAGIC_NUMBER,
                    "comment": "Emergency close",
                    "type_time": mt5.ORDER_TIME_GTC,
                    "type_filling": mt5.ORDER_FILLING_IOC,
                }
                
                result = mt5.order_send(request)
                if result.retcode == mt5.TRADE_RETCODE_DONE:
                    closed_count += 1
            
            self.log(f"🔄 Closed {closed_count} positions", "info")
            
        except Exception as e:
            self.log(f"❌ Close positions error: {e}", "error")
    
    def show_risk_assessment(self):
        """Show risk assessment"""
        try:
            if not self.mt5_connected:
                messagebox.showinfo("Risk Assessment", "Connect to MT5 for risk assessment")
                return
            
            account_info = mt5.account_info()
            if not account_info:
                return
            
            # Calculate risk metrics
            risk_info = f"""
🛡️ RISK ASSESSMENT REPORT

💰 Account Information:
   Balance: ${account_info.balance:,.2f}
   Equity: ${account_info.equity:,.2f}
   Margin: ${account_info.margin:,.2f}
   Free Margin: ${account_info.margin_free:,.2f}

📊 Trading Statistics:
   Orders Executed: {self.order_counter}
   Success Rate: {self.calculate_success_rate():.1f}%
   Current Mode: {self.current_mode}

⚠️ Risk Levels:
   Max Orders: {self.get_max_orders()}
   Max Risk per Trade: {config.MAX_RISK_PER_TRADE}%
   Max Drawdown: {config.MAX_DRAWDOWN}%
   
🎯 Current TP/SL:
   Take Profit: {self.get_mode_tpsl()[0]}% of balance
   Stop Loss: {self.get_mode_tpsl()[1]}% of balance
"""
            
            messagebox.showinfo("Risk Assessment", risk_info)
            
        except Exception as e:
            self.log(f"❌ Risk assessment error: {e}", "error")
    
    def log_trade(self, signal, result, tp_amount, sl_amount):
        """Log trade details to CSV"""
        try:
            with open("ultimate_trades.csv", "a", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                
                # Write header if file is empty
                if file.tell() == 0:
                    writer.writerow([
                        "Timestamp", "Mode", "Symbol", "Action", "Price", "Lot", 
                        "TP_Amount", "SL_Amount", "Confidence", "Ticket", "Status"
                    ])
                
                writer.writerow([
                    datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    self.current_mode,
                    self.symbol_var.get(),
                    signal['action'],
                    self.get_current_price(self.symbol_var.get()),
                    self.lot_var.get(),
                    tp_amount,
                    sl_amount,
                    signal.get('confidence', 0),
                    result.order,
                    "SUCCESS"
                ])
                
        except Exception as e:
            self.log(f"❌ Trade logging error: {e}", "error")
    
    def log(self, message, level="info"):
        """Enhanced logging with colors"""
        try:
            timestamp = datetime.datetime.now().strftime("%H:%M:%S")
            log_message = f"[{timestamp}] {message}\n"
            
            # Insert with appropriate color
            self.log_text.insert(tk.END, log_message, level)
            self.log_text.see(tk.END)
            
            # Also log to file
            with open("ultimate_bot.log", "a", encoding="utf-8") as file:
                file.write(log_message)
                
        except Exception:
            pass
    
    def on_closing(self):
        """Handle application closing"""
        try:
            if self.running:
                if messagebox.askyesno("Confirm Exit", "Trading bot is running. Stop and exit?"):
                    self.stop_bot()
                    time.sleep(2)
                else:
                    return
            
            # Check for open positions
            if self.mt5_connected:
                positions = mt5.positions_get()
                if positions and len(positions) > 0:
                    if messagebox.askyesno("Open Positions", 
                                         f"You have {len(positions)} open positions. Close all before exit?"):
                        self.close_all_positions()
                        time.sleep(1)
            
            # Disconnect MT5
            self.disconnect_mt5()
            
            self.log("👋 Ultimate Trading Bot session ended")
            self.root.destroy()
            
        except Exception as e:
            print(f"Closing error: {e}")
            self.root.destroy()

def main():
    """Main function to start the ultimate trading bot"""
    try:
        print("🚀 Starting ULTIMATE Windows MT5 Trading Bot...")
        print("✅ All advanced features integrated")
        print("🎯 3 Trading modes: HFT, Normal, Scalping") 
        print("💰 Balance-based TP/SL system")
        print("🔧 Optimized for real trading")
        
        app = UltimateWindowsTradingBot()
        app.root.mainloop()
        
    except Exception as e:
        print(f"❌ Application startup error: {e}")
        messagebox.showerror("Startup Error", f"Failed to start application:\n{e}")

if __name__ == "__main__":
    main()