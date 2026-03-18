"""
AI分析模块测试
测试AI分析和情感分析功能
"""

import unittest
import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.ai_inv.ai_analyzer import AIAnalyzer
from src.ai_inv.sentiment_analyzer import SentimentAnalyzer, NewsSentimentAnalyzer


class TestAIAnalyzer(unittest.TestCase):
    """测试AI分析器"""
    
    def setUp(self):
        """创建测试实例"""
        self.analyzer = AIAnalyzer()
    
    def test_init(self):
        """测试初始化"""
        self.assertIsNotNone(self.analyzer)
        self.assertIsNotNone(self.analyzer.openai_client)
    
    def test_analyze_stock_with_ai(self):
        """测试AI股票分析"""
        # 准备测试数据
        technical_data = {
            '价格': {
                '收盘价': 28000.0,
                '涨跌幅': '+1.5%'
            },
            '趋势指标': {
                '20日均线': '27500.0',
                '50日均线': '27000.0'
            },
            '动量指标': {
                'RSI': '65.5',
                'RSI状态': '正常'
            },
            '交易信号': 'BUY',
            '信号强度': 3
        }
        
        # 执行分析
        result = self.analyzer.analyze_stock_with_ai('^HSI', technical_data)
        
        # 验证结果
        self.assertIsInstance(result, dict)
        self.assertIn('status', result)
        
        print("✓ AI股票分析测试通过")
    
    def test_get_investment_advice(self):
        """测试获取投资建议"""
        technical_data = {
            '价格': {'收盘价': 5.20, '涨跌幅': '-2.5%'},
            '趋势指标': {'20日均线': '5.50', '50日均线': '5.80'},
            '动量指标': {'RSI': '25.5', 'RSI状态': '超卖'},
            '交易信号': 'HOLD',
            '信号强度': 0
        }
        
        advice = self.analyzer.get_investment_advice('6158.HK', technical_data)
        
        self.assertIsInstance(advice, dict)
        self.assertIn('raw_response', advice)
        
        print("✓ 获取投资建议测试通过")
    
    def test_explain_indicator(self):
        """测试指标解释"""
        explanation = self.analyzer.explain_indicator(
            indicator_name='RSI',
            value=65.5,
            context='港股分析'
        )
        
        self.assertIsInstance(explanation, str)
        self.assertGreater(len(explanation), 0)
        
        print("✓ 指标解释测试通过")


class TestSentimentAnalyzer(unittest.TestCase):
    """测试情感分析器"""
    
    def setUp(self):
        """创建测试实例"""
        self.analyzer = SentimentAnalyzer()
    
    def test_init(self):
        """测试初始化"""
        self.assertIsNotNone(self.analyzer)
        self.assertIsNotNone(self.analyzer.positive_words)
        self.assertIsNotNone(self.analyzer.negative_words)
    
    def test_analyze_positive_text(self):
        """测试正面文本分析"""
        text = "恆生指數今日上漲2%，市場情緒樂觀，投資者信心增強"
        result = self.analyzer.analyze_text(text)
        
        self.assertEqual(result['sentiment'], 'positive')
        self.assertGreater(result['score'], 0)
        self.assertGreater(result['positive_count'], 0)
        
        print("✓ 正面文本分析测试通过")
    
    def test_analyze_negative_text(self):
        """测试负面文本分析"""
        text = "恆生指數今日下跌3%，市場出現恐慌情緒。疫情復發影響經濟前景"
        result = self.analyzer.analyze_text(text)
        
        self.assertEqual(result['sentiment'], 'negative')
        self.assertLess(result['score'], 0)
        self.assertGreater(result['negative_count'], 0)
        
        print("✓ 负面文本分析测试通过")
    
    def test_analyze_neutral_text(self):
        """测试中性文本分析"""
        text = "恆生指數今日收盤價為28000點"
        result = self.analyzer.analyze_text(text)
        
        self.assertIn(result['sentiment'], ['neutral', 'positive', 'negative'])
        self.assertIsInstance(result['score'], float)
        
        print("✓ 中性文本分析测试通过")
    
    def test_sentiment_strength(self):
        """测试情感强度"""
        # 强正面
        strong_positive = "恆生指數暴漲5%，創下新高！市場狂歡，投資者興奮！"
        result = self.analyzer.analyze_text(strong_positive)
        self.assertEqual(result['strength'], 'strong')
        
        # 弱正面
        weak_positive = "恆生指數小幅上漲"
        result = self.analyzer.analyze_text(weak_positive)
        self.assertIn(result['strength'], ['weak', 'moderate'])
        
        print("✓ 情感强度测试通过")
    
    def test_extract_sentiment_words(self):
        """测试情感词提取"""
        text = "恆生指數上漲，盈利增長，業績優異"
        result = self.analyzer.analyze_text(text)
        
        self.assertGreater(len(result['positive_words']), 0)
        
        # 检查是否提取到预期词汇
        expected_words = ['上漲', '盈利增長', '業績優異']
        found_words = result['positive_words']
        
        # 至少找到一个预期词汇
        self.assertTrue(any(word in found_words for word in expected_words))
        
        print("✓ 情感词提取测试通过")
    
    def test_confidence_calculation(self):
        """测试置信度计算"""
        # 长文本应该有更高的置信度
        long_text = "恆生指數今日上漲2%，市場情緒樂觀，投資者信心增強。" * 10
        result_long = self.analyzer.analyze_text(long_text)
        
        short_text = "恆生指數上漲"
        result_short = self.analyzer.analyze_text(short_text)
        
        self.assertGreaterEqual(result_long['confidence'], result_short['confidence'])
        
        print("✓ 置信度计算测试通过")


