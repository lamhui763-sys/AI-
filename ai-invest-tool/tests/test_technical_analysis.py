"""
技术分析模块测试
测试各种技术指标的计算和功能
"""

import unittest
import pandas as pd
import numpy as np
import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.ai_inv.indicators import TechnicalIndicators


class TestTechnicalIndicators(unittest.TestCase):
    """测试技术指标计算"""
    
    def setUp(self):
        """创建测试数据"""
        np.random.seed(42)
        dates = pd.date_range(start='2023-01-01', periods=100, freq='D')
        
        self.test_data = pd.DataFrame({
            'Date': dates,
            'Open': np.random.uniform(90, 110, 100),
            'High': np.random.uniform(100, 120, 100),
            'Low': np.random.uniform(80, 100, 100),
            'Close': np.random.uniform(90, 110, 100),
            'Volume': np.random.randint(100000, 1000000, 100)
        })
        
        # 确保High >= Close >= Low
        self.test_data['High'] = self.test_data[['Open', 'Close']].max(axis=1) + 5
        self.test_data['Low'] = self.test_data[['Open', 'Close']].min(axis=1) - 5
        
        self.ti = TechnicalIndicators()
    
    def test_sma(self):
        """测试简单移动平均线"""
        result = self.ti.sma(self.test_data, period=20)
        
        # 检查列是否创建
        self.assertIn('SMA_20', result.columns)
        
        # 检查前20行是否为NaN
        self.assertTrue(pd.isna(result['SMA_20'].iloc[0]))
        self.assertTrue(pd.isna(result['SMA_19']))
        
        # 检查第21行是否有效
        self.assertFalse(pd.isna(result['SMA_20'].iloc[20]))
        
        print("✓ SMA测试通过")
    
    def test_ema(self):
        """测试指数移动平均线"""
        result = self.ti.ema(self.test_data, period=12)
        
        # 检查列是否创建
        self.assertIn('EMA_12', result.columns)
        
        # EMA不应该有NaN（除了第一行）
        self.assertFalse(pd.isna(result['EMA_12'].iloc[1]))
        
        print("✓ EMA测试通过")
    
    def test_bollinger_bands(self):
        """测试布林带"""
        result = self.ti.bollinger_bands(self.test_data, period=20)
        
        # 检查所有列是否创建
        self.assertIn('BB_Upper', result.columns)
        self.assertIn('BB_Middle', result.columns)
        self.assertIn('BB_Lower', result.columns)
        self.assertIn('BB_Width', result.columns)
        
        # 检查上轨 >= 中轨 >= 下轨
        latest = result.iloc[-1]
        self.assertGreaterEqual(latest['BB_Upper'], latest['BB_Middle'])
        self.assertGreaterEqual(latest['BB_Middle'], latest['BB_Lower'])
        
        print("✓ 布林带测试通过")
    
    def test_rsi(self):
        """测试RSI指标"""
        result = self.ti.rsi(self.test_data, period=14)
        
        # 检查列是否创建
        self.assertIn('RSI_14', result.columns)
        
        # 检查RSI范围（0-100）
        valid_rsi = result['RSI_14'].dropna()
        self.assertTrue((valid_rsi >= 0).all())
        self.assertTrue((valid_rsi <= 100).all())
        
        print("✓ RSI测试通过")
    
    def test_macd(self):
        """测试MACD指标"""
        result = self.ti.macd(self.test_data)
        
        # 检查所有列是否创建
        self.assertIn('MACD', result.columns)
        self.assertIn('MACD_Signal', result.columns)
        self.assertIn('MACD_Histogram', result.columns)
        
        # 检查MACD柱状图 = MACD - 信号线
        latest = result.iloc[-1]
        expected_hist = latest['MACD'] - latest['MACD_Signal']
        self.assertAlmostEqual(latest['MACD_Histogram'], expected_hist, places=4)
        
        print("✓ MACD测试通过")
    
    def test_stoch_oscillator(self):
        """测试随机震荡指标"""
        result = self.ti.stoch_oscillator(self.test_data)
        
        # 检查列是否创建
        self.assertIn('Stoch_K', result.columns)
        self.assertIn('Stoch_D', result.columns)
        
        # 检查范围（0-100）
        valid_k = result['Stoch_K'].dropna()
        self.assertTrue((valid_k >= 0).all())
        self.assertTrue((valid_k <= 100).all())
        
        print("✓ 随机震荡指标测试通过")
    
    def test_williams_r(self):
        """测试威廉指标"""
        result = self.ti.williams_r(self.test_data)
        
        # 检查列是否创建
        self.assertIn('Williams_R', result.columns)
        
        # 检查范围（-100到0）
        valid_wr = result['Williams_R'].dropna()
        self.assertTrue((valid_wr >= -100).all())
        self.assertTrue((valid_wr <= 0).all())
        
        print("✓ 威廉指标测试通过")
    
    def test_obv(self):
        """测试OBV指标"""
        result = self.ti.obv(self.test_data)
        
        # 检查列是否创建
        self.assertIn('OBV', result.columns)
        self.assertIn('OBV_MA', result.columns)
        
        # OBV应该是累积值
        self.assertTrue(len(result['OBV'].dropna()) > 0)
        
        print("✓ OBV测试通过")
    
    def test_atr(self):
        """测试ATR指标"""
        result = self.ti.atr(self.test_data)
        
        # 检查列是否创建
        self.assertIn('ATR', result.columns)
        
        # ATR应该是正数
        valid_atr = result['ATR'].dropna()
        self.assertTrue((valid_atr > 0).all())
        
        print("✓ ATR测试通过")
    
    def test_keltner_channels(self):
        """测试肯特纳通道"""
        result = self.ti.keltner_channels(self.test_data)
        
        # 检查所有列是否创建
        self.assertIn('KC_Upper', result.columns)
        self.assertIn('KC_Middle', result.columns)
        self.assertIn('KC_Lower', result.columns)
        
        # 检查上轨 >= 中轨 >= 下轨
        latest = result.iloc[-1]
        self.assertGreaterEqual(latest['KC_Upper'], latest['KC_Middle'])
        self.assertGreaterEqual(latest['KC_Middle'], latest['KC_Lower'])
        
        print("✓ 肯特纳通道测试通过")
    
    def test_calculate_all_indicators(self):
        """测试计算所有指标"""
        result = self.ti.calculate_all_indicators(self.test_data)
        
        # 检查关键指标是否存在
        expected_columns = [
            'SMA_5', 'SMA_20', 'SMA_200',
            'EMA_12', 'EMA_26',
            'BB_Upper', 'BB_Middle', 'BB_Lower',
            'RSI_14',
            'MACD', 'MACD_Signal', 'MACD_Histogram',
            'OBV',
            'ATR'
        ]
        
        for col in expected_columns:
            self.assertIn(col, result.columns)
        
        print("✓ 所有指标计算测试通过")
    
    def test_trading_signals(self):
        """测试交易信号生成"""
        # 先计算所有指标
        data = self.ti.calculate_all_indicators(self.test_data)
        
        # 生成交易信号
        result = self.ti.get_trading_signals(data)
        
        # 检查信号列是否创建
        self.assertIn('Signal', result.columns)
        self.assertIn('Signal_Strength', result.columns)
        
        # 检查信号值
        valid_signals = result['Signal'].dropna()
        for signal in valid_signals:
            self.assertIn(signal, ['STRONG BUY', 'BUY', 'HOLD', 'SELL', 'STRONG SELL'])
        
        # 检查强度范围
        valid_strengths = result['Signal_Strength'].dropna()
        for strength in valid_strengths:
            self.assertGreaterEqual(strength, 0)
            self.assertLessEqual(strength, 5)
        
        print("✓ 交易信号测试通过")
    
    def test_get_summary(self):
        """测试获取摘要"""
        # 计算所有指标
        data = self.ti.calculate_all_indicators(self.test_data)
        
        # 获取摘要
        summary = self.ti.get_summary(data, latest=True)
        
        # 检查摘要结构
        self.assertIn('价格', summary)
        self.assertIn('趋势指标', summary)
        self.assertIn('动量指标', summary)
        
        print("✓ 摘要获取测试通过")


