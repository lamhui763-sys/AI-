"""
技术分析示例
展示如何使用技术分析模块
"""

import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.ai_inv.technical_analyzer import TechnicalAnalyzer


def example_1_basic_analysis():
    """示例1: 基本技术分析"""
    print("\n" + "="*60)
    print("示例1: 基本技术分析")
    print("="*60)
    
    # 创建分析器
    analyzer = TechnicalAnalyzer()
    
    # 分析单只股票
    symbol = '^HSI'  # 恒生指数
    data = analyzer.analyze_stock(symbol, period='1y')
    
    if not data.empty:
        # 显示最新数据
        latest = data.iloc[-1]
        print(f"\n股票: {symbol}")
        print(f"最新收盘价: {latest['Close']:.2f}")
        print(f"RSI(14): {latest.get('RSI_14', 'N/A'):.2f}")
        print(f"MACD: {latest.get('MACD', 'N/A'):.4f}")
        print(f"交易信号: {latest.get('Signal', 'N/A')}")
        print(f"信号强度: {int(latest.get('Signal_Strength', 0))}/5")
        
        # 生成报告
        report = analyzer.generate_report(symbol)
        print(report)


def example_2_multiple_stocks():
    """示例2: 分析多只股票"""
    print("\n" + "="*60)
    print("示例2: 分析多只股票")
    print("="*60)
    
    analyzer = TechnicalAnalyzer()
    
    # 分析多只股票
    symbols = ['^HSI', '6158.HK', '7200.HK']
    results = analyzer.analyze_watchlist(symbols, period='6m')
    
    print(f"\n成功分析 {len(results)} 只股票")
    
    for symbol, data in results.items():
        latest = data.iloc[-1]
        print(f"\n{symbol}:")
        print(f"  收盘价: {latest['Close']:.2f}")
        print(f"  信号: {latest.get('Signal', 'N/A')}")
        print(f"  强度: {int(latest.get('Signal_Strength', 0))}/5")


def example_3_trading_signals():
    """示例3: 获取交易信号"""
    print("\n" + "="*60)
    print("示例3: 获取交易信号")
    print("="*60)
    
    analyzer = TechnicalAnalyzer()
    
    # 获取恒生指数的交易信号
    signal = analyzer.get_trading_signal('^HSI')
    
    print("\n恒生指数 (^HSI) 技术信号:")
    print(f"\n【价格信息】")
    for key, value in signal.get('价格', {}).items():
        print(f"  {key}: {value}")
    
    print(f"\n【趋势指标】")
    for key, value in signal.get('趋势指标', {}).items():
        print(f"  {key}: {value}")
    
    print(f"\n【动量指标】")
    for key, value in signal.get('动量指标', {}).items():
        print(f"  {key}: {value}")
    
    print(f"\n【交易信号】")
    print(f"  信号: {signal.get('交易信号', 'N/A')}")
    print(f"  强度: {signal.get('信号强度', 0)}/5")


def example_4_compare_stocks():
    """示例4: 比较多只股票"""
    print("\n" + "="*60)
    print("示例4: 比较多只股票")
    print("="*60)
    
    analyzer = TechnicalAnalyzer()
    
    # 比较多只股票
    symbols = ['^HSI', '6158.HK', '7200.HK']
    comparison = analyzer.compare_stocks(symbols)
    
    print("\n股票技术指标对比:")
    print(comparison.to_string(index=False))


def example_5_find_opportunities():
    """示例5: 寻找交易机会"""
    print("\n" + "="*60)
    print("示例5: 寻找交易机会")
    print("="*60)
    
    analyzer = TechnicalAnalyzer()
    
    # 寻找买入机会
    symbols = ['^HSI', '6158.HK', '7200.HK']
    opportunities = analyzer.find_opportunities(symbols, signal_type='BUY', min_strength=2)
    
    print(f"\n找到 {len(opportunities)} 个买入机会:\n")
    
    for opp in opportunities:
        print(f"股票代码: {opp['股票代码']}")
        print(f"  信号: {opp['信号']}")
        print(f"  强度: {opp['强度']}/5")
        print(f"  收盘价: {opp['收盘价']:.2f}")
        print(f"  RSI: {opp['RSI']:.2f}")
        print(f"  MACD: {opp['MACD']:.4f}")
        print(f"  分析时间: {opp['分析时间']}\n")


def example_6_trend_analysis():
    """示例6: 趋势分析"""
    print("\n" + "="*60)
    print("示例6: 趋势分析")
    print("="*60)
    
    analyzer = TechnicalAnalyzer()
    
    # 分析恒生指数趋势
    trend = analyzer.get_trend_analysis('^HSI', period='1y')
    
    print("\n恒生指数 (^HSI) 趋势分析:")
    for key, value in trend.items():
        print(f"  {key}: {value}")


def example_7_export_analysis():
    """示例7: 导出分析结果"""
    print("\n" + "="*60)
    print("示例7: 导出分析结果")
    print("="*60)
    
    analyzer = TechnicalAnalyzer()
    
    # 导出Excel
    symbol = '^HSI'
    filepath = 'hsi_technical_analysis.xlsx'
    
    success = analyzer.export_analysis(
        symbol=symbol,
        filepath=filepath,
        period='1y',
        format='excel'
    )
    
    if success:
        print(f"\n成功导出技术分析结果到: {filepath}")
        print("文件包含以下技术指标:")
        print("  - 趋势指标: SMA, EMA, 布林带")
        print("  - 动量指标: RSI, MACD, 随机震荡, 威廉指标")
        print("  - 成交量指标: OBV, 成交量MA")
        print("  - 波动率指标: ATR, 肯特纳通道")
        print("  - 交易信号")
    else:
        print("\n导出失败")


def example_8_specific_indicators():
    """示例8: 计算特定指标"""
    print("\n" + "="*60)
    print("示例8: 计算特定指标")
    print("="*60)
    
    from src.ai_inv.indicators import TechnicalIndicators
    
    ti = TechnicalIndicators()
    
    # 获取数据
    analyzer = TechnicalAnalyzer()
    data = analyzer.analyze_stock('^HSI', period='1y')
    
    # 只计算指定指标
    indicators_list = ['sma20', 'sma50', 'rsi', 'macd']
    print(f"\n计算特定指标: {', '.join(indicators_list)}")
    
    latest = data.iloc[-1]
    print(f"\n最新数据 ({data.index[-1].date()}):")
    print(f"  收盘价: {latest['Close']:.2f}")
    print(f"  SMA20: {latest['SMA_20']:.2f}")
    print(f"  SMA50: {latest['SMA_50']:.2f}")
    print(f"  RSI14: {latest['RSI_14']:.2f}")
    print(f"  MACD: {latest['MACD']:.4f}")
    print(f"  MACD信号线: {latest['MACD_Signal']:.4f}")


def main():
    """运行所有示例"""
    print("\n" + "="*60)
    print("AI投资工具 - 技术分析示例")
    print("="*60)
    
    examples = [
        ("基本技术分析", example_1_basic_analysis),
        ("分析多只股票", example_2_multiple_stocks),
        ("获取交易信号", example_3_trading_signals),
        ("比较多只股票", example_4_compare_stocks),
        ("寻找交易机会", example_5_find_opportunities),
        ("趋势分析", example_6_trend_analysis),
        ("导出分析结果", example_7_export_analysis),
        ("计算特定指标", example_8_specific_indicators),
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
        print("请确保已安装所需的依赖包")
        import traceback
        traceback.print_exc()
    
    print("\n" + "="*60)
    print("所有示例运行完成!")
    print("="*60)


if __name__ == '__main__':
    main()
