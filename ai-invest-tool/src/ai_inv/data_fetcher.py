"""
Data Fetcher Module - 数据获取模块
负责从各种数据源获取股票数据

Author: WorkBuddy AI
Version: 1.0.0
"""

import pandas as pd
import numpy as np
import yfinance as yf
import logging
from datetime import datetime, timedelta
from typing import Optional, Dict, List


class DataFetcher:
    """数据获取器"""

    def __init__(self, config: Optional[Dict] = None):
        """
        初始化数据获取器

        Args:
            config: 配置字典
        """
        self.config = config or {}
        self.logger = logging.getLogger(__name__)

        # Yahoo Finance配置
        self.yf_enabled = self.config.get('yahoo_finance', {}).get('enabled', True)
        self.yf_timeout = self.config.get('yahoo_finance', {}).get('timeout', 30)

        # Alpha Vantage配置
        self.av_enabled = 'alpha_vantage' in self.config
        self.av_api_key = self.config.get('alpha_vantage', {}).get('api_key', '')
        self.av_output_size = self.config.get('alpha_vantage', {}).get('output_size', 'full')

        self.logger.info("DataFetcher initialized")

    def get_historical_data(self, symbol: str, period: str = '1y',
                            interval: str = '1d') -> Optional[pd.DataFrame]:
        """
        获取历史数据 (兼容性方法)
        """
        return self.fetch_stock_data(symbol, period, interval)

    def fetch_stock_data(self, symbol: str, period: str = '1y',
                        interval: str = '1d') -> Optional[pd.DataFrame]:
        """
        获取股票数据

        Args:
            symbol: 股票代码 (如 '6158.HK', '^HSI')
            period: 时间周期 ('1y', '2y', '5y', 'max')
            interval: 数据间隔 ('1d', '1wk', '1mo')

        Returns:
            DataFrame: 股票数据，包含OHLCV
        """
        self.logger.info(f"Fetching {symbol} data: period={period}, interval={interval}")

        try:
            # 优先使用Yahoo Finance
            if self.yf_enabled:
                data = self._fetch_from_yahoo(symbol, period, interval)
                if data is not None and not data.empty:
                    return data

            # 尝试Alpha Vantage
            if self.av_enabled:
                data = self._fetch_from_alpha_vantage(symbol)
                if data is not None and not data.empty:
                    return data

            self.logger.warning(f"No data found for {symbol}")
            return None

        except Exception as e:
            self.logger.error(f"Error fetching {symbol}: {str(e)}")
            return None

    def _fetch_from_yahoo(self, symbol: str, period: str,
                         interval: str) -> Optional[pd.DataFrame]:
        """从Yahoo Finance获取数据"""
        try:
            # 创建ticker对象
            ticker = yf.Ticker(symbol)

            # 获取历史数据
            data = ticker.history(
                period=period,
                interval=interval,
                timeout=self.yf_timeout
            )

            # 检查数据
            if data is None or data.empty:
                self.logger.warning(f"No data from Yahoo for {symbol}")
                return None

            # 标准化列名
            data.columns = ['Open', 'High', 'Low', 'Close', 'Volume']

            # 重置索引
            data.reset_index(inplace=True)

            # 转换日期格式
            data['Date'] = pd.to_datetime(data['Date'])
            data.set_index('Date', inplace=True)

            # 填充缺失值
            data = data.ffill().bfill()

            self.logger.info(f"Successfully fetched {len(data)} records from Yahoo")
            return data

        except Exception as e:
            self.logger.error(f"Yahoo Finance error: {str(e)}")
            return None

    def _fetch_from_alpha_vantage(self, symbol: str) -> Optional[pd.DataFrame]:
        """从Alpha Vantage获取数据"""
        try:
            import requests

            # API URL
            base_url = "https://www.alphavantage.co/query"
            params = {
                'function': 'TIME_SERIES_DAILY',
                'symbol': symbol.replace('.HK', '.HKG'),  # 转换港股代码
                'outputsize': self.av_output_size,
                'apikey': self.av_api_key,
                'datatype': 'csv'
            }

            # 发送请求
            response = requests.get(base_url, params=params, timeout=30)

            if response.status_code != 200:
                self.logger.error(f"Alpha Vantage API error: {response.status_code}")
                return None

            # 解析CSV数据
            from io import StringIO
            data = pd.read_csv(StringIO(response.text))

            if data.empty:
                return None

            # 标准化列名
            data.columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']

            # 转换日期
            data['Date'] = pd.to_datetime(data['Date'])
            data.set_index('Date', inplace=True)

            # 确保数据顺序
            data.sort_index(inplace=True)

            self.logger.info(f"Successfully fetched {len(data)} records from Alpha Vantage")
            return data

        except Exception as e:
            self.logger.error(f"Alpha Vantage error: {str(e)}")
            return None

    def fetch_historical_data(self, symbol: str, start_date: str,
                             end_date: Optional[str] = None) -> Optional[pd.DataFrame]:
        """
        获取历史数据（用于回测）

        Args:
            symbol: 股票代码
            start_date: 开始日期 (YYYY-MM-DD)
            end_date: 结束日期 (YYYY-MM-DD)，默认为今天

        Returns:
            DataFrame: 历史数据
        """
        self.logger.info(f"Fetching historical data for {symbol} from {start_date}")

        try:
            # 转换日期
            start = datetime.strptime(start_date, '%Y-%m-%d')
            end = datetime.strptime(end_date, '%Y-%m-%d') if end_date else datetime.now()

            # 计算时间跨度
            days = (end - start).days

            # 估算period
            if days <= 365:
                period = '1y'
            elif days <= 730:
                period = '2y'
            elif days <= 1825:
                period = '5y'
            else:
                period = 'max'

            # 获取数据
            data = self.fetch_stock_data(symbol, period, '1d')

            if data is None:
                return None

            # 过滤日期范围
            data = data.loc[start:end]

            return data

        except Exception as e:
            self.logger.error(f"Error fetching historical data: {str(e)}")
            return None

    def fetch_multiple_stocks(self, symbols: List[str],
                             period: str = '1y',
                             interval: str = '1d') -> Dict[str, pd.DataFrame]:
        """
        获取多只股票数据

        Args:
            symbols: 股票代码列表
            period: 时间周期
            interval: 数据间隔

        Returns:
            dict: {symbol: DataFrame}
        """
        results = {}

        for symbol in symbols:
            data = self.fetch_stock_data(symbol, period, interval)
            if data is not None:
                results[symbol] = data

        return results

    def get_current_price(self, symbol: str) -> Optional[float]:
        """
        获取当前价格

        Args:
            symbol: 股票代码

        Returns:
            float: 当前价格
        """
        try:
            ticker = yf.Ticker(symbol)
            data = ticker.history(period='1d', interval='1m', timeout=10)

            if data is None or data.empty:
                return None

            return data['Close'].iloc[-1]

        except Exception as e:
            self.logger.error(f"Error getting current price: {str(e)}")
            return None

    def get_stock_info(self, symbol: str) -> Optional[Dict]:
        """
        获取股票基本信息

        Args:
            symbol: 股票代码

        Returns:
            dict: 股票信息
        """
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info

            # 提取关键信息
            key_info = {
                'name': info.get('longName', 'N/A'),
                'sector': info.get('sector', 'N/A'),
                'industry': info.get('industry', 'N/A'),
                'market_cap': info.get('marketCap', 0),
                'pe_ratio': info.get('forwardPE', 0),
                'dividend_yield': info.get('dividendYield', 0),
                '52_week_high': info.get('fiftyTwoWeekHigh', 0),
                '52_week_low': info.get('fiftyTwoWeekLow', 0),
                'beta': info.get('beta', 0),
            }

            return key_info

        except Exception as e:
            self.logger.error(f"Error getting stock info: {str(e)}")
            return None
