"""
回测引擎使用示例
展示如何使用回测引擎验证交易策略
"""

import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

from src.ai_inv.backtester import (
    BacktestEngine,
    MAStrategy,
    RSIStrategy,
    MACDStrategy,
    CombinedStrategy,
    BacktestReport
)
from src.ai_inv.data_manager import DataManager
from src.ai_inv.indicators import TechnicalIndicators


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


def example_1_basic_backtest():
    """示例1: 基本回测"""
    print("\n" + "="*60)
    print("示例1: 基本回测")
    print("="*60)
    
    # 创建回测引擎
    engine = BacktestEngine(
        initial_capital=100000,  # 10万港元
        commission=0.001,  # 0.1%手续费
        slippage=0.0005  # 0.05%滑点
    )
    
    # 生成测试数据
    data = generate_test_data(days=252)
    
    # 创建策略
    strategy = MAStrategy(short_period=5, long_period=20)
    
    print(f"\n使用策略: {strategy.name}")
    
    # 运行回测
    results = engine.run_backtest(data, strategy)
    
    # 显示结果
    print("\n回测结果:")
    print(f"初始资金: HK${results['summary']['initial_capital']:,.2f}")
    print(f"最终资金: HK${results['summary']['final_capital']:,.2f}")
    print(f"总收益率: {results['summary']['total_return']:.2f}%")
    print(f"年化收益率: {results['summary']['annual_return']:.2f}%")
    print(f"最大回撤: {results['summary']['max_drawdown']:.2f}%")
    print(f"夏普比率: {results['summary']['sharpe_ratio']:.2f}")


def example_2_rsi_strategy():
    """示例2: RSI策略回测"""
    print("\n" + "="*60)
    print("示例2: RSI策略回测")
    print("="*60)
    
    engine = BacktestEngine(initial_capital=100000)
    data = generate_test_data(days=252)
    
    # 创建RSI策略
    strategy = RSIStrategy(
        period=14,
        oversold=30.0,
        overbought=70.0
    )
    
    print(f"\n使用策略: {strategy.name}")
    print("RSI参数:")
    print(f"  周期: {strategy.period}")
    print(f"  超卖阈值: {strategy.oversold}")
    print(f"  超买阈值: {strategy.overbought}")
    
    # 运行回测
    results = engine.run_backtest(data, strategy)
    
    print("\n回测结果:")
    print(f"总收益率: {results['summary']['total_return']:.2f}%")
    print(f"年化收益率: {results['summary']['annual_return']:.2f}%")
    print(f"夏普比率: {results['summary']['sharpe_ratio']:.2f}")
    print(f"交易次数: {results['trades']['total_trades']}")
    print(f"胜率: {results['trades']['win_rate']:.2f}%")


def example_3_macd_strategy():
    """示例3: MACD策略回测"""
    print("\n" + "="*60)
    print("示例3: MACD策略回测")
    print("="*60)
    
    engine = BacktestEngine(initial_capital=100000)
    data = generate_test_data(days=252)
    
    # 创建MACD策略
    strategy = MACDStrategy(
        fast_period=12,
        slow_period=26,
        signal_period=9
    )
    
    print(f"\n使用策略: {strategy.name}")
    print("MACD参数:")
    print(f"  快线周期: {strategy.fast_period}")
    print(f"  慢线周期: {strategy.slow_period}")
    print(f"  信号线周期: {strategy.signal_period}")
    
    # 运行回测
    results = engine.run_backtest(data, strategy)
    
    print("\n回测结果:")
    print(f"总收益率: {results['summary']['total_return']:.2f}%")
    print(f"最大回撤: {results['summary']['max_drawdown']:.2f}%")
    print(f"夏普比率: {results['summary']['sharpe_ratio']:.2f}")


def example_4_combined_strategy():
    """示例4: 组合策略回测"""
    print("\n" + "="*60)
    print("示例4: 组合策略回测")
    print("="*60)
    
    engine = BacktestEngine(initial_capital=100000)
    data = generate_test_data(days=252)
    
    # 创建组合策略
    strategies = [
        MAStrategy(short_period=5, long_period=20),
        RSIStrategy(period=14, oversold=30, overbought=70),
        MACDStrategy(fast_period=12, slow_period=26, signal_period=9)
    ]
    
    combined_strategy = CombinedStrategy(strategies)
    
    print(f"\n使用策略: {combined_strategy.name}")
    print(f"包含 {len(strategies)} 个子策略:")
    for s in strategies:
        print(f"  - {s.name}")
    
    # 运行回测
    results = engine.run_backtest(data, combined_strategy)
    
    print("\n回测结果:")
    print(f"总收益率: {results['summary']['total_return']:.2f}%")
    print(f"年化收益率: {results['summary']['annual_return']:.2f}%")
    print(f"夏普比率: {results['summary']['sharpe_ratio']:.2f}")
    print(f"交易次数: {results['trades']['total_trades']}")


