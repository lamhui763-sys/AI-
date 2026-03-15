"""
Data Manager Module - 数据管理模块
统一管理数据获取、处理和存储

Author: WorkBuddy AI
Version: 1.0.0
"""

import logging
from typing import Optional, Dict, List
from datetime import datetime, timedelta

from .data_fetcher import DataFetcher
from .data_processor import DataProcessor


class DataManager:
    """数据管理器 - 统一接口"""

    def __init__(self, config):
        """
        初始化数据管理器

        Args:
            config: 配置字典
        """
        self.config = config
        self.logger = logging.getLogger(__name__)

        # 初始化子模块
        self.fetcher = DataFetcher(config)
        self.processor = DataProcessor(config)

        # 缓存
        self._cache = {}
        self._cache_expiry = 1800  # 30分钟缓存

        self.logger.info("DataManager initialized")

    def get_stock_data(self, symbol: str, period: str = '1y',
                       interval: str = '1d', use_cache: bool = True,
                       force_refresh: bool = False) -> Optional[pd.DataFrame]:
        """
        获取股票数据（统一接口）

        Args:
            symbol: 股票代码
            period: 时间周期
            interval: 数据间隔
            use_cache: 是否使用缓存
            force_refresh: 强制刷新

        Returns:
            DataFrame: 股票数据（已清洗和转换）
        """
        self.logger.info(f"Getting stock data for {symbol}")

        try:
            # 检查缓存
            cache_key = f"{symbol}_{period}_{interval}"
            if use_cache and not force_refresh and cache_key in self._cache:
                cache_data, cache_time = self._cache[cache_key]
                age = (datetime.now() - cache_time).total_seconds()

                if age < self._cache_expiry:
                    self.logger.info(f"Using cached data for {symbol} (age: {age:.0f}s)")
                    return cache_data

            # 获取原始数据
            raw_data = self.fetcher.fetch_stock_data(symbol, period, interval)

            if raw_data is None or raw_data.empty:
                self.logger.error(f"No data retrieved for {symbol}")
                return None

            # 清洗数据
            clean_data = self.processor.clean_data(raw_data)

            if clean_data is None or clean_data.empty:
                self.logger.error(f"Data cleaning failed for {symbol}")
                return None

            # 转换数据
            transformed_data = self.processor.transform_data(clean_data, add_features=True)

            if transformed_data is None or transformed_data.empty:
                self.logger.error(f"Data transformation failed for {symbol}")
                return None

            # 保存到数据库
            self.processor.save_to_database(symbol, transformed_data)

            # 更新缓存
            self._cache[cache_key] = (transformed_data, datetime.now())

            self.logger.info(f"Successfully retrieved and processed {len(transformed_data)} records")
            return transformed_data

        except Exception as e:
            self.logger.error(f"Error getting stock data: {str(e)}")
            return None

    def get_historical_data(self, symbol: str, start_date: str,
                           end_date: Optional[str] = None) -> Optional[pd.DataFrame]:
        """
        获取历史数据（用于回测）

        Args:
            symbol: 股票代码
            start_date: 开始日期
            end_date: 结束日期

        Returns:
            DataFrame: 历史数据
        """
        self.logger.info(f"Getting historical data for {symbol}")

        try:
            # 尝试从数据库加载
            db_data = self.processor.load_from_database(
                symbol, start_date, end_date
            )

            if db_data is not None and not db_data.empty:
                # 检查数据完整性
                expected_days = self._calculate_expected_days(start_date, end_date)
                if len(db_data) >= expected_days * 0.8:  # 至少80%的数据
                    self.logger.info(f"Using database data for {symbol}")
                    return db_data

            # 数据库数据不足，从网络获取
            raw_data = self.fetcher.fetch_historical_data(
                symbol, start_date, end_date
            )

            if raw_data is None or raw_data.empty:
                return None

            # 处理数据
            clean_data = self.processor.clean_data(raw_data)
            transformed_data = self.processor.transform_data(clean_data)

            # 保存到数据库
            self.processor.save_to_database(symbol, transformed_data)

            return transformed_data

        except Exception as e:
            self.logger.error(f"Error getting historical data: {str(e)}")
            return None

    def get_multiple_stocks(self, symbols: List[str],
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
        self.logger.info(f"Getting data for {len(symbols)} stocks")

        results = {}

        for symbol in symbols:
            data = self.get_stock_data(symbol, period, interval)
            if data is not None:
                results[symbol] = data

        self.logger.info(f"Successfully retrieved data for {len(results)}/{len(symbols)} stocks")
        return results

    def get_stock_info(self, symbol: str) -> Optional[Dict]:
        """
        获取股票信息

        Args:
            symbol: 股票代码

        Returns:
            dict: 股票信息
        """
        self.logger.info(f"Getting stock info for {symbol}")

        try:
            # 从API获取
            info = self.fetcher.get_stock_info(symbol)

            if info is not None:
                return info

            return None

        except Exception as e:
            self.logger.error(f"Error getting stock info: {str(e)}")
            return None

    def get_data_summary(self, symbol: str) -> Optional[Dict]:
        """
        获取数据摘要

        Args:
            symbol: 股票代码

        Returns:
            dict: 数据摘要
        """
        self.logger.info(f"Getting data summary for {symbol}")

        try:
            # 获取数据
            data = self.get_stock_data(symbol, period='1y', interval='1d')

            if data is None or data.empty:
                return None

            # 计算统计信息
            stats = self.processor.get_data_statistics(data)

            # 添加额外信息
            summary = {
                'symbol': symbol,
                'data_quality': {
                    'completeness': self._calculate_completeness(data),
                    'freshness': self._calculate_freshness(data),
                    'consistency': self._calculate_consistency(data)
                },
                'statistics': stats
            }

            return summary

        except Exception as e:
            self.logger.error(f"Error getting data summary: {str(e)}")
            return None

    def _calculate_expected_days(self, start_date: str, end_date: Optional[str] = None) -> int:
        """计算预期的交易日数量"""
        try:
            start = datetime.strptime(start_date, '%Y-%m-%d')
            end = datetime.strptime(end_date, '%Y-%m-%d') if end_date else datetime.now()

            total_days = (end - start).days

            # 假设约70%是交易日（去除周末和节假日）
            trading_days = int(total_days * 0.7)

            return trading_days

        except Exception:
            return 0

    def _calculate_completeness(self, data: pd.DataFrame) -> float:
        """计算数据完整性"""
        try:
            total = len(data)
            non_null = data.count()

            if total == 0:
                return 0.0

            completeness = (non_null.sum() / (non_null.size * total)) * 100
            return round(completeness, 2)

        except Exception:
            return 0.0

    def _calculate_freshness(self, data: pd.DataFrame) -> Dict:
        """计算数据新鲜度"""
        try:
            last_date = data.index.max()
            days_old = (datetime.now() - last_date).days

            return {
                'last_date': last_date.strftime('%Y-%m-%d'),
                'days_old': days_old,
                'status': 'fresh' if days_old <= 2 else 'stale'
            }

        except Exception:
            return {'status': 'unknown'}

    def _calculate_consistency(self, data: pd.DataFrame) -> Dict:
        """计算数据一致性"""
        try:
            # 检查价格一致性
            price_consistent = (
                (data['High'] >= data['Low']).all() and
                (data['High'] >= data['Close']).all() and
                (data['Low'] <= data['Close']).all()
            )

            # 检查成交量一致性
            volume_positive = (data['Volume'] >= 0).all() if 'Volume' in data.columns else True

            return {
                'price_consistent': price_consistent,
                'volume_positive': volume_positive,
                'overall': price_consistent and volume_positive
            }

        except Exception:
            return {'status': 'unknown'}

    def refresh_cache(self, symbol: Optional[str] = None):
        """
        刷新缓存

        Args:
            symbol: 特定股票代码，None表示全部
        """
        self.logger.info(f"Refreshing cache for {symbol if symbol else 'all stocks'}")

        if symbol is None:
            self._cache.clear()
        else:
            # 清除特定股票的缓存
            keys_to_remove = [k for k in self._cache.keys() if k.startswith(symbol)]
            for key in keys_to_remove:
                del self._cache[key]

        self.logger.info("Cache refreshed")

    def export_data(self, symbol: str, format: str = 'excel',
                   filename: Optional[str] = None) -> Optional[str]:
        """
        导出数据

        Args:
            symbol: 股票代码
            format: 导出格式 ('excel', 'csv')
            filename: 输出文件名

        Returns:
            str: 文件路径
        """
        try:
            # 获取数据
            data = self.get_stock_data(symbol)

            if data is None or data.empty:
                return None

            if format == 'excel':
                return self.processor.export_to_excel(data, symbol, filename)
            elif format == 'csv':
                if filename is None:
                    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                    filename = f"./output/{symbol}_{timestamp}.csv"

                data.to_csv(filename)
                return filename
            else:
                self.logger.error(f"Unsupported format: {format}")
                return None

        except Exception as e:
            self.logger.error(f"Error exporting data: {str(e)}")
            return None

    def maintenance(self):
        """执行数据维护任务"""
        self.logger.info("Performing data maintenance")

        try:
            # 备份数据库
            self.processor.backup_database()

            # 清理旧数据（保留365天）
            deleted = self.processor.clean_old_data(days_to_keep=365)

            self.logger.info(f"Data maintenance completed. Deleted {deleted} old records")

        except Exception as e:
            self.logger.error(f"Error in maintenance: {str(e)}")

    def get_watchlist_data(self) -> Dict[str, pd.DataFrame]:
        """
        获取关注列表所有股票数据

        Returns:
            dict: {symbol: DataFrame}
        """
        watchlist = self.config.get('hk_stocks', {}).get('watchlist', [])
        period = self.config.get('hk_stocks', {}).get('default_period', '1y')
        interval = self.config.get('hk_stocks', {}).get('default_interval', '1d')

        return self.get_multiple_stocks(watchlist, period, interval)
