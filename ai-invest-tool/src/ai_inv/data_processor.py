"""
Data Processor Module - 数据处理模块
负责数据清洗、转换和存储

Author: WorkBuddy AI
Version: 1.0.0
"""

import pandas as pd
import numpy as np
import sqlite3
import logging
from datetime import datetime, timedelta
from typing import Optional, List, Dict
from pathlib import Path


class DataProcessor:
    """数据处理器"""

    def __init__(self, config):
        """
        初始化数据处理器

        Args:
            config: 配置字典
        """
        self.config = config
        self.logger = logging.getLogger(__name__)

        # 数据库配置
        db_config = config.get('database', {})
        self.db_path = db_config.get('path', './data/investment.db')
        self.backup_enabled = db_config.get('backup_enabled', True)

        # 创建数据目录
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)

        # 初始化数据库
        self._init_database()

        self.logger.info("DataProcessor initialized")

    def _init_database(self):
        """初始化数据库"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # 创建股票数据表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS stock_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    symbol TEXT NOT NULL,
                    date TEXT NOT NULL,
                    open REAL,
                    high REAL,
                    low REAL,
                    close REAL,
                    volume INTEGER,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(symbol, date)
                )
            ''')

            # 创建股票信息表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS stock_info (
                    symbol TEXT PRIMARY KEY,
                    name TEXT,
                    sector TEXT,
                    industry TEXT,
                    market_cap REAL,
                    pe_ratio REAL,
                    dividend_yield REAL,
                    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            # 创建分析结果表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS analysis_results (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    symbol TEXT NOT NULL,
                    analysis_type TEXT NOT NULL,
                    analysis_date TEXT NOT NULL,
                    result_data TEXT NOT NULL,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            # 创建索引
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_stock_symbol_date ON stock_data(symbol, date)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_analysis_symbol_date ON analysis_results(symbol, analysis_date)')

            conn.commit()
            conn.close()

            self.logger.info("Database initialized successfully")

        except Exception as e:
            self.logger.error(f"Error initializing database: {str(e)}")
            raise

    def clean_data(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        清洗数据

        Args:
            data: 原始数据DataFrame

        Returns:
            DataFrame: 清洗后的数据
        """
        self.logger.info("Cleaning data")

        try:
            # 创建副本
            df = data.copy()

            # 1. 处理缺失值
            # 前向填充，然后后向填充
            df = df.ffill().bfill()

            # 2. 移除完全空的行
            df = df.dropna(how='all')

            # 3. 处理异常值
            # 价格不能为负数或零
            price_columns = ['Open', 'High', 'Low', 'Close']
            for col in price_columns:
                if col in df.columns:
                    df = df[df[col] > 0]

            # 4. 检查High/Low关系
            # High应该 >= Low
            df = df[df['High'] >= df['Low']]

            # 5. 检查Close在High和Low之间
            df = df[
                (df['Close'] <= df['High']) &
                (df['Close'] >= df['Low'])
            ]

            # 6. 移除成交量异常值
            if 'Volume' in df.columns:
                # 成交量不能为负数
                df = df[df['Volume'] >= 0]

                # 处理极端值（超过3个标准差）
                vol_mean = df['Volume'].mean()
                vol_std = df['Volume'].std()
                upper_bound = vol_mean + 3 * vol_std
                df.loc[df['Volume'] > upper_bound, 'Volume'] = upper_bound

            # 7. 排序数据（按日期升序）
            df.sort_index(inplace=True)

            # 8. 移除重复日期
            df = df[~df.index.duplicated(keep='last')]

            self.logger.info(f"Data cleaned: {len(data)} -> {len(df)} records")

            return df

        except Exception as e:
            self.logger.error(f"Error cleaning data: {str(e)}")
            return data

    def transform_data(self, data: pd.DataFrame,
                     add_features: bool = True) -> pd.DataFrame:
        """
        转换数据，添加技术特征

        Args:
            data: 原始数据
            add_features: 是否添加技术特征

        Returns:
            DataFrame: 转换后的数据
        """
        self.logger.info("Transforming data")

        try:
            df = data.copy()

            # 1. 添加基本收益率
            df['returns'] = df['Close'].pct_change()

            # 2. 添加对数收益率
            df['log_returns'] = np.log(df['Close'] / df['Close'].shift(1))

            # 3. 添加波动率
            df['volatility'] = df['returns'].rolling(window=20).std()

            # 4. 添加成交量变化
            if 'Volume' in df.columns:
                df['volume_change'] = df['Volume'].pct_change()

            # 5. 添加涨跌标记
            df['direction'] = np.where(df['returns'] > 0, 1,
                                   np.where(df['returns'] < 0, -1, 0))

            # 6. 添加技术特征（可选）
            if add_features:
                df = self._add_technical_features(df)

            # 7. 添加时间特征
            df['day_of_week'] = df.index.dayofweek
            df['day_of_month'] = df.index.day
            df['month'] = df.index.month
            df['quarter'] = df.index.quarter

            self.logger.info(f"Data transformed: {len(df.columns)} columns")

            return df

        except Exception as e:
            self.logger.error(f"Error transforming data: {str(e)}")
            return data

    def _add_technical_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """添加技术分析特征"""
        try:
            # 简单移动平均
            for period in [5, 10, 20, 50, 200]:
                df[f'SMA_{period}'] = df['Close'].rolling(window=period).mean()

            # 指数移动平均
            for period in [12, 26]:
                df[f'EMA_{period}'] = df['Close'].ewm(span=period).mean()

            # 价格变化
            df['price_change_1d'] = df['Close'] - df['Close'].shift(1)
            df['price_change_5d'] = df['Close'] - df['Close'].shift(5)

            # 高低点
            df['high_20d'] = df['High'].rolling(window=20).max()
            df['low_20d'] = df['Low'].rolling(window=20).min()

            return df

        except Exception as e:
            self.logger.error(f"Error adding technical features: {str(e)}")
            return df

    def normalize_data(self, data: pd.DataFrame,
                     method: str = 'minmax') -> pd.DataFrame:
        """
        归一化数据

        Args:
            data: 原始数据
            method: 归一化方法 ('minmax', 'zscore')

        Returns:
            DataFrame: 归一化后的数据
        """
        self.logger.info(f"Normalizing data using {method} method")

        try:
            df = data.copy()

            # 选择数值列
            numeric_columns = df.select_dtypes(include=[np.number]).columns

            if method == 'minmax':
                # Min-Max归一化
                for col in numeric_columns:
                    min_val = df[col].min()
                    max_val = df[col].max()
                    if max_val != min_val:
                        df[f'{col}_normalized'] = (df[col] - min_val) / (max_val - min_val)

            elif method == 'zscore':
                # Z-score标准化
                for col in numeric_columns:
                    mean_val = df[col].mean()
                    std_val = df[col].std()
                    if std_val != 0:
                        df[f'{col}_zscore'] = (df[col] - mean_val) / std_val

            return df

        except Exception as e:
            self.logger.error(f"Error normalizing data: {str(e)}")
            return data

    def save_to_database(self, symbol: str, data: pd.DataFrame) -> bool:
        """
        保存数据到数据库

        Args:
            symbol: 股票代码
            data: 股票数据

        Returns:
            bool: 是否成功
        """
        self.logger.info(f"Saving {symbol} data to database")

        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # 准备数据
            records = []
            for date, row in data.iterrows():
                records.append((
                    symbol,
                    date.strftime('%Y-%m-%d'),
                    float(row['Open']) if pd.notna(row['Open']) else None,
                    float(row['High']) if pd.notna(row['High']) else None,
                    float(row['Low']) if pd.notna(row['Low']) else None,
                    float(row['Close']) if pd.notna(row['Close']) else None,
                    int(row['Volume']) if pd.notna(row['Volume']) else None
                ))

            # 批量插入
            cursor.executemany('''
                INSERT OR REPLACE INTO stock_data
                (symbol, date, open, high, low, close, volume)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', records)

            conn.commit()
            conn.close()

            self.logger.info(f"Saved {len(records)} records for {symbol}")
            return True

        except Exception as e:
            self.logger.error(f"Error saving to database: {str(e)}")
            return False

    def load_from_database(self, symbol: str,
                          start_date: Optional[str] = None,
                          end_date: Optional[str] = None) -> Optional[pd.DataFrame]:
        """
        从数据库加载数据

        Args:
            symbol: 股票代码
            start_date: 开始日期 (YYYY-MM-DD)
            end_date: 结束日期 (YYYY-MM-DD)

        Returns:
            DataFrame: 股票数据
        """
        self.logger.info(f"Loading {symbol} data from database")

        try:
            conn = sqlite3.connect(self.db_path)

            # 构建SQL查询
            sql = "SELECT date, open, high, low, close, volume FROM stock_data WHERE symbol = ?"
            params = [symbol]

            if start_date:
                sql += " AND date >= ?"
                params.append(start_date)

            if end_date:
                sql += " AND date <= ?"
                params.append(end_date)

            sql += " ORDER BY date ASC"

            # 执行查询
            df = pd.read_sql_query(sql, conn, params=params)

            conn.close()

            if df.empty:
                self.logger.warning(f"No data found for {symbol}")
                return None

            # 转换日期列
            df['date'] = pd.to_datetime(df['date'])
            df.set_index('date', inplace=True)

            # 重命名列
            df.columns = ['Open', 'High', 'Low', 'Close', 'Volume']

            self.logger.info(f"Loaded {len(df)} records for {symbol}")
            return df

        except Exception as e:
            self.logger.error(f"Error loading from database: {str(e)}")
            return None

    def save_analysis_result(self, symbol: str, analysis_type: str,
                          result_data: Dict) -> bool:
        """
        保存分析结果到数据库

        Args:
            symbol: 股票代码
            analysis_type: 分析类型
            result_data: 分析结果

        Returns:
            bool: 是否成功
        """
        try:
            import json

            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # 插入分析结果
            cursor.execute('''
                INSERT INTO analysis_results
                (symbol, analysis_type, analysis_date, result_data)
                VALUES (?, ?, ?, ?)
            ''', (
                symbol,
                analysis_type,
                datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                json.dumps(result_data, ensure_ascii=False)
            ))

            conn.commit()
            conn.close()

            return True

        except Exception as e:
            self.logger.error(f"Error saving analysis result: {str(e)}")
            return False

    def export_to_excel(self, data: pd.DataFrame, symbol: str,
                       filename: Optional[str] = None) -> str:
        """
        导出数据到Excel

        Args:
            data: 股票数据
            symbol: 股票代码
            filename: 输出文件名

        Returns:
            str: 文件路径
        """
        try:
            # 生成文件名
            if filename is None:
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = f"./output/{symbol}_{timestamp}.xlsx"

            # 创建输出目录
            Path(filename).parent.mkdir(parents=True, exist_ok=True)

            # 导出到Excel
            data.to_excel(filename, engine='openpyxl')

            self.logger.info(f"Data exported to {filename}")
            return filename

        except Exception as e:
            self.logger.error(f"Error exporting to Excel: {str(e)}")
            return ""

    def get_data_statistics(self, data: pd.DataFrame) -> Dict:
        """
        获取数据统计信息

        Args:
            data: 股票数据

        Returns:
            dict: 统计信息
        """
        try:
            stats = {
                'total_records': len(data),
                'date_range': {
                    'start': data.index.min().strftime('%Y-%m-%d'),
                    'end': data.index.max().strftime('%Y-%m-%d')
                },
                'price_stats': {
                    'mean': data['Close'].mean(),
                    'median': data['Close'].median(),
                    'std': data['Close'].std(),
                    'min': data['Close'].min(),
                    'max': data['Close'].max()
                },
                'volume_stats': {
                    'mean': data['Volume'].mean(),
                    'median': data['Volume'].median(),
                    'std': data['Volume'].std(),
                    'min': data['Volume'].min(),
                    'max': data['Volume'].max()
                } if 'Volume' in data.columns else {},
                'returns_stats': {
                    'mean': data['returns'].mean(),
                    'std': data['returns'].std(),
                    'skewness': data['returns'].skew(),
                    'kurtosis': data['returns'].kurtosis()
                } if 'returns' in data.columns else {}
            }

            return stats

        except Exception as e:
            self.logger.error(f"Error calculating statistics: {str(e)}")
            return {}

    def backup_database(self) -> bool:
        """
        备份数据库

        Returns:
            bool: 是否成功
        """
        if not self.backup_enabled:
            return False

        try:
            # 生成备份文件名
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_path = f"{self.db_path}.bak_{timestamp}"

            # 复制文件
            import shutil
            shutil.copy2(self.db_path, backup_path)

            self.logger.info(f"Database backed up to {backup_path}")
            return True

        except Exception as e:
            self.logger.error(f"Error backing up database: {str(e)}")
            return False

    def clean_old_data(self, days_to_keep: int = 365) -> int:
        """
        清理旧数据

        Args:
            days_to_keep: 保留天数

        Returns:
            int: 删除的记录数
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # 计算截止日期
            cutoff_date = datetime.now() - timedelta(days=days_to_keep)
            cutoff_str = cutoff_date.strftime('%Y-%m-%d')

            # 删除旧数据
            cursor.execute('DELETE FROM stock_data WHERE date < ?', (cutoff_str,))
            deleted_count = cursor.rowcount

            conn.commit()
            conn.close()

            self.logger.info(f"Deleted {deleted_count} old records")
            return deleted_count

        except Exception as e:
            self.logger.error(f"Error cleaning old data: {str(e)}")
            return 0