class TestNewsSentimentAnalyzer(unittest.TestCase):
    """测试新闻情感分析器"""
    
    def setUp(self):
        """创建测试实例"""
        self.analyzer = NewsSentimentAnalyzer()
    
    def test_analyze_single_news(self):
        """测试分析单条新闻"""
        news = {
            'title': '恆生指數突破30000點',
            'summary': '受惠於市場樂觀情緒，恆生指數今日上升300點',
            'time': '2026-03-13 10:30:00',
            'source': '財經日報'
        }
        
        result = self.analyzer.analyze_news_sentiment(news)
        
        self.assertIn('sentiment', result)
        self.assertIn('score', result)
        self.assertEqual(result['news_source'], '財經日報')
        
        print("✓ 单条新闻分析测试通过")
    
    def test_batch_analyze_news(self):
        """测试批量分析新闻"""
        news_list = [
            {
                'title': '恆生指數突破30000點',
                'summary': '受惠於市場樂觀情緒，恆生指數今日上升300點',
                'time': '2026-03-13 10:30:00',
                'source': '財經日報'
            },
            {
                'title': '科技股表現突出',
                'summary': '多隻大型科技股上漲超過5%，帶動大市上升',
                'time': '2026-03-13 11:00:00',
                'source': '經濟日報'
            },
            {
                'title': '房地產股面臨壓力',
                'summary': '受政策影響，房地產股普遍下跌',
                'time': '2026-03-13 14:00:00',
                'source': '明報'
            }
        ]
        
        result = self.analyzer.batch_analyze_news(news_list)
        
        self.assertEqual(result['news_analyzed'], 3)
        self.assertIn('overall_sentiment', result)
        self.assertIn('average_score', result)
        self.assertGreater(result['positive_count'], 0)
        
        print("✓ 批量新闻分析测试通过")
    
    def test_get_sentiment_summary(self):
        """测试获取情感摘要"""
        news_list = [
            {
                'title': '恆生指數突破30000點',
                'summary': '受惠於市場樂觀情緒，恆生指數今日上升300點',
                'time': '2026-03-13 10:30:00',
                'source': '財經日報'
            }
        ]
        
        summary = self.analyzer.get_sentiment_summary(news_list)
        
        self.assertIsInstance(summary, str)
        self.assertIn('新闻情感分析摘要', summary)
        self.assertIn('分析新闻数量', summary)
        
        print("✓ 情感摘要获取测试通过")


class TestSentimentTrend(unittest.TestCase):
    """测试情感趋势分析"""
    
    def setUp(self):
        """创建测试实例"""
        self.analyzer = SentimentAnalyzer()
    
    def test_analyze_sentiment_trend(self):
        """测试情感趋势分析"""
        # 模拟历史数据
        sentiment_history = [
            {'score': 0.3, 'time': '2026-03-10'},
            {'score': 0.5, 'time': '2026-03-11'},
            {'score': 0.7, 'time': '2026-03-12'},
            {'score': 0.8, 'time': '2026-03-13'}
        ]
        
        trend = self.analyzer.analyze_sentiment_trend(sentiment_history)
        
        self.assertIn('trend', trend)
        self.assertIn('message', trend)
        self.assertEqual(trend['trend'], 'improving')
        
        print("✓ 情感趋势分析测试通过")
    
    def test_declining_trend(self):
        """测试下降趋势"""
        sentiment_history = [
            {'score': 0.8, 'time': '2026-03-10'},
            {'score': 0.6, 'time': '2026-03-11'},
            {'score': 0.4, 'time': '2026-03-12'},
            {'score': 0.2, 'time': '2026-03-13'}
        ]
        
        trend = self.analyzer.analyze_sentiment_trend(sentiment_history)
        
        self.assertEqual(trend['trend'], 'declining')
        
        print("✓ 下降趋势测试通过")
    
    def test_stable_trend(self):
        """测试稳定趋势"""
        sentiment_history = [
            {'score': 0.5, 'time': '2026-03-10'},
            {'score': 0.52, 'time': '2026-03-11'},
            {'score': 0.48, 'time': '2026-03-12'},
            {'score': 0.51, 'time': '2026-03-13'}
        ]
        
        trend = self.analyzer.analyze_sentiment_trend(sentiment_history)
        
        self.assertEqual(trend['trend'], 'stable')
        
        print("✓ 稳定趋势测试通过")


class TestHybridAI(unittest.TestCase):
    """测试混合AI分析 (已降級為 AIAnalyzer)"""
    
    def setUp(self):
        """创建测试实例"""
        from src.ai_inv.ai_analyzer import AIAnalyzer
        self.analyzer = AIAnalyzer()
    
    def test_init(self):
        """测试初始化"""
        self.assertIsNotNone(self.analyzer)
    
    def test_analyze_with_consensus(self):
        """测试共识分析 (模擬)"""
        technical_data = {
            '价格': {'收盘价': 28000.0},
            '交易信号': 'BUY',
            '信号强度': 3
        }
        
        # 由於 HybridAIAnalyzer 已移除，這裡僅做基本驗證
        self.assertIsNotNone(self.analyzer)
        print("✓ 共识分析測試 (已跳過詳細邏輯)")


def run_tests():
    """运行所有测试"""
    print("\n" + "="*60)
    print("AI分析模块测试")
    print("="*60 + "\n")
    
    # 创建测试套件
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # 添加测试
    suite.addTests(loader.loadTestsFromTestCase(TestAIAnalyzer))
    suite.addTests(loader.loadTestsFromTestCase(TestSentimentAnalyzer))
    suite.addTests(loader.loadTestsFromTestCase(TestNewsSentimentAnalyzer))
    suite.addTests(loader.loadTestsFromTestCase(TestSentimentTrend))
    suite.addTests(loader.loadTestsFromTestCase(TestHybridAI))
    
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
