"""
回测引擎模块测试
测试回测引擎和各种策略功能
"""

import unittest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.ai_inv.backtester import (
    BacktestEngine,
    MAStrategy,
    RSIStrategy,
    MACDStrategy,
    CombinedStrategy,
    BacktestReport
)
from src.ai_inv.portfolio_optimizer import (
    PortfolioOptimizer,
    RiskManager,
    PerformanceAnalyzer
)


def generate_test_data(days: int = 252) -> pd.DataFrame:
    """生成测试数据"""
    np.random.seed(42)
    
    dates = pd.date_range(start='2023-01-01', periods=days, freq='D')
    
    # 生成随机游走价格
    price = 100.0
    prices = [price]
    
    for _ in range(days - 1):
        change = np.random.normal(0, 0.02)
        price = price * (1 + change)
        prices.append(price)
    
    prices = np.array(prices)
    
    # 创建OHLCV数据
    data = pd.DataFrame({
        'Open': prices * np.random.uniform(0.98, 1.02, days),
        'High': prices * np.random.uniform(1.0, 1.05, days),
        'Low': prices * np.random.uniform(0.95, 1.0, days),
        'Close': prices,
        'Volume': np.random.randint(100000, 1000000, days)
    })
    
    data.index = dates
    
    return data


class TestBacktestEngine(unittest.TestCase):
    """测试回测引擎"""
    
    def setUp(self):
        """设置测试环境"""
        self.engine = BacktestEngine(
            initial_capital=100000,
            commission=0.001,
            slippage=0.0005
        )
        self.data = generate_test_data(days=252)
    
    def test_init(self):
        """测试初始化"""
        self.assertEqual(self.engine.initial_capital, 100000)
        self.assertEqual(self.engine.commission, 0.001)
        self.assertEqual(self.engine.slippage, 0.0005)
    
    def test_reset(self):
        """测试重置"""
        # 先运行一次回测
        strategy = MAStrategy(5, 20)
        self.engine.run_backtest(self.data, strategy)
        
        # 重置
        self.engine.reset()
        
        self.assertEqual(self.engine.current_capital, 100000)
        self.assertEqual(self.engine.cash, 100000)
        self.assertEqual(len(self.engine.trades), 0)
        
        print("✓ 回测引擎重置测试通过")
    
    def test_run_backtest(self):
        """测试运行回测"""
        strategy = MAStrategy(5, 20)
        results = self.engine.run_backtest(self.data, strategy)
        
        # 验证结果结构
        self.assertIn('summary', results)
        self.assertIn('trades', results)
        self.assertIn('equity_curve', results)
        self.assertIn('trades_history', results)
        
        # 验证摘要内容
        summary = results['summary']
        self.assertIn('initial_capital', summary)
        self.assertIn('final_capital', summary)
        self.assertIn('total_return', summary)
        self.assertIn('annual_return', summary)
        self.assertIn('max_drawdown', summary)
        self.assertIn('sharpe_ratio', summary)
        
        print("✓ 运行回测测试通过")
    
    def test_performance_metrics(self):
        """测试性能指标计算"""
        strategy = MAStrategy(5, 20)
        results = self.engine.run_backtest(self.data, strategy)
        
        summary = results['summary']
        
        # 检查指标数值范围
        self.assertGreaterEqual(summary['sharpe_ratio'], -10.0)
        self.assertLessEqual(summary['sharpe_ratio'], 10.0)
        self.assertGreaterEqual(summary['max_drawdown'], 0)
        
        print("✓ 性能指标计算测试通过")