def example_5_strategy_comparison():
    """示例5: 策略对比"""
    print("\n" + "="*60)
    print("示例5: 策略对比")
    print("="*60)
    
    data = generate_test_data(days=252)
    
    # 定义多个策略
    strategies = [
        ('MA(5,20)', MAStrategy(5, 20)),
        ('MA(10,30)', MAStrategy(10, 30)),
        ('RSI(14)', RSIStrategy(14)),
        ('MACD(12,26,9)', MACDStrategy(12, 26, 9)),
    ]
    
    results = []
    
    for name, strategy in strategies:
        engine = BacktestEngine(initial_capital=100000)
        result = engine.run_backtest(data, strategy)
        
        results.append({
            '策略': name,
            '总收益率': result['summary']['total_return'],
            '年化收益率': result['summary']['annual_return'],
            '最大回撤': result['summary']['max_drawdown'],
            '夏普比率': result['summary']['sharpe_ratio'],
            '交易次数': result['trades']['total_trades']
        })
    
    # 转换为DataFrame
    df = pd.DataFrame(results)
    
    print("\n策略对比结果:")
    print(df.to_string(index=False))
    
    # 找出最佳策略
    best_sharpe = df.loc[df['夏普比率'].idxmax()]
    print(f"\n夏普比率最高: {best_sharpe['策略']} ({best_sharpe['夏普比率']:.2f})")


def example_6_generate_report():
    """示例6: 生成回测报告"""
    print("\n" + "="*60)
    print("示例6: 生成回测报告")
    print("="*60)
    
    engine = BacktestEngine(initial_capital=100000)
    data = generate_test_data(days=252)
    strategy = MAStrategy(5, 20)
    
    # 运行回测
    results = engine.run_backtest(data, strategy)
    
    # 生成报告
    report = BacktestReport.generate_report(results, strategy.name)
    
    print(report)


def example_7_parameter_optimization():
    """示例7: 参数优化"""
    print("\n" + "="*60)
    print("示例7: 参数优化")
    print("="*60)
    
    data = generate_test_data(days=252)
    
    # 测试不同的MA参数组合
    short_periods = [5, 10, 15]
    long_periods = [20, 30, 40]
    
    results = []
    
    for short in short_periods:
        for long in long_periods:
            if short >= long:
                continue
            
            engine = BacktestEngine(initial_capital=100000)
            strategy = MAStrategy(short_period=short, long_period=long)
            result = engine.run_backtest(data, strategy)
            
            results.append({
                '短期均线': short,
                '长期均线': long,
                '总收益率': result['summary']['total_return'],
                '夏普比率': result['summary']['sharpe_ratio'],
                '最大回撤': result['summary']['max_drawdown']
            })
    
    df = pd.DataFrame(results)
    
    print("\n参数优化结果:")
    print(df.to_string(index=False))
    
    # 找出最优参数
    best_return = df.loc[df['总收益率'].idxmax()]
    best_sharpe = df.loc[df['夏普比率'].idxmax()]
    
    print(f"\n收益率最高参数: MA({best_return['短期均线']},{best_return['长期均线']})")
    print(f"  收益率: {best_return['总收益率']:.2f}%")
    print(f"\n夏普比率最高参数: MA({best_sharpe['短期均线']},{best_sharpe['长期均线']})")
    print(f"  夏普比率: {best_sharpe['夏普比率']:.2f}")


