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

    def __init__(self, config: Optional[Dict] = None):
        """
        初始化数据处理器

        Args:
            config: 配置字典
        """
        self.config = config or {}
        self.logger = logging.getLogger(__name__)

        # 数据库配置
        self.db_path = self.config.get('database', {}).get('path', 'data/stocks.db')
        self.db_enabled = self.config.get('database', {}).get('enabled', True)

        # 创建数据目录
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)

        # 初始化数据库
        self._init_database()

    def _init_database(self):
        """初始化数据库表"""
        if not self.db_enabled:
            return

        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # 创建股票数据表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS stock_data (
                    symbol TEXT,
                    date TEXT,
                    open REAL,
                    high REAL,
                    low REAL,
                    close REAL,
                    volume INTEGER,
                    PRIMARY KEY (symbol, date)
                )
            ''')

            # 创建分析结果表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS analysis_results (
                    symbol TEXT,
                    date TEXT,
                    indicator TEXT,
                    value REAL,
                    PRIMARY KEY (symbol, date, indicator)
                )
            ''')

            conn.commit()
            conn.close()
            self.logger.info(f"Database initialized at {self.db_path}")

        except Exception as e:
            self.logger.error(f"Database initialization failed: {e}")

    def save_stock_data(self, symbol: str, data: pd.DataFrame) -> bool:
        """
        保存股票数据到数据库

        Args:
            symbol: 股票代码
            data: 数据框

        Returns:
            是否成功
        """
        if not self.db_enabled or data.empty:
            return False

        try:
            conn = sqlite3.connect(self.db_path)
            
            # 准备数据
            df_to_save = data.copy()
            df_to_save['symbol'] = symbol
            if 'Date' in df_to_save.columns:
                df_to_save['date'] = df_to_save['Date'].dt.strftime('%Y-%m-%d')
            else:
                df_to_save['date'] = df_to_save.index.strftime('%Y-%m-%d')

            # 仅保留需要的列
            cols = ['symbol', 'date', 'Open', 'High', 'Low', 'Close', 'Volume']
            df_to_save = df_to_save[[c for c in cols if c in df_to_save.columns]]
            df_to_save.columns = [c.lower() for c in df_to_save.columns]

            # 保存
            df_to_save.to_sql('stock_data', conn, if_exists='append', index=False, 
                             method='multi', chunksize=500)
            
            conn.close()
            return True

        except Exception as e:
            self.logger.error(f"Failed to save stock data: {e}")
            return False

    def get_cached_data(self, symbol: str, start_date: str, end_date: str) -> Optional[pd.DataFrame]:
        """
        从数据库获取缓存的数据

        Args:
            symbol: 股票代码
            start_date: 开始日期
            end_date: 结束日期

        Returns:
            数据框或None
        """
        if not self.db_enabled:
            return None

        try:
            conn = sqlite3.connect(self.db_path)
            query = f"""
                SELECT * FROM stock_data 
                WHERE symbol = '{symbol}' 
                AND date BETWEEN '{start_date}' AND '{end_date}'
                ORDER BY date ASC
            """
            df = pd.read_sql_query(query, conn)
            conn.close()

            if df.empty:
                return None

            # 恢复列名和索引
            df['date'] = pd.to_datetime(df['date'])
            df.set_index('date', inplace=True)
            df.columns = [c.capitalize() for c in df.columns]
            
            return df

        except Exception as e:
            self.logger.error(f"Failed to get cached data: {e}")
            return None

    def clean_data(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        清洗数据

        Args:
            data: 原始数据

        Returns:
            清洗后的数据
        """
        if data.empty:
            return data

        # 处理缺失值
        df = data.copy()
        df = df.ffill().bfill()

        # 移除重复项
        df = df[~df.index.duplicated(keep='first')]

        return df