class TestTechnicalAnalyzer(unittest.TestCase):
    """测试技术分析器"""
    
    @classmethod
    def setUpClass(cls):
        """设置测试环境"""
        # 只在有网络时运行这些测试
        cls.skip_tests = False
    
    def setUp(self):
        """创建测试实例"""
        if self.skip_tests:
            self.skipTest("跳过需要网络的测试")
        
        from src.ai_inv.technical_analyzer import TechnicalAnalyzer
        self.analyzer = TechnicalAnalyzer()
    
    def test_analyze_stock(self):
        """测试分析股票"""
        if self.skip_tests:
            return
        
        # 分析恒生指数
        data = self.analyzer.analyze_stock('^HSI', period='1m')
        
        # 检查数据
        self.assertFalse(data.empty)
        self.assertIn('Close', data.columns)
        self.assertIn('RSI_14', data.columns)
        self.assertIn('Signal', data.columns)
        
        print("✓ 分析股票测试通过")
    
    def test_get_trading_signal(self):
        """测试获取交易信号"""
        if self.skip_tests:
            return
        
        signal = self.analyzer.get_trading_signal('^HSI')
        
        # 检查信号结构
        self.assertIn('价格', signal)
        self.assertIn('趋势指标', signal)
        self.assertIn('动量指标', signal)
        self.assertIn('交易信号', signal)
        
        print("✓ 获取交易信号测试通过")


def run_tests():
    """运行所有测试"""
    print("\n" + "="*60)
    print("技术分析模块测试")
    print("="*60 + "\n")
    
    # 创建测试套件
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # 添加测试
    suite.addTests(loader.loadTestsFromTestCase(TestTechnicalIndicators))
    suite.addTests(loader.loadTestsFromTestCase(TestTechnicalAnalyzer))
    
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
