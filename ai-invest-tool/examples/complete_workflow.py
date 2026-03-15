"""
完整工作流示例
展示从数据获取到报告生成的完整流程

这个示例涵盖了:
1. 数据获取
2. 技术分析
3. AI分析
4. 策略回测
5. 投资组合分析
6. 报告生成
"""

import sys
import os

# 添加src到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.ai_inv.data_fetcher import DataFetcher
from src.ai_inv.technical_analyzer import TechnicalAnalyzer
from src.ai_inv.ai_analyzer import AIAnalyzer
from src.ai_inv.sentiment_analyzer import SentimentAnalyzer
from src.ai_inv.smart_advisor import SmartAdvisor
from src.ai_inv.backtester import BacktestEngine, MAStrategy, RSIStrategy, MACDStrategy
from src.ai_inv.portfolio_optimizer import PortfolioOptimizer, RiskManager
from src.ai_inv.excel_visualizer import ExcelVisualizer

import pandas as pd
from datetime import datetime


def main():
    """主工作流"""
    
    print("=" * 80)
    print("AI投资工具 - 完整工作流示例")
    print("=" * 80)
    
    # 步骤1: 数据获取
    print("\n步骤1: 数据获取")
    print("-" * 80)
    fetcher = DataFetcher()
    
    symbols = ['^HSI', '6158.HK', '7200.HK']
    
    # 获取所有股票数据
    all_data = {}
    for symbol in symbols:
        print(f"正在获取 {symbol} 数据...")
        data = fetcher.get_historical_data(symbol, period='1y')
        if data is not None and not data.empty:
            all_data[symbol] = data
            print(f"  ✅ 获取成功: {len(data)} 条数据")
        else:
            print(f"  ❌ 获取失败")
    
    if not all_data:
        print("\n❌ 没有获取到任何数据，退出...")
        return
    
    # 步骤2: 技术分析
    print("\n步骤2: 技术分析")
    print("-" * 80)
    
    analyzer = TechnicalAnalyzer()
    
    # 分析每只股票
    all_indicators = {}
    all_signals = {}
    
    for symbol, data in all_data.items():
        print(f"\n分析 {symbol}:")
        
        # 计算所有指标
        indicators = TechnicalIndicators().calculate_all_indicators(data)
        all_indicators[symbol] = indicators
        
        # 获取交易信号
        signal = analyzer.get_trading_signal(symbol)
        all_signals[symbol] = signal
        
        # 显示关键指标
        print(f"  最新价格: HK${data['Close'].iloc[-1]:.2f}")
        print(f"  RSI(14): {indicators['RSI'].iloc[-1]:.2f}")
        print(f"  交易信号: {signal['交易信号']}")
        print(f"  信号强度: {signal['强度']}")
    
    # 步骤3: 寻找交易机会
    print("\n步骤3: 寻找交易机会")
    print("-" * 80)
    
    opportunities = analyzer.find_opportunities(
        symbols=symbols,
        signal_type='BUY',
        min_strength=2
    )
    
    if opportunities:
        print("\n买入机会:")
        for opp in opportunities:
            print(f"  {opp['股票代码']}: {opp['信号']} (强度: {opp['强度']})")
    else:
        print("\n当前没有明显的买入机会")
    
    # 步骤4: AI分析（需要API Key）
    print("\n步骤4: AI分析")
    print("-" * 80)
    
    # 检查是否有API Key
    api_key = os.environ.get('OPENAI_API_KEY')
    
    if api_key:
        print("检测到OpenAI API Key，进行AI分析...")
        
        ai_analyzer = AIAnalyzer()
        ai_results = {}
        
        for symbol in symbols[:1]:  # 只分析第一个股票（节省成本）
            print(f"\nAI分析 {symbol}:")
            
            # 准备技术数据
            tech_data = {
                '价格': {
                    '收盘价': all_data[symbol]['Close'].iloc[-1],
                    '涨跌幅': ((all_data[symbol]['Close'].iloc[-1] - 
                               all_data[symbol]['Close'].iloc[-2]) / 
                               all_data[symbol]['Close'].iloc[-2] * 100)
                },
                '技术指标': {
                    'RSI': all_indicators[symbol]['RSI'].iloc[-1]
                },
                '交易信号': all_signals[symbol]['交易信号'],
                '信号强度': all_signals[symbol]['强度']
            }
            
            # AI分析
            ai_result = ai_analyzer.analyze_stock_with_ai(symbol, tech_data)
            ai_results[symbol] = ai_result
            
            print(f"  AI建议: {ai_result['recommendation']}")
            print(f"  置信度: {ai_result['confidence']:.1%}")
    else:
        print("未检测到OpenAI API Key，跳过AI分析")
        print("设置方法: export OPENAI_API_KEY='your-api-key'")
        ai_results = {}
    
    # 步骤5: 策略回测
    print("\n步骤5: 策略回测")
    print("-" * 80)
    
    # 选择一只股票进行回测
    test_symbol = symbols[0]
    data = all_data[test_symbol]
    
    print(f"对 {test_symbol} 进行策略回测...")
    
    # 创建多个策略
    strategies = [
        ('MA(5,20)', MAStrategy(5, 20)),
        ('RSI(14)', RSIStrategy(14)),
        ('MACD(12,26,9)', MACDStrategy(12, 26, 9))
    ]
    
    backtest_results = []
    
    for strategy_name, strategy in strategies:
        print(f"\n回测策略: {strategy_name}")
        
        # 创建回测引擎
        engine = BacktestEngine(
            initial_capital=100000,
            commission=0.001
        )
        
        # 运行回测
        results = engine.run_backtest(data, strategy)
        
        # 保存结果
        results['strategy_name'] = strategy_name
        backtest_results.append(results)
        
        # 显示关键指标
        summary = results['summary']
        print(f"  总收益率: {summary['total_return']:.2f}%")
        print(f"  年化收益: {summary['annual_return']:.2f}%")
        print(f"  夏普比率: {summary['sharpe_ratio']:.2f}")
        print(f"  最大回撤: {summary['max_drawdown']:.2f}%")
        print(f"  胜率: {summary['win_rate']:.2f}%")
    
    # 步骤6: 投资组合优化
    print("\n步骤6: 投资组合优化")
    print("-" * 80)
    
    # 准备收益率数据
    returns_data = {}
    for symbol, data in all_data.items():
        returns = data['Close'].pct_change().dropna()
        returns_data[symbol] = returns
    
    returns_df = pd.DataFrame(returns_data).dropna()
    
    # 创建优化器
    optimizer = PortfolioOptimizer(risk_free_rate=0.02)
    
    # 优化组合
    print("正在优化投资组合...")
    optimized_result = optimizer.optimize_portfolio(returns_df, method='sharpe')
    
    print("\n最优投资组合权重:")
    for symbol, weight in optimized_result['weights'].items():
        print(f"  {symbol}: {weight:.2%}")
    
    print(f"\n预期年化收益: {optimized_result['expected_return']:.2%}")
    print(f"年化波动率: {optimized_result['volatility']:.2%}")
    print(f"夏普比率: {optimized_result['sharpe_ratio']:.2f}")
    
    # 步骤7: 生成报告
    print("\n步骤7: 生成报告")
    print("-" * 80)
    
    visualizer = ExcelVisualizer(output_dir='output/excel')
    
    # 为每只股票生成分析报告
    for symbol in symbols:
        if symbol in all_data:
            print(f"\n生成 {symbol} 分析报告...")
            
            # 准备AI分析（如果有）
            ai_analysis = ai_results.get(symbol) if api_key else None
            
            # 生成报告
            filepath = visualizer.generate_stock_report(
                symbol=symbol,
                price_data=all_data[symbol],
                indicators=all_indicators[symbol],
                ai_analysis=ai_analysis
            )
            print(f"  ✅ 报告已生成: {filepath}")
    
    # 生成回测报告
    print("\n生成回测报告...")
    for results in backtest_results:
        filepath = visualizer.generate_backtest_report(
            results=results,
            strategy_name=results['strategy_name']
        )
        print(f"  ✅ {results['strategy_name']} 回测报告已生成: {filepath}")
    
    # 步骤8: 总结
    print("\n" + "=" * 80)
    print("工作流完成！")
    print("=" * 80)
    
    print("\n总结:")
    print(f"  分析股票数量: {len(symbols)}")
    print(f"  交易机会: {len(opportunities)} 个")
    print(f"  回测策略: {len(strategies)} 个")
    print(f"  生成报告: {len(symbols) + len(strategies)} 份")
    
    print("\n报告位置:")
    print(f"  output/excel/")
    
    print("\n下一步:")
    print("  1. 查看生成的Excel报告")
    print("  2. 使用Web界面进行交互式分析: streamlit run src/ai_inv/web_dashboard.py")
    print("  3. 根据分析结果调整投资策略")
    
    print("\n" + "=" * 80)


