"""
可视化模块测试
"""

import unittest
import pandas as pd
import numpy as np
from datetime import datetime
import os
import sys

# 添加src到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.ai_inv.excel_visualizer import ExcelVisualizer


class TestExcelVisualizer(unittest.TestCase):
    """Excel可视化器测试"""
    
    def setUp(self):
        """测试前准备"""
        self.visualizer = ExcelVisualizer(output_dir='output/test_excel')
        
        # 创建测试数据
        dates = pd.date_range(start='2024-01-01', periods=100, freq='D')
        self.test_data = pd.DataFrame({
            'Open': np.random.uniform(27000, 28000, 100),
            'High': np.random.uniform(28000, 29000, 100),
            'Low': np.random.uniform(26000, 27000, 100),
            'Close': np.random.uniform(27000, 28000, 100),
            'Volume': np.random.uniform(1000000, 2000000, 100)
        }, index=dates)
        
        # 创建测试指标
        self.test_indicators = {
            'SMA': {
                'SMA_5': pd.Series(np.random.uniform(27000, 28000, 100), index=dates),
                'SMA_20': pd.Series(np.random.uniform(27000, 28000, 100), index=dates)
            },
            'RSI': pd.Series(np.random.uniform(30, 70, 100), index=dates),
            'MACD': {
                'macd': pd.Series(np.random.uniform(-50, 50, 100), index=dates),
                'signal': pd.Series(np.random.uniform(-50, 50, 100), index=dates),
                'histogram': pd.Series(np.random.uniform(-20, 20, 100), index=dates)
            },
            'Bollinger_Bands': {
                'upper': pd.Series(np.random.uniform(28000, 29000, 100), index=dates),
                'middle': pd.Series(np.random.uniform(27000, 28000, 100), index=dates),
                'lower': pd.Series(np.random.uniform(26000, 27000, 100), index=dates)
            }
        }
    
    def test_init(self):
        """测试初始化"""
        self.assertIsNotNone(self.visualizer)
        self.assertEqual(self.visualizer.output_dir, 'output/test_excel')
    
    def test_generate_stock_report(self):
        """测试生成股票报告"""
        # 生成报告
        filepath = self.visualizer.generate_stock_report(
            symbol='TEST',
            price_data=self.test_data,
            indicators=self.test_indicators
        )
        
        # 检查文件是否创建
        self.assertTrue(os.path.exists(filepath))
        self.assertTrue(filepath.endswith('.xlsx'))
    
    def test_generate_stock_report_with_ai(self):
        """测试生成包含AI分析的报告"""
        # 创建AI分析数据
        ai_analysis = {
            'recommendation': {
                'action': 'BUY',
                'confidence': 0.8,
                'risk_level': 'medium'
            },
            'sentiment': {
                'overall': 'positive',
                'score': 0.6
            }
        }
        
        # 生成报告
        filepath = self.visualizer.generate_stock_report(
            symbol='TEST',
            price_data=self.test_data,
            indicators=self.test_indicators,
            ai_analysis=ai_analysis
        )
        
        # 检查文件是否创建
        self.assertTrue(os.path.exists(filepath))
    
    def test_generate_backtest_report(self):
        """测试生成回测报告"""
        # 创建回测结果
        backtest_results = {
            'summary': {
                'initial_capital': 100000,
                'final_capital': 115000,
                'total_return': 15.0,
                'annual_return': 12.5,
                'total_trades': 20,
                'winning_trades': 12,
                'losing_trades': 8,
                'win_rate': 60.0,
                'max_drawdown': -8.5,
                'sharpe_ratio': 1.5,
                'sortino_ratio': 2.0,
                'calmar_ratio': 1.8,
                'start_date': '2024-01-01',
                'end_date': '2024-12-31',
                'volatility': 15.0,
                'max_drawdown_duration': 10,
                'avg_win': 2000,
                'avg_loss': -1000,
                'profit_factor': 2.4
            },
            'trades': pd.DataFrame({
                'entry_date': pd.date_range('2024-01-01', periods=20, freq='5D'),
                'exit_date': pd.date_range('2024-01-06', periods=20, freq='5D'),
                'entry_price': np.random.uniform(27000, 28000, 20),
                'exit_price': np.random.uniform(27000, 28000, 20),
                'shares': np.random.randint(10, 100, 20),
                'pnl': np.random.uniform(-1000, 2000, 20),
                'pnl_pct': np.random.uniform(-5, 10, 20)
            }),
            'equity_curve': pd.DataFrame({
                'date': pd.date_range('2024-01-01', periods=100, freq='D'),
                'equity': np.cumsum(np.random.normal(100, 500, 100)) + 100000
            }).set_index('date')
        }
        
        # 生成报告
        filepath = self.visualizer.generate_backtest_report(
            results=backtest_results,
            strategy_name='TestStrategy'
        )
        
        # 检查文件是否创建
        self.assertTrue(os.path.exists(filepath))
    
    def test_generate_portfolio_report(self):
        """测试生成投资组合报告"""
        # 创建投资组合数据
        portfolio_data = {
            'total_value': 1000000,
            'total_pnl': 50000,
            'total_return': 5.0,
            'num_holdings': 3,
            'date': datetime.now().strftime('%Y-%m-%d'),
            'holdings': pd.DataFrame({
                'symbol': ['6158.HK', '7200.HK', '^HSI'],
                'shares': [10000, 5000, 100],
                'avg_price': [0.50, 10.00, 28000.0],
                'current_price': [0.52, 10.50, 28500.0],
                'market_value': [5200, 52500, 2850000],
                'cost_basis': [5000, 50000, 2800000],
                'pnl': [200, 2500, 50000],
                'pnl_pct': [4.0, 5.0, 1.79]
            }),
            'returns': pd.DataFrame({
                'date': pd.date_range('2024-01-01', periods=30, freq='D'),
                'return': np.random.normal(0.001, 0.02, 30)
            }),
            'risk_analysis': {
                'volatility': 15.5,
                'beta': 1.2,
                'sharpe': 1.8,
                'max_drawdown': -8.5,
                'var_95': -5000.0
            }
        }
        
        # 生成报告
        filepath = self.visualizer.generate_portfolio_report(
            portfolio_data=portfolio_data
        )
        
        # 检查文件是否创建
        self.assertTrue(os.path.exists(filepath))


class TestWebDashboard(unittest.TestCase):
    """Web仪表板测试"""
    
    def test_imports(self):
        """测试导入"""
        try:
            from src.ai_inv import web_dashboard
            self.assertTrue(True)
        except ImportError as e:
            self.skipTest(f"Web dashboard导入失败: {e}")
    
    def test_plot_functions_exist(self):
        """测试绘图函数是否存在"""
        try:
            from src.ai_inv.web_dashboard import (
                plot_price_chart,
                plot_rsi_chart,
                plot_macd_chart
            )
            self.assertTrue(callable(plot_price_chart))
            self.assertTrue(callable(plot_rsi_chart))
            self.assertTrue(callable(plot_macd_chart))
        except ImportError as e:
            self.skipTest(f"导入失败: {e}")


if __name__ == '__main__':
    unittest.main()