class TestMAStrategy(unittest.TestCase):
    """测试移动平均策略"""
    
    def setUp(self):
        """设置测试环境"""
        self.data = generate_test_data(days=100)
        self.strategy = MAStrategy(short_period=5, long_period=20)
    
    def test_init(self):
        """测试初始化"""
        self.assertEqual(self.strategy.short_period, 5)
        self.assertEqual(self.strategy.long_period, 20)
        self.assertEqual(self.strategy.name, "MA(5,20)")
    
    def test_generate_signal(self):
        """测试信号生成"""
        # 计算技术指标
        from src.ai_inv.indicators import TechnicalIndicators
        ti = TechnicalIndicators()
        data = ti.calculate_all_indicators(self.data)
        
        # 生成信号
        signal = self.strategy.generate_signal(data)
        
        # 验证信号结构
        self.assertIn('action', signal)
        self.assertIn(signal['action'], ['buy', 'sell', 'hold'])
        
        print("✓ MA策略信号生成测试通过")


class TestRSIStrategy(unittest.TestCase):
    """测试RSI策略"""
    
    def setUp(self):
        """设置测试环境"""
        self.data = generate_test_data(days=100)
        self.strategy = RSIStrategy(period=14, oversold=30, overbought=70)
    
    def test_init(self):
        """测试初始化"""
        self.assertEqual(self.strategy.period, 14)
        self.assertEqual(self.strategy.oversold, 30)
        self.assertEqual(self.strategy.overbought, 70)
    
    def test_generate_signal(self):
        """测试信号生成"""
        from src.ai_inv.indicators import TechnicalIndicators
        ti = TechnicalIndicators()
        data = ti.calculate_all_indicators(self.data)
        
        signal = self.strategy.generate_signal(data)
        
        self.assertIn('action', signal)
        self.assertIn(signal['action'], ['buy', 'sell', 'hold'])
        
        print("✓ RSI策略信号生成测试通过")


class TestMACDStrategy(unittest.TestCase):
    """测试MACD策略"""
    
    def setUp(self):
        """设置测试环境"""
        self.data = generate_test_data(days=100)
        self.strategy = MACDStrategy(fast_period=12, slow_period=26, signal_period=9)
    
    def test_init(self):
        """测试初始化"""
        self.assertEqual(self.strategy.fast_period, 12)
        self.assertEqual(self.strategy.slow_period, 26)
        self.assertEqual(self.strategy.signal_period, 9)
    
    def test_generate_signal(self):
        """测试信号生成"""
        from src.ai_inv.indicators import TechnicalIndicators
        ti = TechnicalIndicators()
        data = ti.calculate_all_indicators(self.data)
        
        signal = self.strategy.generate_signal(data)
        
        self.assertIn('action', signal)
        self.assertIn(signal['action'], ['buy', 'sell', 'hold'])
        
        print("✓ MACD策略信号生成测试通过")


class TestCombinedStrategy(unittest.TestCase):
    """测试组合策略"""
    
    def setUp(self):
        """设置测试环境"""
        self.data = generate_test_data(days=100)
        
        strategies = [
            MAStrategy(5, 20),
            RSIStrategy(14, 30, 70),
            MACDStrategy(12, 26, 9)
        ]
        
        self.strategy = CombinedStrategy(strategies)
    
    def test_init(self):
        """测试初始化"""
        self.assertEqual(len(self.strategy.strategies), 3)
        self.assertEqual(len(self.strategy.weights), 3)
    
    def test_generate_signal(self):
        """测试信号生成"""
        from src.ai_inv.indicators import TechnicalIndicators
        ti = TechnicalIndicators()
        data = ti.calculate_all_indicators(self.data)
        
        signal = self.strategy.generate_signal(data)
        
        self.assertIn('action', signal)
        self.assertIn(signal['action'], ['buy', 'sell', 'hold'])
        
        print("✓ 组合策略信号生成测试通过")


