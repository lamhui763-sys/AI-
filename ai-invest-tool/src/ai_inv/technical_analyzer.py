"""
技术分析器模块
集成数据获取和技术指标计算，提供统一的技术分析接口
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Union
from datetime import datetime, timedelta
import logging

from .indicators import TechnicalIndicators
from .data_manager import DataManager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TechnicalAnalyzer:
    """技术分析器 - 统一的技术分析接口"""
    
    def __init__(self, config: Optional[Dict] = None):
        """
        初始化技术分析器
        
        Args:
            config: 配置字典
        """
        self.config = config or {}
        self.indicators = TechnicalIndicators()
        self.data_manager = DataManager(config)
        self.logger = logger
    
    def analyze_stock(self, symbol: str, period: str = '1y', 
                      interval: str = '1d', indicators: Optional[List[str]] = None) -> pd.DataFrame:
        """
        分析单只股票的技术指标
        
        Args:
            symbol: 股票代码，如 '6158.HK'
            period: 时间周期，如 '1y', '6m', '3m'
            interval: 数据间隔，如 '1d', '1h'
            indicators: 指标列表，None表示计算所有指标
            
        Returns:
            包含技术指标的数据框
        """
        self.logger.info(f"开始分析股票: {symbol}")
        
        # 获取数据
        data = self.data_manager.get_stock_data(symbol, period=period, interval=interval)
        
        if data is None or data.empty:
            self.logger.error(f"无法获取股票 {symbol} 的数据")
            return pd.DataFrame()
        
        # 计算指标
        if indicators is None:
            # 计算所有指标
            data = self.indicators.calculate_all_indicators(data)
        else:
            # 计算指定指标
            for indicator in indicators:
                data = self._calculate_indicator(data, indicator)
        
        # 生成交易信号
        data = self.indicators.get_trading_signals(data)
        
        self.logger.info(f"股票 {symbol} 分析完成，共 {len(data)} 条数据")
        return data
    
    def analyze_watchlist(self, symbols: List[str], period: str = '1y',
                          interval: str = '1d') -> Dict[str, pd.DataFrame]:
        """
        分析多只股票（关注列表）
        
        Args:
            symbols: 股票代码列表
            period: 时间周期
            interval: 数据间隔
            
        Returns:
            股票代码到数据框的字典
        """
        self.logger.info(f"开始分析 {len(symbols)} 只股票")
        
        results = {}
        for symbol in symbols:
            try:
                data = self.analyze_stock(symbol, period=period, interval=interval)
                if not data.empty:
                    results[symbol] = data
            except Exception as e:
                self.logger.error(f"分析股票 {symbol} 时出错: {e}")
        
        self.logger.info(f"成功分析 {len(results)}/{len(symbols)} 只股票")
        return results
    
    def get_trading_signal(self, symbol: str, period: str = '3m') -> Dict:
        """
        获取单只股票的交易信号
        
        Args:
            symbol: 股票代码
            period: 分析周期
            
        Returns:
            包含交易信号的字典
        """
        # 分析股票
        data = self.analyze_stock(symbol, period=period)
        
        if data is None or data.empty:
            return {'error': '无法获取数据'}
        
        # 获取摘要
        summary = self.indicators.get_summary(data)
        
        return summary
    
    def compare_stocks(self, symbols: List[str]) -> pd.DataFrame:
        """
        比较多只股票的技术指标
        
        Args:
            symbols: 股票代码列表
            
        Returns:
            比较结果DataFrame
        """
        comparison = []
        
        for symbol in symbols:
            try:
                # 获取技术指标摘要
                signal = self.get_trading_signal(symbol, period='1y')
                
                if 'error' not in signal:
                    row = {'股票代码': symbol}
                    
                    # 添加各项指标
                    for category, indicators in signal.items():
                        if isinstance(indicators, dict):
                            for key, value in indicators.items():
                                row[f"{category}.{key}"] = value
                        else:
                            row[category] = indicators
                    
                    comparison.append(row)
            except Exception as e:
                self.logger.error(f"比较股票 {symbol} 时出错: {e}")
        
        return pd.DataFrame(comparison)
    
    def find_opportunities(self, symbols: List[str], 
                          signal_type: str = 'BUY',
                          min_strength: int = 1) -> List[Dict]:
        """
        寻找交易机会
        
        Args:
            symbols: 股票代码列表
            signal_type: 信号类型 ('BUY', 'SELL', 'STRONG BUY', 'STRONG SELL')
            min_strength: 最小信号强度
            
        Returns:
            交易机会列表
        """
        opportunities = []
        
        for symbol in symbols:
            try:
                data = self.analyze_stock(symbol, period='3m')
                
                if data is None or data.empty:
                    continue
                
                # 获取最新信号
                latest = data.iloc[-1]
                signal = latest.get('Signal', 'HOLD')
                strength = int(latest.get('Signal_Strength', 0))
                
                # 检查是否符合条件
                if signal == signal_type and strength >= min_strength:
                    opportunities.append({
                        '股票代码': symbol,
                        '信号': signal,
                        '强度': strength,
                        '收盘价': float(latest['Close']),
                        'RSI': float(latest.get('RSI_14', 0)),
                        'MACD': float(latest.get('MACD', 0)),
                        '分析时间': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    })
            
            except Exception as e:
                self.logger.error(f"分析股票 {symbol} 时出错: {e}")
        
        # 按强度排序
        opportunities.sort(key=lambda x: x['强度'], reverse=True)
        
        return opportunities
    
    def generate_report(self, symbol: str, period: str = '1y') -> str:
        """
        生成技术分析报告
        
        Args:
            symbol: 股票代码
            period: 分析周期
            
        Returns:
            格式化的分析报告文本
        """
        # 获取分析数据
        data = self.analyze_stock(symbol, period=period)
        
        if data is None or data.empty:
            return f"无法获取股票 {symbol} 的数据"
        
        # 获取摘要
        summary = self.indicators.get_summary(data)
        
        # 生成报告
        report = f"""
{'='*60}
技术分析报告
{'='*60}

