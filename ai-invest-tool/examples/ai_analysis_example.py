"""
AI分析示例
展示如何使用AI分析模块
"""

import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.ai_inv.ai_analyzer import AIAnalyzer
from src.ai_inv.sentiment_analyzer import SentimentAnalyzer, NewsSentimentAnalyzer
from src.ai_inv.smart_advisor import SmartAdvisor


def example_1_ai_stock_analysis():
    """示例1: AI股票分析"""
    print("\n" + "="*60)
    print("示例1: AI股票分析")
    print("="*60)
    
    # 创建AI分析器
    analyzer = AIAnalyzer()
    
    # 准备技术数据
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
    
    # AI分析
    result = analyzer.analyze_stock_with_ai('^HSI', technical_data)
    
    print("\nAI分析结果:")
    print(f"状态: {result.get('status', 'unknown')}")
    if 'raw_response' in result:
        print(f"响应: {result['raw_response'][:200]}...")


def example_2_investment_advice():
    """示例2: 获取投资建议"""
    print("\n" + "="*60)
    print("示例2: 获取投资建议")
    print("="*60)
    
    analyzer = AIAnalyzer()
    
    technical_data = {
        '价格': {'收盘价': 5.20, '涨跌幅': '-2.5%'},
        '趋势指标': {'20日均线': '5.50', '50日均线': '5.80'},
        '动量指标': {'RSI': '25.5', 'RSI状态': '超卖'},
        '交易信号': 'HOLD',
        '信号强度': 0
    }
    
    advice = analyzer.get_investment_advice('6158.HK', technical_data)
    
    print("\n投资建议:")
    print(f"是否建议投资: {advice.get('是否投资', 'N/A')}")
    print(f"建议仓位: {advice.get('建议仓位比例', 'N/A')}")
    print(f"买入时机: {advice.get('买入时机', 'N/A')}")
    
    if 'raw_response' in advice:
        print(f"\n详细建议: {advice['raw_response'][:300]}...")


def example_3_sentiment_analysis():
    """示例3: 情感分析"""
    print("\n" + "="*60)
    print("示例3: 情感分析")
    print("="*60)
    
    analyzer = SentimentAnalyzer()
    
    # 分析正面新闻
    positive_text = "恒生指數今日上漲2%，市場情緒樂觀，投資者信心增強。多隻藍籌股創新高，科技股表現突出。"
    result = analyzer.analyze_text(positive_text)
    
    print("\n正面新闻分析:")
    print(f"情感: {result['sentiment']}")
    print(f"分数: {result['score']:.2f}")
    print(f"强度: {result['strength']}")
    print(f"正面词: {result['positive_words'][:5]}")
    print(f"负面词: {result['negative_words'][:5]}")
    
    # 分析负面新闻
    negative_text = "恒生指數今日下跌3%，市場出現恐慌情緒。疫情復發影響經濟前景，投資者擔憂企業盈利下滑。"
    result = analyzer.analyze_text(negative_text)
    
    print("\n\n负面新闻分析:")
    print(f"情感: {result['sentiment']}")
    print(f"分数: {result['score']:.2f}")
    print(f"强度: {result['strength']}")


def example_4_news_sentiment_analysis():
    """示例4: 新闻情感分析"""
    print("\n" + "="*60)
    print("示例4: 新闻情感分析")
    print("="*60)
    
    analyzer = NewsSentimentAnalyzer()
    
    # 模拟新闻列表
    news_list = [
        {
            'title': '恆生指數突破30000點',
            'summary': '受惠於市場樂觀情緒，恆生指數今日上升300點，突破30000點關口。',
            'time': '2026-03-13 10:30:00',
            'source': '財經日報'
        },
        {
            'title': '科技股表現突出',
            'summary': '多隻大型科技股上漲超過5%，帶動大市上升。市場對科技業前景樂觀。',
            'time': '2026-03-13 11:00:00',
            'source': '經濟日報'
        },
        {
            'title': '房地產股面臨壓力',
            'summary': '受政策影響，房地產股普遍下跌。市場擔憂樓市前景不明朗。',
            'time': '2026-03-13 14:00:00',
            'source': '明報'
        }
    ]
    
    # 批量分析
    result = analyzer.batch_analyze_news(news_list)
    
    print(f"\n分析新闻数量: {result['news_analyzed']}")
    print(f"整体情感: {result['overall_sentiment']}")
    print(f"平均分数: {result['average_score']:.2f}")
    print(f"\n情感分布:")
    print(f"  正面: {result['positive_count']} 条")
    print(f"  负面: {result['negative_count']} 条")
    print(f"  中性: {result['neutral_count']} 条")
    
    # 获取摘要
    summary = analyzer.get_sentiment_summary(news_list)
    print(summary)


