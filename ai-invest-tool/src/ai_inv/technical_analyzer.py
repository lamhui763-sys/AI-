'''
技术分析器模块
集成数据获取和技术指标计算，提供统一的技术分析接口
'''

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Union
from datetime import datetime, timedelta
import logging

# 确保我们从正确的模块导入
from .indicators import TechnicalIndicators
from .data_fetcher import DataFetcher

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TechnicalAnalyzer:
    """技术分析器 - 重构后，提供稳健、统一的技术分析接口"""
    
    def __init__(self, config: Optional[Dict] = None):
        """
        初始化技术分析器
        """
        self.config = config or {}
        self.indicators = TechnicalIndicators()
        self.data_fetcher = DataFetcher()
        self.logger = logger
        # 添加一个简单的缓存来避免在同一次会话中重复获取和计算
        self.analysis_cache = {}

    def analyze_stock(self, symbol: str, period: str = '1y', 
                      interval: str = '1d') -> Optional[pd.DataFrame]:
        """
        分析单只股票的技术指标。这个函数是核心入口点。
        它获取原始数据，然后计算所有技术指标，最后返回一个包含所有信息的DataFrame。
        
        Args:
            symbol: 股票代码
            period: 时间周期
            interval: 数据间隔
            
        Returns:
            一个包含价格和所有技术指标的DataFrame，如果失败则返回None。
        """
        self.logger.info(f"开始为 {symbol} 分析周期 {period} 的数据")
        cache_key = f"{symbol}_{period}_{interval}"
        
        if cache_key in self.analysis_cache:
            self.logger.info(f"从缓存加载 {symbol} 的分析数据")
            return self.analysis_cache[cache_key]

        try:
            # 1. 获取历史数据
            data = self.data_fetcher.get_historical_data(symbol, period=period, interval=interval)
            
            if data is None or data.empty:
                self.logger.error(f"无法获取股票 {symbol} 的数据")
                return None
            
            # 2. 计算所有技术指标
            # `calculate_all_indicators` 应该返回一个附加了所有指标列的新DataFrame
            indicators_df = self.indicators.calculate_all_indicators(data.copy())
            
            self.logger.info(f"股票 {symbol} 分析完成，共 {len(indicators_df)} 条数据")
            
            # 3. 存入缓存并返回结果
            self.analysis_cache[cache_key] = indicators_df
            return indicators_df

        except Exception as e:
            self.logger.error(f"在 analyze_stock (symbol: {symbol}) 中发生意外错误: {e}", exc_info=True)
            return None

    def get_trading_signal(self, data: pd.DataFrame) -> Dict:
        """
        从一个已经包含技术指标的DataFrame中，安全地提取最新的交易信号。
        这个函数是高效的，因为它不执行任何I/O或重度计算。
        
        Args:
            data: 包含技术指标的DataFrame。
            
        Returns:
            一个包含交易信号和强度的字典。
        """
        if data is None or data.empty:
            return {'交易信号': 'N/A', '强度': 'N/A', 'error': '输入数据为空'}
        
        try:
            latest = data.iloc[-1]
            
            # 使用.get()方法安全地从DataFrame的最新行中获取值，如果列不存在则返回'N/A'
            signal = latest.get('Signal', 'N/A')
            strength = latest.get('Signal_Strength', 'N/A')
            
            # 返回的字典键与UI中st.metric的标签匹配
            return {
                '交易信号': signal,
                '强度': strength
            }
        except Exception as e:
            self.logger.error(f"在 get_trading_signal 中发生错误: {e}", exc_info=True)
            return {'交易信号': '错误', '强度': '错误', 'error': f'计算信号时出错: {e}'}