def example_8_risk_management():
    """示例8: 风险管理"""
    print("\n" + "="*60)
    print("示例8: 风险管理")
    print("="*60)
    
    from src.ai_inv.portfolio_optimizer import RiskManager
    
    # 创建风险管理器
    risk_manager = RiskManager(
        max_position_size=0.2,  # 最大单只股票仓位20%
        max_portfolio_risk=0.25  # 最大组合风险25%
    )
    
    # 计算仓位大小
    capital = 100000
    position_size = risk_manager.calculate_position_size(
        capital=capital,
        risk_per_trade=0.02,  # 每笔交易风险2%
        stop_loss_pct=0.05  # 止损5%
    )
    
    print(f"\n仓位计算:")
    print(f"总资金: HK${capital:,.0f}")
    print(f"单笔交易风险: 2%")
    print(f"止损比例: 5%")
    print(f"建议仓位: HK${position_size:,.0f} ({position_size/capital:.2%})")
    
    # 检查组合风险
    portfolio_value = 100000
    positions = {
        '6158.HK': 10000,
        '7200.HK': 20000,
        '^HSI': 30000
    }
    current_prices = {
        '6158.HK': 0.50,
        '7200.HK': 2.00,
        '^HSI': 28000.0
    }
    
    risk_check = risk_manager.check_risk(portfolio_value, positions, current_prices)
    
    print(f"\n组合风险检查:")
    print(f"组合价值: HK${portfolio_value:,.0f}")
    print(f"风险等级: {risk_check['risk_level'].upper()}")
    
    if risk_check['has_warnings']:
        print("\n风险警告:")
        for warning in risk_check['warnings']:
            print(f"  - {warning['message']}")
    else:
        print("\n未发现风险警告")
    
    # 生成止损价格
    entry_price = 100.0
    
    stop_loss_fixed = risk_manager.generate_stop_loss(
        entry_price=entry_price,
        method='fixed',
        params={'loss_pct': 0.05}
    )
    
    stop_loss_atr = risk_manager.generate_stop_loss(
        entry_price=entry_price,
        method='atr',
        params={'atr': 2.0, 'atr_multiplier': 2.0}
    )
    
    print(f"\n止损价格:")
    print(f"入场价: HK${entry_price:.2f}")
    print(f"固定止损 (5%): HK${stop_loss_fixed:.2f}")
    print(f"ATR止损 (2倍ATR): HK${stop_loss_atr:.2f}")


def example_9_portfolio_optimization():
    """示例9: 投资组合优化"""
    print("\n" + "="*60)
    print("示例9: 投资组合优化")
    print("="*60)
    
    from src.ai_inv.portfolio_optimizer import PortfolioOptimizer
    
    # 创建收益率数据
    np.random.seed(42)
    symbols = ['6158.HK', '7200.HK', '^HSI', '0005.HK', '0700.HK']
    
    # 生成模拟收益率数据
    returns_data = {}
    for symbol in symbols:
        returns_data[symbol] = np.random.normal(0.001, 0.02, 252)
    
    returns_df = pd.DataFrame(returns_data)
    returns_df.index = pd.date_range(start='2023-01-01', periods=252)
    
    # 创建优化器
    optimizer = PortfolioOptimizer(risk_free_rate=0.02)
    
    # 使用不同方法优化
    methods = ['equal_weight', 'sharpe', 'min_variance']
    
    results = []
    for method in methods:
        result = optimizer.optimize_portfolio(returns_df, method=method)
        
        weights_str = ', '.join([f"{s}: {w:.2%}" for s, w in result['weights'].items()])
        
        print(f"\n{method.upper()} 优化:")
        print(f"  预期年化收益: {result['expected_return']:.2%}")
        print(f"  年化波动率: {result['volatility']:.2%}")
        print(f"  夏普比率: {result['sharpe_ratio']:.2f}")
        print(f"  权重分配: {weights_str}")


def example_10_performance_analysis():
    """示例10: 性能分析"""
    print("\n" + "="*60)
    print("示例10: 性能分析")
    print("="*60)
    
    from src.ai_inv.portfolio_optimizer import PerformanceAnalyzer
    
    # 创建资金曲线
    np.random.seed(42)
    dates = pd.date_range(start='2023-01-01', periods=252, freq='D')
    portfolio_value = 100000 * (1 + np.cumsum(np.random.normal(0.0005, 0.01, 252)))
    
    equity_curve = pd.DataFrame({
        'portfolio_value': portfolio_value
    }, index=dates)
    
    # 分析性能
    analyzer = PerformanceAnalyzer()
    results = analyzer.analyze_performance(equity_curve)
    
    print("\n收益指标:")
    for key, value in results['return_metrics'].items():
        print(f"  {key}: {value}")
    
    print("\n风险指标:")
    for key, value in results['risk_metrics'].items():
        print(f"  {key}: {value}")
    
    print("\n分布指标:")
    for key, value in results['distribution_metrics'].items():
        print(f"  {key}: {value}")


def main():
    """运行所有示例"""
    print("\n" + "="*60)
    print("AI投资工具 - 回测引擎示例")
    print("="*60)
    
    examples = [
        ("基本回测", example_1_basic_backtest),
        ("RSI策略回测", example_2_rsi_strategy),
        ("MACD策略回测", example_3_macd_strategy),
        ("组合策略回测", example_4_combined_strategy),
        ("策略对比", example_5_strategy_comparison),
        ("生成回测报告", example_6_generate_report),
        ("参数优化", example_7_parameter_optimization),
        ("风险管理", example_8_risk_management),
        ("投资组合优化", example_9_portfolio_optimization),
        ("性能分析", example_10_performance_analysis),
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
