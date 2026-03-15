"""
技术分析指标模块
提供各种技术分析指标的计算功能，包括移动平均、RSI、MACD等
"""

import pandas as pd
import numpy as np
from typing import Union, Dict, List
import warnings

warnings.filterwarnings('ignore')


class TechnicalIndicators:
    """技术指标计算类"""
    
    def __init__(self):
        """初始化技术指标计算器"""
        pass
    
    # ==================== 趋势指标 ====================
    
    def sma(self, data: pd.DataFrame, period: int = 20, price_col: str = 'Close') -> pd.DataFrame:
        """
        计算简单移动平均线 (SMA - Simple Moving Average)
        
        Args:
            data: 包含OHLC数据的DataFrame
            period: 周期，默认20
            price_col: 价格列名，默认'Close'
            
        Returns:
            包含SMA指标的DataFrame
            
        Example:
            >>> df = pd.DataFrame({'Close': [1, 2, 3, 4, 5]})
            >>> ti = TechnicalIndicators()
            >>> result = ti.sma(df, period=3)
        """
        result = data.copy()
        result[f'SMA_{period}'] = data[price_col].rolling(window=period).mean()
        return result
    
    def ema(self, data: pd.DataFrame, period: int = 12, price_col: str = 'Close') -> pd.DataFrame:
        """
        计算指数移动平均线 (EMA - Exponential Moving Average)
        
        Args:
            data: 包含OHLC数据的DataFrame
            period: 周期，默认12
            price_col: 价格列名，默认'Close'
            
        Returns:
            包含EMA指标的DataFrame
        """
        result = data.copy()
        result[f'EMA_{period}'] = data[price_col].ewm(span=period, adjust=False).mean()
        return result
    
    def bollinger_bands(self, data: pd.DataFrame, period: int = 20, 
                        std_dev: int = 2, price_col: str = 'Close') -> pd.DataFrame:
        """
        计算布林带 (Bollinger Bands)
        
        Args:
            data: 包含OHLC数据的DataFrame
            period: 周期，默认20
            std_dev: 标准差倍数，默认2
            price_col: 价格列名，默认'Close'
            
        Returns:
            包含上轨、中轨、下轨的DataFrame
        """
        result = data.copy()
        sma = data[price_col].rolling(window=period).mean()
        std = data[price_col].rolling(window=period).std()
        
        result['BB_Upper'] = sma + (std_dev * std)
        result['BB_Middle'] = sma
        result['BB_Lower'] = sma - (std_dev * std)
        result['BB_Width'] = (result['BB_Upper'] - result['BB_Lower']) / result['BB_Middle']
        
        return result
    
    # ==================== 动量指标 ====================
    
    def rsi(self, data: pd.DataFrame, period: int = 14, price_col: str = 'Close') -> pd.DataFrame:
        """
        计算相对强弱指标 (RSI - Relative Strength Index)
        
        RSI范围：0-100
        - RSI > 70: 超买，可能回调
        - RSI < 30: 超卖，可能反弹
        
        Args:
            data: 包含OHLC数据的DataFrame
            period: 周期，默认14
            price_col: 价格列名，默认'Close'
            
        Returns:
            包含RSI指标的DataFrame
        """
        result = data.copy()
        
        # 计算价格变化
        delta = data[price_col].diff()
        
        # 分离涨跌
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        
        # 计算RSI
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        
        result[f'RSI_{period}'] = rsi
        return result
    
    def macd(self, data: pd.DataFrame, fast_period: int = 12, 
             slow_period: int = 26, signal_period: int = 9,
             price_col: str = 'Close') -> pd.DataFrame:
        """
        计算MACD指标 (Moving Average Convergence Divergence)
        
        包含：
        - MACD线 = EMA(12) - EMA(26)
        - 信号线 = EMA(MACD, 9)
        - 柱状图 = MACD - 信号线
        
        Args:
            data: 包含OHLC数据的DataFrame
            fast_period: 快线周期，默认12
            slow_period: 慢线周期，默认26
            signal_period: 信号线周期，默认9
            price_col: 价格列名，默认'Close'
            
        Returns:
            包含MACD指标的DataFrame
        """
        result = data.copy()
        
        # 计算快慢EMA
        ema_fast = data[price_col].ewm(span=fast_period, adjust=False).mean()
        ema_slow = data[price_col].ewm(span=slow_period, adjust=False).mean()
        
        # 计算MACD线
        macd_line = ema_fast - ema_slow
        result['MACD'] = macd_line
        
        # 计算信号线
        signal_line = macd_line.ewm(span=signal_period, adjust=False).mean()
        result['MACD_Signal'] = signal_line
        
        # 计算柱状图
        result['MACD_Histogram'] = macd_line - signal_line
        
        return result
    
    def stoch_oscillator(self, data: pd.DataFrame, k_period: int = 14, 
                         d_period: int = 3) -> pd.DataFrame:
        """
        计算随机震荡指标 (Stochastic Oscillator)
        
        包含：
        - %K = (当前收盘价 - N日内最低价) / (N日内最高价 - N日内最低价) * 100
        - %D = %K的M日移动平均
        
        Args:
            data: 包含OHLC数据的DataFrame
            k_period: %K周期，默认14
            d_period: %D周期，默认3
            
        Returns:
            包含随机震荡指标的DataFrame
        """
        result = data.copy()
        
        # 计算%K
        low_min = data['Low'].rolling(window=k_period).min()
        high_max = data['High'].rolling(window=k_period).max()
        
        result['Stoch_K'] = ((data['Close'] - low_min) / (high_max - low_min)) * 100
        
        # 计算%D
        result['Stoch_D'] = result['Stoch_K'].rolling(window=d_period).mean()
        
        return result
    
    def williams_r(self, data: pd.DataFrame, period: int = 14) -> pd.DataFrame:
        """
        计算威廉指标 (Williams %R)
        
        范围：-100到0
        - %R > -20: 超买
        - %R < -80: 超卖
        
        Args:
            data: 包含OHLC数据的DataFrame
            period: 周期，默认14
            
        Returns:
            包含威廉指标的DataFrame
        """
        result = data.copy()
        
        high_max = data['High'].rolling(window=period).max()
        low_min = data['Low'].rolling(window=period).min()
        
        result['Williams_R'] = -100 * ((high_max - data['Close']) / (high_max - low_min))
        
        return result
    
    # ==================== 成交量指标 ====================
    
    def obv(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        计算能量潮指标 (OBV - On Balance Volume)
        
        OBV = 昨日OBV + 当日成交量（若上涨）
        OBV = 昨日OBV - 当日成交量（若下跌）
        
        Args:
            data: 包含OHLCV数据的DataFrame
            
        Returns:
            包含OBV指标的DataFrame
        """
        result = data.copy()
        
        # 计算OBV
        obv = (np.sign(data['Close'].diff()) * data['Volume']).fillna(0).cumsum()
        result['OBV'] = obv
        
        # 计算OBV移动平均
        result['OBV_MA'] = result['OBV'].rolling(window=20).mean()
        
        return result
    
    def volume_sma(self, data: pd.DataFrame, period: int = 20) -> pd.DataFrame:
        """
        计算成交量移动平均
        
        Args:
            data: 包含OHLCV数据的DataFrame
            period: 周期，默认20
            
        Returns:
            包含成交量MA的DataFrame
        """
        result = data.copy()
        result[f'Volume_MA_{period}'] = data['Volume'].rolling(window=period).mean()
        return result
    
    # ==================== 波动率指标 ====================
    
    def atr(self, data: pd.DataFrame, period: int = 14) -> pd.DataFrame:
        """
        计算平均真实波幅 (ATR - Average True Range)
        
        衡量市场波动性
        
        Args:
            data: 包含OHLC数据的DataFrame
            period: 周期，默认14
            
        Returns:
            包含ATR指标的DataFrame
        """
        result = data.copy()
        
        # 计算真实波幅
        high_low = data['High'] - data['Low']
        high_close = np.abs(data['High'] - data['Close'].shift())
        low_close = np.abs(data['Low'] - data['Close'].shift())
        
        true_range = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
        
        # 计算ATR
        result['ATR'] = true_range.rolling(window=period).mean()
        
        return result
    
    def keltner_channels(self, data: pd.DataFrame, period: int = 20, 
                          atr_period: int = 14, multiplier: float = 2.0) -> pd.DataFrame:
        """
        计算肯特纳通道 (Keltner Channels)
        
        类似于布林带，但使用ATR代替标准差
        
        Args:
            data: 包含OHLC数据的DataFrame
            period: EMA周期，默认20
            atr_period: ATR周期，默认14
            multiplier: ATR倍数，默认2.0
            
        Returns:
            包含肯特纳通道的DataFrame
        """
        result = data.copy()
        
        # 计算EMA和ATR
        ema = data['Close'].ewm(span=period, adjust=False).mean()
        atr = self.atr(data, period=atr_period)['ATR']
        
        # 计算通道
        result['KC_Upper'] = ema + (multiplier * atr)
        result['KC_Middle'] = ema
        result['KC_Lower'] = ema - (multiplier * atr)
        
        return result
    
    # ==================== 综合分析 ====================
    
    def calculate_all_indicators(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        计算所有技术指标
        
        Args:
            data: 包含OHLCV数据的DataFrame
            
        Returns:
            包含所有技术指标的DataFrame
        """
        result = data.copy()
        
        # 趋势指标
        result = self.sma(result, period=5)
        result = self.sma(result, period=10)
        result = self.sma(result, period=20)
        result = self.sma(result, period=50)
        result = self.sma(result, period=200)
        result = self.ema(result, period=12)
        result = self.ema(result, period=26)
        result = self.bollinger_bands(result)
        
        # 动量指标
        result = self.rsi(result)
        result = self.macd(result)
        result = self.stoch_oscillator(result)
        result = self.williams_r(result)
        
        # 成交量指标
        result = self.obv(result)
        result = self.volume_sma(result)
        
        # 波动率指标
        result = self.atr(result)
        result = self.keltner_channels(result)
        
        return result
    
    def get_trading_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        生成交易信号
        
        基于多个指标的综合分析
        
        Args:
            data: 包含技术指标的DataFrame
            
        Returns:
            包含交易信号的DataFrame
        """
        result = data.copy()
        
        # 初始化信号列
        result['Signal'] = 'HOLD'
        result['Signal_Strength'] = 0
        
        # 基于多个指标生成信号
        signals = []
        strengths = []
        
        for i in range(1, len(data)):
            signal = 'HOLD'
            strength = 0
            reasons = []
            
            try:
                # RSI信号
                rsi_val = data['RSI_14'].iloc[i]
                if rsi_val < 30:
                    signal = 'BUY'
                    strength += 1
                    reasons.append('RSI超卖')
                elif rsi_val > 70:
                    signal = 'SELL'
                    strength -= 1
                    reasons.append('RSI超买')
                
                # MACD信号
                macd = data['MACD'].iloc[i]
                macd_signal = data['MACD_Signal'].iloc[i]
                macd_hist = data['MACD_Histogram'].iloc[i]
                
                if macd_hist > 0 and data['MACD_Histogram'].iloc[i-1] <= 0:
                    if signal != 'SELL':
                        signal = 'BUY'
                        strength += 2
                        reasons.append('MACD金叉')
                elif macd_hist < 0 and data['MACD_Histogram'].iloc[i-1] >= 0:
                    if signal != 'BUY':
                        signal = 'SELL'
                        strength -= 2
                        reasons.append('MACD死叉')
                
                # 移动平均线信号
                sma_short = data['SMA_5'].iloc[i]
                sma_long = data['SMA_20'].iloc[i]
                
                if sma_short > sma_long and data['SMA_5'].iloc[i-1] <= data['SMA_20'].iloc[i-1]:
                    if signal != 'SELL':
                        signal = 'BUY'
                        strength += 1
                        reasons.append('短期均线金叉')
                elif sma_short < sma_long and data['SMA_5'].iloc[i-1] >= data['SMA_20'].iloc[i-1]:
                    if signal != 'BUY':
                        signal = 'SELL'
                        strength -= 1
                        reasons.append('短期均线死叉')
                
                # 布林带信号
                bb_upper = data['BB_Upper'].iloc[i]
                bb_lower = data['BB_Lower'].iloc[i]
                close = data['Close'].iloc[i]
                
                if close <= bb_lower:
                    if signal != 'SELL':
                        signal = 'BUY'
                        strength += 1
                        reasons.append('触及布林下轨')
                elif close >= bb_upper:
                    if signal != 'BUY':
                        signal = 'SELL'
                        strength -= 1
                        reasons.append('触及布林上轨')
                
                # 成交量确认
                vol = data['Volume'].iloc[i]
                vol_ma = data['Volume_MA_20'].iloc[i]
                
                if vol > vol_ma * 1.5:
                    if signal == 'BUY':
                        strength += 1
                        reasons.append('成交量放大')
                    elif signal == 'SELL':
                        strength -= 1
                        reasons.append('成交量放大')
                
                # 综合判断
                if strength >= 3:
                    signal = 'STRONG BUY'
                elif strength >= 1:
                    signal = 'BUY'
                elif strength <= -3:
                    signal = 'STRONG SELL'
                elif strength <= -1:
                    signal = 'SELL'
                else:
                    signal = 'HOLD'
                
            except (KeyError, IndexError):
                pass
            
            signals.append(signal)
            strengths.append(abs(strength))
        
        # 添加第一行（无信号）
        signals.insert(0, 'HOLD')
        strengths.insert(0, 0)
        
        result['Signal'] = signals
        result['Signal_Strength'] = strengths
        
        return result
    
    def get_summary(self, data: pd.DataFrame, latest: bool = True) -> Dict:
        """
        获取技术指标摘要
        
        Args:
            data: 包含技术指标的DataFrame
            latest: 是否只返回最新数据，默认True
            
        Returns:
            技术指标摘要字典
        """
        if latest:
            df = data.tail(1)
        else:
            df = data
        
        summary = {
            '价格': {
                '收盘价': float(df['Close'].iloc[-1]),
                '涨跌': float(df['Close'].iloc[-1] - df['Close'].iloc[-2]) if len(df) > 1 else 0,
                '涨跌幅': f"{(df['Close'].iloc[-1] - df['Close'].iloc[-2]) / df['Close'].iloc[-2] * 100:.2f}%" if len(df) > 1 else "0%"
            },
            '趋势指标': {},
            '动量指标': {},
            '成交量指标': {},
            '波动率指标': {}
        }
        
        # 趋势指标
        if 'SMA_20' in df.columns:
            summary['趋势指标']['20日均线'] = f"{df['SMA_20'].iloc[-1]:.2f}"
        if 'SMA_50' in df.columns:
            summary['趋势指标']['50日均线'] = f"{df['SMA_50'].iloc[-1]:.2f}"
        if 'BB_Upper' in df.columns:
            summary['趋势指标']['布林上轨'] = f"{df['BB_Upper'].iloc[-1]:.2f}"
            summary['趋势指标']['布林下轨'] = f"{df['BB_Lower'].iloc[-1]:.2f}"
        
        # 动量指标
        if 'RSI_14' in df.columns:
            rsi = df['RSI_14'].iloc[-1]
            summary['动量指标']['RSI'] = f"{rsi:.2f}"
            if rsi > 70:
                summary['动量指标']['RSI状态'] = '超买'
            elif rsi < 30:
                summary['动量指标']['RSI状态'] = '超卖'
            else:
                summary['动量指标']['RSI状态'] = '正常'
        
        if 'MACD' in df.columns:
            summary['动量指标']['MACD'] = f"{df['MACD'].iloc[-1]:.4f}"
            summary['动量指标']['MACD信号线'] = f"{df['MACD_Signal'].iloc[-1]:.4f}"
            summary['动量指标']['MACD柱'] = f"{df['MACD_Histogram'].iloc[-1]:.4f}"
        
        # 交易信号
        if 'Signal' in df.columns:
            summary['交易信号'] = df['Signal'].iloc[-1]
            summary['信号强度'] = int(df['Signal_Strength'].iloc[-1])
        
        return summary