class TestBacktestReport(unittest.TestCase):
    """测试回测报告"""
    
    def test_generate_report(self):
        """测试生成报告"""
        # 创建模拟结果
        results = {
            'summary': {
                'initial_capital': 100000,
                'final_capital': 120000,
                'total_return': 20.0,
                'annual_return': 15.0,
                'volatility': 10.0,
                'max_drawdown': -5.0,
                'sharpe_ratio': 1.5,
                'sortino_ratio': 2.0
            },
            'trades': {
                'total_trades': 50,
                'winning_trades': 30,
                'win_rate': 60.0
            }
        }
        
        # 生成报告
        report = BacktestReport.generate_report(results, "Test Strategy")
        
        # 验证报告内容
        self.assertIsInstance(report, str)
        self.assertIn('回测报告', report)
        self.assertIn('Test Strategy', report)
        self.assertIn('20.0%', report)
        
        print("✓ 生成回测报告测试通过")
    
    def test_export_results(self):
        """测试导出结果"""
        # 创建模拟结果
        equity_df = pd.DataFrame({
            'portfolio_value': [100000, 105000, 110000],
            'cash': [100000, 95000, 90000],
            'holdings_value': [0, 10000, 20000]
        })
        
        trades_df = pd.DataFrame({
            'action': ['buy', 'buy'],
            'symbol': ['TEST', 'TEST'],
            'quantity': [100, 100]
        })
        
        results = {
            'equity_curve': equity_df,
            'trades_history': trades_df
        }
        
        # 测试CSV导出
        BacktestReport.export_results(
            results,
            'test_results.csv',
            format='csv'
        )
        
        # 验证文件创建
        self.assertTrue(os.path.exists('test_results_equity.csv'))
        self.assertTrue(os.path.exists('test_results_trades.csv'))
        
        # 清理文件
        os.remove('test_results_equity.csv')
        os.remove('test_results_trades.csv')
        
        print("✓ 导出结果测试通过")


class TestPortfolioOptimizer(unittest.TestCase):
    """测试投资组合优化"""
    
    def setUp(self):
        """设置测试环境"""
        np.random.seed(42)
        symbols = ['A', 'B', 'C']
        returns_data = {}
        
        for symbol in symbols:
            returns_data[symbol] = np.random.normal(0.001, 0.02, 100)
        
        self.returns_df = pd.DataFrame(returns_data)
        self.optimizer = PortfolioOptimizer(risk_free_rate=0.02)
    
    def test_optimize_equal_weight(self):
        """测试等权重优化"""
        result = self.optimizer.optimize_portfolio(
            self.returns_df,
            method='equal_weight'
        )
        
        # 验证结果结构
        self.assertIn('weights', result)
        self.assertIn('expected_return', result)
        self.assertIn('volatility', result)
        self.assertIn('sharpe_ratio', result)
        
        # 验证权重和为1
        total_weight = sum(result['weights'].values())
        self.assertAlmostEqual(total_weight, 1.0, places=2)
        
        print("✓ 等权重优化测试通过")
    
    def test_optimize_sharpe(self):
        """测试夏普比率优化"""
        result = self.optimizer.optimize_portfolio(
            self.returns_df,
            method='sharpe'
        )
        
        self.assertIn('sharpe_ratio', result)
        self.assertIsInstance(result['sharpe_ratio'], float)
        
        print("✓ 夏普比率优化测试通过")
    
    def test_optimize_min_variance(self):
        """测试最小方差优化"""
        result = self.optimizer.optimize_portfolio(
            self.returns_df,
            method='min_variance'
        )
        
        self.assertIn('volatility', result)
        self.assertIsInstance(result['volatility'], float)
        
        print("✓ 最小方差优化测试通过")


