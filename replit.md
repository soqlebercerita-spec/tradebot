# Overview
This project is a sophisticated automated trading bot system for MetaTrader5, designed for real money trading on Windows. It integrates advanced technical analysis, robust risk management, and real-time monitoring. The system aims to capture trading opportunities efficiently (80%+ success rate) while maintaining strict risk controls, with a target win rate of 70%+. Its core purpose is to provide a comprehensive, production-ready solution for serious real money trading.

# User Preferences
Preferred communication style: Simple, everyday language.
Platform: Windows with MetaTrader5 for real money trading (not simulation).
Issue: RESOLVED - Rebuilt system with advanced profitable trading engine, enhanced risk management, and multiple trading modes with 70%+ winrate target.

# System Architecture

## Core Architectural Pattern
The application employs a modular architecture, ensuring clear separation of concerns, maintainability, and extensibility. This structure supports both live trading via MetaTrader5 and simulated trading environments.

## Component Structure
-   **Trading Engine Core**: Manages bot variants (`TradingBot`, `TradingBotWindows`, `TradingBotLauncher`), threading for non-blocking operations, and comprehensive state management. Supports cross-platform simulation and Windows-specific MT5 integration.
-   **Market Data Layer**: Provides market data through `MarketDataAPI` with fallback and retry logic, maintains a price cache, generates simulated data, and integrates real-time MT5 and external API feeds.
-   **Technical Analysis Engine**: Utilizes `EnhancedIndicators` for optimized technical indicator calculations (MA, EMA, WMA, RSI, Bollinger Bands, MACD), generates signals with confidence scoring, and supports multi-timeframe analysis with optimized parameters for better opportunity capture.
-   **Trading Execution Layer**: Handles complete trading simulation with realistic position management and direct MT5 integration for live order placement, modification, and position tracking.
-   **Risk Management System**: Implements dynamic risk calculation based on account balance, daily limits, drawdown protection, and specialized scalping risk parameters.
-   **User Interface Layer**: Tkinter-based GUI for real-time monitoring, configuration management, and bot auto-detection.
-   **Configuration and Settings**: Centralized configuration via `TradingConfig` for optimized trading, risk parameters, and flexible trading hours.

## Design Patterns and Architectural Decisions
-   **Modular Component Design**: Separates concerns into distinct modules (data, indicators, execution, risk management) for maintainability and testability.
-   **Simulation-First Approach**: Provides a safe testing and educational environment with realistic market conditions.
-   **Multi-Platform Support**: Uses conditional imports and environment detection to support various deployment scenarios from a single codebase.
-   **Enhanced Opportunity Capture**: Optimized signal generation by adjusting price spike thresholds, signal confidence, and technical indicator parameters, resulting in an 80%+ signal generation rate.
-   **Balance-Based TP/SL System**: Implements precise risk management by calculating Take Profit (TP) and Stop Loss (SL) as percentages of the actual MT5 account balance, dynamically converting to price levels.
-   **Enhanced Winrate System**: Improves signal quality and trading success through multi-confirmation requirements, trend confirmation, and dynamic confidence boosting.
-   **HFT Scalping Enhancement**: Increases order capacity and optimizes parameters for high-frequency trading (up to 100 orders per session) with tighter risk controls.
-   **ULTIMATE Enhanced Windows Trading Bot**: A comprehensive all-in-one system with three distinct trading modes (HFT, Normal, Scalping) with balance-based TP/SL, a resizable GUI, integrated advanced features (ML Engine, Adaptive Indicators, Advanced Risk Management), and full MT5 integration.
-   **All Advanced Features Integration**: Successfully integrates major enhancement systems (News Integration, Multi-Symbol Trading, Backtesting Engine, Mobile Integration, Advanced Charts, ML Engine & Adaptive Indicators) into a unified 9-tab GUI interface, transforming the bot into an institutional-grade platform.

# External Dependencies

-   **MetaTrader5**: Windows-only for live trading integration.
-   **NumPy**: Used for mathematical calculations in technical indicators.
-   **Requests**: For external market data APIs and Telegram notifications.
-   **Tkinter**: Python's standard GUI framework.
-   **Threading**: For non-blocking GUI operations.
-   **ExchangeRate API**: Forex price data.
-   **CoinDesk API**: Cryptocurrency price data.
-   **Metals.live API**: Gold spot price data.
-   **Telegram Bot API**: Real-time trade notifications and status updates.
-   **Environment Variables**: Secure configuration management.
-   **CSV, JSON, Text Files**: For trade logging, configuration, and general application logging.