股票代码: {symbol}
分析日期: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
分析周期: {period}

{'='*60}
一、价格信息
{'='*60}
收盘价: {summary['价格']['收盘价']:.2f}
涨跌幅: {summary['价格']['涨跌幅']}

{'='*60}
二、趋势指标
{'='*60}
"""
        for key, value in summary['趋势指标'].items():
            report += f"{key}: {value}\n"
        
        report += f"""
{'='*60}
三、动量指标
{'='*60}
"""
        for key, value in summary['动量指标'].items():
            report += f"{key}: {value}\n"
        
        if '交易信号' in summary:
            report += f"""
{'='*60}
四、交易信号
{'='*60}
信号: {summary['交易信号']}
强度: {summary['信号强度']}/5
"""
        
        # 添加技术建议
        signal = summary.get('交易信号', 'HOLD')
        rsi = float(summary.get('动量指标', {}).get('RSI', 50))
        
        report += f"""
{'='*60}
五、技术建议
{'='*60}
"""
        
        if signal == 'STRONG BUY':
            report += "建议: 强力买入\n"
            report += "理由: 多项技术指标显示买入信号\n"
        elif signal == 'BUY':
            report += "建议: 买入\n"
            report += "理由: 技术指标偏多\n"
        elif signal == 'STRONG SELL':
            report += "建议: 强力卖出\n"
            report += "理由: 多项技术指标显示卖出信号\n"
        elif signal == 'SELL':
            report += "建议: 卖出\n"
            report += "理由: 技术指标偏空\n"
        else:
            report += "建议: 观望\n"
            report += "理由: 技术指标显示中性\n"
        
        # 风险提示
        if rsi > 80:
            report += "\n风险提示: RSI极高，存在回调风险\n"
        elif rsi < 20:
            report += "\n机会提示: RSI极低，可能存在反彈機會\n"
        
        report += f"\n{'='*60}\n"
        
        return report
    
    def export_analysis(self, symbol: str, filepath: str, 
                        period: str = '1y', format: str = 'excel') -> bool:
        """
        导出技术分析结果
        
        Args:
            symbol: 股票代码
            filepath: 导出文件路径
            period: 分析周期
            format: 导出格式 ('excel', 'csv')
            
        Returns:
            是否成功
        """
        try:
            # 获取分析数据
            data = self.analyze_stock(symbol, period=period)
            
            if data is None or data.empty:
                self.logger.error("没有数据可导出")
                return False
            
            # 导出数据
            if format == 'excel':
                data.to_excel(filepath, index=False)
            elif format == 'csv':
                data.to_csv(filepath, index=False, encoding='utf-8-sig')
            else:
                self.logger.error(f"不支持的导出格式: {format}")
                return False
            
            self.logger.info(f"成功导出到: {filepath}")
            return True
        
        except Exception as e:
            self.logger.error(f"导出失败: {e}")
            return False
    
    def _calculate_indicator(self, data: pd.DataFrame, indicator: str) -> pd.DataFrame:
        """
        计算单个指标
        
        Args:
            data: 数据框
            indicator: 指标名称
            
        Returns:
            包含指标的数据框
        """
        indicator_map = {
            'sma5': lambda d: self.indicators.sma(d, 5),
            'sma10': lambda d: self.indicators.sma(d, 10),
            'sma20': lambda d: self.indicators.sma(d, 20),
            'sma50': lambda d: self.indicators.sma(d, 50),
            'sma200': lambda d: self.indicators.sma(d, 200),
            'ema12': lambda d: self.indicators.ema(d, 12),
            'ema26': lambda d: self.indicators.ema(d, 26),
            'bollinger': lambda d: self.indicators.bollinger_bands(d),
            'rsi': lambda d: self.indicators.rsi(d),
            'macd': lambda d: self.indicators.macd(d),
            'stoch': lambda d: self.indicators.stoch_oscillator(d),
            'williams': lambda d: self.indicators.williams_r(d),
            'obv': lambda d: self.indicators.obv(d),
            'atr': lambda d: self.indicators.atr(d),
            'keltner': lambda d: self.indicators.keltner_channels(d),
        }
        
        if indicator in indicator_map:
            return indicator_map[indicator](data)
        else:
            self.logger.warning(f"未知指标: {indicator}")
            return data
    
    def get_trend_analysis(self, symbol: str, period: str = '3m') -> Dict:
        """
        获取趋势分析
        
        Args:
            symbol: 股票代码
            period: 分析周期
            
        Returns:
            趋势分析字典
        """
        data = self.analyze_stock(symbol, period=period)
        
        if data is None or data.empty:
            return {'error': '无法获取数据'}
        
        latest = data.iloc[-1]
        
        # 趋势判断
        trend = {
            '短期趋势': self._judge_trend(data, 5, 20),
            '中期趋势': self._judge_trend(data, 20, 50),
            '长期趋势': self._judge_trend(data, 50, 200),
            '整体趋势': '上升' if latest['SMA_5'] > latest['SMA_200'] else '下降',
            '趋势强度': abs(latest['SMA_5'] - latest['SMA_200']) / latest['SMA_200'] * 100,
        }
        
        return trend
    
    def _judge_trend(self, data: pd.DataFrame, short: int, long: int) -> str:
        """
        判断趋势
        
        Args:
            data: 数据框
            short: 短期均线周期
            long: 长期均线周期
            
        Returns:
            趋势描述
        """
        latest = data.iloc[-1]
        
        short_ma = latest[f'SMA_{short}']
        long_ma = latest[f'SMA_{long}']
        
        if short_ma > long_ma:
            return '上升'
        elif short_ma < long_ma:
            return '下降'
        else:
            return '横盘'