def advanced_workflow():
    """高级工作流 - 包含更多功能"""
    
    print("\n" + "=" * 80)
    print("AI投资工具 - 高级工作流")
    print("=" * 80)
    
    # 1. 情感分析
    print("\n高级功能1: 情感分析")
    print("-" * 80)
    
    sentiment_analyzer = SentimentAnalyzer()
    
    news_texts = [
        "恆生指數今日上漲2%，市場情緒樂觀，投資者對經濟前景看好",
        "科技股表現突出，多隻股票創新高，買盤積極",
        "市場擔憂通脹壓力，部分投資者選擇獲利了結"
    ]
    
    for i, text in enumerate(news_texts, 1):
        result = sentiment_analyzer.analyze_text(text)
        print(f"\n新闻 {i}:")
        print(f"  内容: {text}")
        print(f"  情感: {result['sentiment']}")
        print(f"  分数: {result['score']:.2f}")
    
    # 2. 智能顾问
    print("\n\n高级功能2: 智能投资顾问")
    print("-" * 80)
    
    if os.environ.get('OPENAI_API_KEY'):
        advisor = SmartAdvisor()
        
        # 综合分析
        symbol = '^HSI'
        print(f"\n对 {symbol} 进行综合分析...")
        
        analysis = advisor.get_comprehensive_analysis(symbol)
        
        print(f"\n投资建议: {analysis['recommendation']['action']}")
        print(f"置信度: {analysis['recommendation']['confidence']:.1%}")
        print(f"风险等级: {analysis['recommendation']['risk_level']}")
        
        # 生成投资计划
        print("\n生成投资计划...")
        plan = advisor.get_investment_plan(
            symbol=symbol,
            capital=100000,
            risk_tolerance='medium',
            investment_goal='growth'
        )
        
        print(f"\n入场策略: {plan.get('entry_strategy', 'N/A')}")
        print(f"止损价位: {plan.get('stop_loss', 'N/A')}")
        print(f"止盈价位: {plan.get('take_profit', 'N/A')}")
        print(f"建议仓位: {plan.get('position_size', 'N/A')}")
    else:
        print("未配置API Key，跳过智能顾问分析")
    
    # 3. 风险管理
    print("\n\n高级功能3: 风险管理")
    print("-" * 80)
    
    risk_manager = RiskManager(
        max_position_size=0.2,  # 单个股票最大20%仓位
        max_portfolio_risk=0.25  # 组合最大风险25%
    )
    
    # 计算建议仓位
    capital = 100000
    risk_per_trade = 0.02  # 每笔交易2%风险
    stop_loss_pct = 0.05  # 5%止损
    
    position_size = risk_manager.calculate_position_size(
        capital=capital,
        risk_per_trade=risk_per_trade,
        stop_loss_pct=stop_loss_pct
    )
    
    print(f"\n风险管理建议:")
    print(f"  总资金: HK${capital:,.2f}")
    print(f"  单笔风险: {risk_per_trade:.1%}")
    print(f"  止损比例: {stop_loss_pct:.1%}")
    print(f"  建议仓位: HK${position_size:,.2f}")
    
    # 4. 蒙特卡洛模拟
    print("\n\n高级功能4: 蒙特卡洛模拟")
    print("-" * 80)
    
    print("正在进行蒙特卡洛模拟...")
    
    mc_result = optimizer.monte_carlo_simulation(
        returns_df=returns_df,
        n_simulations=1000,
        n_periods=252  # 1年交易日
    )
    
    print(f"\n模拟结果 ({mc_result['n_simulations']} 次):")
    print(f"  平均收益: {mc_result['mean_return']:.2%}")
    print(f"  标准差: {mc_result['std_return']:.2%}")
    print(f"  95%置信区间: [{mc_result['percentile_5']:.2%}, {mc_result['percentile_95']:.2%}]")
    
    print("\n" + "=" * 80)
    print("高级工作流完成！")
    print("=" * 80)


if __name__ == "__main__":
    # 运行基本工作流
    main()
    
    # 运行高级工作流
    print("\n" + "=" * 80)
    print("是否运行高级工作流？(需要更多时间和资源)")
    
    choice = input("输入 y 继续，其他键跳过: ")
    
    if choice.lower() == 'y':
        advanced_workflow()
    
    print("\n\n感谢使用AI投资工具！")
