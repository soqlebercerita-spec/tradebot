"""
Enhanced Technical Indicators with Optimized Parameters
Designed to capture more market opportunities
"""

import numpy as np
from config import config

class EnhancedIndicators:
    """Enhanced technical indicators optimized for opportunity capture"""
    
    @staticmethod
    def calculate_ma(data, period=None):
        """Calculate Simple Moving Average with enhanced error handling"""
        if period is None:
            period = config.MA_PERIODS[0]
        
        if len(data) < period:
            return None
        
        try:
            return np.mean(data[-period:])
        except Exception as e:
            print(f"MA calculation error: {e}")
            return None
    
    @staticmethod
    def calculate_ema(data, period=None, alpha=None):
        """Calculate Exponential Moving Average with optimized smoothing"""
        if period is None:
            period = config.EMA_PERIODS[0]
        
        if len(data) < period:
            return None
        
        try:
            if alpha is None:
                alpha = 2 / (period + 1)
            
            ema = data[0]
            for price in data[1:]:
                ema = alpha * price + (1 - alpha) * ema
            
            return ema
        except Exception as e:
            print(f"EMA calculation error: {e}")
            return None
    
    @staticmethod
    def calculate_wma(data, period=None):
        """Calculate Weighted Moving Average"""
        if period is None:
            period = config.WMA_PERIODS[0]
        
        if len(data) < period:
            return None
        
        try:
            weights = np.arange(1, period + 1)
            recent_data = data[-period:]
            return np.average(recent_data, weights=weights)
        except Exception as e:
            print(f"WMA calculation error: {e}")
            return None
    
    @staticmethod
    def calculate_rsi(data, period=None):
        """Calculate RSI with enhanced sensitivity"""
        if period is None:
            period = config.RSI_PERIOD
        
        if len(data) < period + 1:
            return 50  # Return neutral RSI if insufficient data
        
        try:
            deltas = np.diff(data)
            gains = np.where(deltas > 0, deltas, 0)
            losses = np.where(deltas < 0, -deltas, 0)
            
            avg_gain = np.mean(gains[-period:])
            avg_loss = np.mean(losses[-period:])
            
            if avg_loss == 0:
                return 100
            
            rs = avg_gain / avg_loss
            rsi = 100 - (100 / (1 + rs))
            
            return rsi
        except Exception as e:
            print(f"RSI calculation error: {e}")
            return 50
    
    @staticmethod
    def calculate_bollinger_bands(data, period=None, deviation=None):
        """Calculate Bollinger Bands with tighter parameters"""
        if period is None:
            period = config.BB_PERIOD
        if deviation is None:
            deviation = config.BB_DEVIATION
        
        if len(data) < period:
            return None, None, None
        
        try:
            recent_data = data[-period:]
            sma = np.mean(recent_data)
            std = np.std(recent_data)
            
            upper_band = sma + (deviation * std)
            lower_band = sma - (deviation * std)
            
            return upper_band, sma, lower_band
        except Exception as e:
            print(f"Bollinger Bands calculation error: {e}")
            return None, None, None
    
    @staticmethod
    def calculate_trend_strength(data, short_period=7, long_period=20):
        """Calculate trend strength for signal confidence"""
        if len(data) < long_period:
            return 0.5
        
        try:
            short_ma = np.mean(data[-short_period:])
            long_ma = np.mean(data[-long_period:])
            
            # Calculate trend strength based on MA separation
            price_range = max(data[-long_period:]) - min(data[-long_period:])
            if price_range == 0:
                return 0.5
            
            ma_separation = abs(short_ma - long_ma)
            trend_strength = min(ma_separation / price_range, 1.0)
            
            return trend_strength
        except Exception as e:
            print(f"Trend strength calculation error: {e}")
            return 0.5
    
    @staticmethod
    def calculate_volatility(data, period=20):
        """Calculate price volatility for risk assessment"""
        if len(data) < period:
            return 0
        
        try:
            recent_data = data[-period:]
            returns = np.diff(recent_data) / recent_data[:-1]
            volatility = np.std(returns) * np.sqrt(period)
            return volatility
        except Exception as e:
            print(f"Volatility calculation error: {e}")
            return 0
    
    @staticmethod
    def enhanced_signal_analysis(close_prices, high_prices=None, low_prices=None, volume=None):
        """Enhanced signal analysis combining multiple indicators"""
        if len(close_prices) < config.MIN_DATA_POINTS:
            return {
                'signal': 'WAIT',
                'confidence': 0,
                'strength': 0,
                'indicators': {}
            }
        
        try:
            # Calculate all indicators
            current_price = close_prices[-1]
            
            # Moving Averages
            ma_short = EnhancedIndicators.calculate_ma(close_prices, config.MA_PERIODS[0])
            ma_long = EnhancedIndicators.calculate_ma(close_prices, config.MA_PERIODS[1])
            
            # EMAs
            ema_fast = EnhancedIndicators.calculate_ema(close_prices, config.EMA_PERIODS[0])
            ema_slow = EnhancedIndicators.calculate_ema(close_prices, config.EMA_PERIODS[1])
            
            # WMAs
            wma_fast = EnhancedIndicators.calculate_wma(close_prices, config.WMA_PERIODS[0])
            wma_slow = EnhancedIndicators.calculate_wma(close_prices, config.WMA_PERIODS[1])
            
            # RSI
            rsi = EnhancedIndicators.calculate_rsi(close_prices)
            
            # Bollinger Bands
            bb_upper, bb_middle, bb_lower = EnhancedIndicators.calculate_bollinger_bands(close_prices)
            
            # Trend Analysis
            trend_strength = EnhancedIndicators.calculate_trend_strength(close_prices)
            volatility = EnhancedIndicators.calculate_volatility(close_prices)
            
            # Signal Scoring System
            buy_score = 0
            sell_score = 0
            
            # MA signals (weight: 3) - Enhanced for gold trading
            if ma_short and ma_long:
                if current_price > ma_short > ma_long:
                    buy_score += 3
                elif current_price < ma_short < ma_long:
                    sell_score += 3
                # Additional signals for crossovers
                elif current_price > ma_short and ma_short > ma_long * 0.999:  # Near crossover
                    buy_score += 1
                elif current_price < ma_short and ma_short < ma_long * 1.001:  # Near crossover
                    sell_score += 1
            
            # EMA signals (weight: 2) - Enhanced for momentum
            if ema_fast and ema_slow:
                if ema_fast > ema_slow and current_price > ema_fast:
                    buy_score += 2
                elif ema_fast < ema_slow and current_price < ema_fast:
                    sell_score += 2
                # Additional momentum signals
                elif ema_fast > ema_slow * 1.001:  # Strong upward momentum
                    buy_score += 1
                elif ema_fast < ema_slow * 0.999:  # Strong downward momentum
                    sell_score += 1
            
            # WMA signals (weight: 1)
            if wma_fast and wma_slow:
                if wma_fast > wma_slow:
                    buy_score += 1
                elif wma_fast < wma_slow:
                    sell_score += 1
            
            # RSI signals - IMPROVED Quality Control for HFT
            if rsi <= 25:  # Very oversold - strong buy signal
                buy_score += 4
            elif rsi >= 75:  # Very overbought - strong sell signal
                sell_score += 4
            elif rsi <= 35:  # Oversold - moderate buy
                buy_score += 2
            elif rsi >= 65:  # Overbought - moderate sell
                sell_score += 2
            elif 45 <= rsi <= 55:  # Neutral zone - avoid trading
                buy_score -= 1
                sell_score -= 1
            
            # Bollinger Band signals (weight: 2)
            if bb_lower and bb_upper:
                if current_price <= bb_lower:
                    buy_score += 2
                elif current_price >= bb_upper:
                    sell_score += 2
            
            # Trend confirmation (weight: 1)
            if trend_strength > config.TREND_STRENGTH_MIN:
                if ma_short and ma_long and ma_short > ma_long:
                    buy_score += 1
                elif ma_short and ma_long and ma_short < ma_long:
                    sell_score += 1
            
            # Determine signal - Enhanced for real trading
            max_possible_score = 15  # Updated for new scoring weights
            buy_confidence = buy_score / max_possible_score
            sell_confidence = sell_score / max_possible_score
            
            signal = 'WAIT'
            confidence = 0
            
            # ENHANCED signal logic - Higher Quality Control
            minimum_score = config.SKOR_MINIMAL
            confidence_threshold = config.SIGNAL_CONFIDENCE_THRESHOLD
            
            # Primary signal logic - strict quality control
            if buy_score >= minimum_score and buy_confidence >= confidence_threshold and buy_confidence > sell_confidence * 1.2:
                signal = 'BUY'
                confidence = buy_confidence
            elif sell_score >= minimum_score and sell_confidence >= confidence_threshold and sell_confidence > buy_confidence * 1.2: 
                signal = 'SELL'
                confidence = sell_confidence
            # Secondary logic - require significant difference between buy/sell signals
            elif buy_score >= minimum_score and buy_confidence > sell_confidence * 1.5:
                signal = 'BUY'
                confidence = buy_confidence * 0.8  # Reduce confidence for secondary signals
            elif sell_score >= minimum_score and sell_confidence > buy_confidence * 1.5:
                signal = 'SELL'
                confidence = sell_confidence * 0.8  # Reduce confidence for secondary signals
            
            return {
                'signal': signal,
                'confidence': confidence,
                'strength': trend_strength,
                'volatility': volatility,
                'indicators': {
                    'ma_short': ma_short,
                    'ma_long': ma_long,
                    'ema_fast': ema_fast,
                    'ema_slow': ema_slow,
                    'wma_fast': wma_fast,
                    'wma_slow': wma_slow,
                    'rsi': rsi,
                    'bb_upper': bb_upper,
                    'bb_middle': bb_middle,
                    'bb_lower': bb_lower,
                    'current_price': current_price
                },
                'scores': {
                    'buy_score': buy_score,
                    'sell_score': sell_score,
                    'buy_confidence': buy_confidence,
                    'sell_confidence': sell_confidence
                }
            }
            
        except Exception as e:
            print(f"Enhanced signal analysis error: {e}")
            return {
                'signal': 'WAIT',
                'confidence': 0,
                'strength': 0,
                'indicators': {}
            }
    
    def get_signal(self, market_data, symbol):
        """Compatible get_signal method for the bot"""
        try:
            if not market_data or len(market_data) == 0:
                return {
                    'action': 'HOLD',
                    'confidence': 0,
                    'strength': 0,
                    'indicators': {}
                }
            
            # Use the enhanced signal analysis
            result = self.enhanced_signal_analysis(market_data, symbol)
            
            # Convert signal format to match expected format
            action = 'HOLD'
            if result['signal'] == 'BUY':
                action = 'BUY'
            elif result['signal'] == 'SELL':
                action = 'SELL'
            
            return {
                'action': action,
                'confidence': result['confidence'],
                'strength': result.get('strength', 0),
                'indicators': result.get('indicators', {}),
                'scores': result.get('scores', {})
            }
            
        except Exception as e:
            print(f"Get signal error: {e}")
            return {
                'action': 'HOLD',
                'confidence': 0,
                'strength': 0,
                'indicators': {}
            }