def example_5_smart_advisor_comprehensive():
    """示例5: 智能顾问综合分析"""
    print("\n" + "="*60)
    print("示例5: 智能顾问综合分析")
    print("="*60)
    
    advisor = SmartAdvisor()
    
    # 获取综合分析
    analysis = advisor.get_comprehensive_analysis('^HSI', period='1y', include_news=True)
    
    print(f"\n股票: {analysis['symbol']}")
    print(f"分析时间: {analysis['analysis_time']}")
    
    # 显示建议
    rec = analysis['recommendation']
    print(f"\n综合建议:")
    print(f"  操作: {rec['action']}")
    print(f"  理由: {rec['reason']}")
    print(f"  风险: {rec['risk_level']}")
    print(f"  置信度: {rec['confidence']}")
    print(f"  总分: {rec['total_score']}/10")
    
    print(f"\n评分分解:")
    print(f"  技术面: {rec['technical_score']}/10")
    print(f"  AI分析: {rec['ai_score']}/10")
    print(f"  情感分析: {rec['sentiment_score']}/10")


def example_6_investment_plan():
    """示例6: 生成投资计划"""
    print("\n" + "="*60)
    print("示例6: 生成投资计划")
    print("="*60)
    
    advisor = SmartAdvisor()
    
    # 生成投资计划
    plan = advisor.get_investment_plan(
        symbol='^HSI',
        capital=100000,  # 10万港元
        risk_tolerance='medium',
        investment_goal='growth'
    )
    
    print(f"\n投资计划: {plan['symbol']}")
    print(f"本金: HK${plan['capital']:,.0f}")
    print(f"风险承受能力: {plan['risk_tolerance']}")
    print(f"投资目标: {plan['investment_goal']}")
    
    print(f"\n入场策略:")
    entry = plan['entry_strategy']
    print(f"  策略: {entry['strategy']}")
    if 'first_entry' in entry:
        print(f"  首次入场价: HK${entry['first_entry']:.2f}")
    if 'batch_count' in entry:
        print(f"  批次数: {entry['batch_count']}")
    
    print(f"\n止损止盈:")
    print(f"  止损位: HK${plan['stop_loss']:.2f}")
    print(f"  止盈位: HK${plan['take_profit']:.2f}")
    
    print(f"\n仓位管理:")
    print(f"  建议仓位: HK${plan['position_size']:,.0f} ({plan['position_size']/plan['capital']*100:.1f}%)")
    
    print(f"\n时间周期: {plan['time_horizon']}")
    
    print(f"\n风险控制措施:")
    for i, control in enumerate(plan['risk_control'], 1):
        print(f"  {i}. {control}")


def example_7_compare_stocks():
    """示例7: 比较多只股票"""
    print("\n" + "="*60)
    print("示例7: 比较多只股票")
    print("="*60)
    
    advisor = SmartAdvisor()
    
    symbols = ['^HSI', '6158.HK', '7200.HK']
    
    # 比较
    comparison = advisor.compare_multiple_stocks(symbols)
    
    print(f"\n比较 {comparison['stocks_analyzed']} 只股票")
    
    # 显示排名
    print("\n排名:")
    for i, stock in enumerate(comparison['rankings'], 1):
        print(f"{i}. {stock['symbol']} - 评分: {stock['score']:.1f}/10 - 建议: {stock['action']}")
    
    print(f"\n建议: {comparison['recommendations']['recommendation']}")


def example_8_detailed_report():
    """示例8: 生成详细报告"""
    print("\n" + "="*60)
    print("示例8: 生成详细报告")
    print("="*60)
    
    advisor = SmartAdvisor()
    
    # 生成报告
    report = advisor.generate_detailed_report('^HSI')
    
    print(report)


def main():
    """运行所有示例"""
    print("\n" + "="*60)
    print("AI投资工具 - AI分析示例")
    print("="*60)
    
    examples = [
        ("AI股票分析", example_1_ai_stock_analysis),
        ("获取投资建议", example_2_investment_advice),
        ("情感分析", example_3_sentiment_analysis),
        ("新闻情感分析", example_4_news_sentiment_analysis),
        ("智能顾问综合分析", example_5_smart_advisor_comprehensive),
        ("生成投资计划", example_6_investment_plan),
        ("比较多只股票", example_7_compare_stocks),
        ("生成详细报告", example_8_detailed_report),
    ]
    
    print("\n可用的示例:")
    for i, (name, _) in enumerate(examples, 1):
        print(f"{i}. {name}")
    
    print("\n运行所有示例...")
    
    try:
        for name, example_func in examples:
            example_func()
    except Exception as e:
        print(f"\n运行示例时出错: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "="*60)
    print("所有示例运行完成!")
    print("="*60)


if __name__ == '__main__':
    main()