class TestRiskManager(unittest.TestCase):
    """测试风险管理"""
    
    def setUp(self):
        """设置测试环境"""
        self.risk_manager = RiskManager(
            max_position_size=0.2,
            max_portfolio_risk=0.25
        )
    
    def test_calculate_position_size(self):
        """测试仓位计算"""
        position_size = self.risk_manager.calculate_position_size(
            capital=100000,
            risk_per_trade=0.02,
            stop_loss_pct=0.05
        )
        
        # 验证结果
        self.assertIsInstance(position_size, float)
        self.assertGreater(position_size, 0)
        self.assertLessEqual(position_size, 100000 * 0.2)
        
        print("✓ 仓位计算测试通过")
    
    def test_check_risk(self):
        """测试风险检查"""
        risk_check = self.risk_manager.check_risk(
            portfolio_value=100000,
            positions={'TEST': 10000},
            current_prices={'TEST': 1.0}
        )
        
        # 验证结果结构
        self.assertIn('has_warnings', risk_check)
        self.assertIn('warnings', risk_check)
        self.assertIn('risk_level', risk_check)
        
        self.assertIn(risk_check['risk_level'], ['low', 'medium', 'high'])
        
        print("✓ 风险检查测试通过")
    
    def test_generate_stop_loss(self):
        """测试止损生成"""
        # 固定止损
        stop_loss = self.risk_manager.generate_stop_loss(
            entry_price=100.0,
            method='fixed',
            params={'loss_pct': 0.05}
        )
        
        self.assertAlmostEqual(stop_loss, 95.0, places=2)
        
        # ATR止损
        stop_loss = self.risk_manager.generate_stop_loss(
            entry_price=100.0,
            method='atr',
            params={'atr': 2.0, 'atr_multiplier': 2.0}
        )
        
        self.assertAlmostEqual(stop_loss, 96.0, places=2)
        
        print("✓ 止损生成测试通过")


class TestPerformanceAnalyzer(unittest.TestCase):
    """测试性能分析"""
    
    def setUp(self):
        """设置测试环境"""
        np.random.seed(42)
        dates = pd.date_range(start='2023-01-01', periods=100, freq='D')
        portfolio_value = 100000 * (1 + np.cumsum(np.random.normal(0.001, 0.01, 100)))
        
        self.equity_curve = pd.DataFrame({
            'portfolio_value': portfolio_value
        }, index=dates)
        
        self.analyzer = PerformanceAnalyzer()
    
    def test_analyze_performance(self):
        """测试性能分析"""
        results = self.analyzer.analyze_performance(self.equity_curve)
        
        # 验证结果结构
        self.assertIn('return_metrics', results)
        self.assertIn('risk_metrics', results)
        self.assertIn('distribution_metrics', results)
        
        # 验证收益指标
        return_metrics = results['return_metrics']
        self.assertIn('total_return', return_metrics)
        self.assertIn('annual_return', return_metrics)
        self.assertIn('volatility', return_metrics)
        
        # 验证风险指标
        risk_metrics = results['risk_metrics']
        self.assertIn('max_drawdown', risk_metrics)
        self.assertIn('sharpe_ratio', risk_metrics)
        self.assertIn('sortino_ratio', risk_metrics)
        
        print("✓ 性能分析测试通过")


def run_tests():
    """运行所有测试"""
    print("\n" + "="*60)
    print("回测引擎模块测试")
    print("="*60 + "\n")
    
    # 创建测试套件
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # 添加测试
    suite.addTests(loader.loadTestsFromTestCase(TestBacktestEngine))
    suite.addTests(loader.loadTestsFromTestCase(TestMAStrategy))
    suite.addTests(loader.loadTestsFromTestCase(TestRSIStrategy))
    suite.addTests(loader.loadTestsFromTestCase(TestMACDStrategy))
    suite.addTests(loader.loadTestsFromTestCase(TestCombinedStrategy))
    suite.addTests(loader.loadTestsFromTestCase(TestBacktestReport))
    suite.addTests(loader.loadTestsFromTestCase(TestPortfolioOptimizer))
    suite.addTests(loader.loadTestsFromTestCase(TestRiskManager))
    suite.addTests(loader.loadTestsFromTestCase(TestPerformanceAnalyzer))
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # 输出结果
    print("\n" + "="*60)
    print(f"测试完成: 运行 {result.testsRun} 个测试")
    print(f"成功: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"失败: {len(result.failures)}")
    print(f"错误: {len(result.errors)}")
    print("="*60 + "\n")
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
