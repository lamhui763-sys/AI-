"""
Web仪表板模块
使用Streamlit创建交互式Web界面

特性:
- 实时股票数据展示
- 技术指标可视化
- 交互式图表
- AI分析结果展示
- 回测结果可视化
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, List, Optional, Any, Union
from datetime import datetime, timedelta
import sys
import os

# 添加src到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from src.ai_inv.data_fetcher import DataFetcher
from src.ai_inv.indicators import TechnicalIndicators
from src.ai_inv.technical_analyzer import TechnicalAnalyzer
from src.ai_inv.ai_analyzer import AIAnalyzer
from src.ai_inv.sentiment_analyzer import SentimentAnalyzer
from src.ai_inv.smart_advisor import SmartAdvisor
from src.ai_inv.backtester import BacktestEngine, MAStrategy, RSIStrategy, MACDStrategy
from src.ai_inv.excel_visualizer import ExcelVisualizer


def main():
    """主函数 - Streamlit应用"""
    
    # 页面配置
    st.set_page_config(
        page_title="AI投资分析工具",
        page_icon="📈",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # 页面选择
    st.sidebar.title("📈 AI投资分析工具")
    page = st.sidebar.radio(
        "选择功能",
        ["股票分析", "技术分析", "AI分析", "回测引擎", "投资组合", "新闻分析"]
    )
    
    # 根据选择显示不同页面
    if page == "股票分析":
        stock_analysis_page()
    elif page == "技术分析":
        technical_analysis_page()
    elif page == "AI分析":
        ai_analysis_page()
    elif page == "回测引擎":
        backtest_page()
    elif page == "投资组合":
        portfolio_page()
    elif page == "新闻分析":
        news_analysis_page()


def stock_analysis_page():
    """股票分析页面"""
    st.header("📊 股票分析")
    
    # 侧边栏配置
    st.sidebar.subheader("股票配置")
    
    # 股票代码输入
    default_symbols = ['^HSI', '6158.HK', '7200.HK']
    symbol_input = st.sidebar.text_input(
        "股票代码（多个用逗号分隔）",
        value="^HSI"
    )
    symbols = [s.strip() for s in symbol_input.split(',')]
    
    # 时间周期选择
    period = st.sidebar.selectbox(
        "时间周期",
        ['1mo', '3mo', '6mo', '1y', '2y', '5y'],
        index=2
    )
    
    # 分析按钮
    if st.sidebar.button("开始分析", type="primary"):
        with st.spinner("正在获取数据并分析..."):
            # 创建数据获取器
            fetcher = DataFetcher()
            
            # 创建分析器
            analyzer = TechnicalAnalyzer()
            
            # 分析每只股票
            results = []
            for symbol in symbols:
                try:
                    # 获取数据
                    data = fetcher.get_historical_data(symbol, period=period)
                    
                    if data is not None and not data.empty:
                        # 技术分析
                        indicators = analyzer.analyze_stock(symbol, period=period)
                        
                        # 获取交易信号
                        signal = analyzer.get_trading_signal(symbol)
                        
                        results.append({
                            'symbol': symbol,
                            'data': data,
                            'indicators': indicators,
                            'signal': signal,
                            'error': None
                        })
                    else:
                        results.append({
                            'symbol': symbol,
                            'data': None,
                            'indicators': None,
                            'signal': None,
                            'error': "无法获取数据"
                        })
                except Exception as e:
                    results.append({
                        'symbol': symbol,
                        'data': None,
                        'indicators': None,
                        'signal': None,
                        'error': str(e)
                    })
            
            # 保存到session state
            st.session_state.analysis_results = results
    
    # 显示分析结果
    if 'analysis_results' in st.session_state:
        results = st.session_state.analysis_results
        
        # 多股票标签页
        tab_names = [r['symbol'] for r in results]
        tabs = st.tabs(tab_names)
        
        for i, (tab, result) in enumerate(zip(tabs, results)):
            with tab:
                if result['error']:
                    st.error(f"❌ 错误: {result['error']}")
                else:
                    # 显示股票信息
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        latest_price = result['data']['Close'].iloc[-1]
                        st.metric("最新价格", f"HK${latest_price:.2f}")
                    
                    with col2:
                        if len(result['data']) >= 2:
                            prev_close = result['data']['Close'].iloc[-2]
                            change = latest_price - prev_close
                            change_pct = (change / prev_close) * 100
                            st.metric(
                                "日涨跌",
                                f"{change:+.2f}",
                                f"{change_pct:+.2f}%"
                            )
                    
                    with col3:
                        st.metric("交易信号", result['signal']['交易信号'])
                    
                    with col4:
                        st.metric("信号强度", result['signal']['强度'])
                    
                    st.divider()
                    
                    # 价格图表
                    st.subheader("价格走势")
                    plot_price_chart(result['data'], result['indicators'])
                    
                    # 技术指标图表
                    st.subheader("技术指标")
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        plot_rsi_chart(result['indicators'])
                    
                    with col2:
                        plot_macd_chart(result['indicators'])
                    
                    # 详细分析
                    with st.expander("📋 详细技术分析"):
                        display_technical_details(result['indicators'])


def technical_analysis_page():
    """技术分析页面"""
    st.header("🔬 技术分析")
    
    # 股票选择
    symbol = st.text_input("股票代码", value="^HSI")
    
    # 指标选择
    st.subheader("选择技术指标")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        show_sma = st.checkbox("移动平均线 (SMA)", value=True)
        show_rsi = st.checkbox("RSI", value=True)
    
    with col2:
        show_macd = st.checkbox("MACD", value=True)
        show_bollinger = st.checkbox("布林带", value=True)
    
    with col3:
        show_volume = st.checkbox("成交量", value=True)
        show_atr = st.checkbox("ATR", value=True)
    
    # 参数设置
    with st.expander("⚙️ 指标参数"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            sma_short = st.number_input("短期均线周期", value=5, min_value=1)
            sma_long = st.number_input("长期均线周期", value=20, min_value=1)
        
        with col2:
            rsi_period = st.number_input("RSI周期", value=14, min_value=1)
            macd_fast = st.number_input("MACD快线", value=12, min_value=1)
        
        with col3:
            macd_slow = st.number_input("MACD慢线", value=26, min_value=1)
            macd_signal = st.number_input("MACD信号线", value=9, min_value=1)
    
    # 分析按钮
    if st.button("生成分析", type="primary"):
        with st.spinner("正在计算技术指标..."):
            try:
                # 创建指标计算器
                indicators = TechnicalIndicators()
                
                # 获取数据
                fetcher = DataFetcher()
                data = fetcher.get_historical_data(symbol, period='1y')
                
                if data is not None and not data.empty:
                    # 计算指标
                    all_indicators = indicators.calculate_all_indicators(data)
                    
                    # 保存到session state
                    st.session_state.tech_data = data
                    st.session_state.tech_indicators = all_indicators
            except Exception as e:
                st.error(f"❌ 错误: {str(e)}")
    
    # 显示结果
    if 'tech_data' in st.session_state and 'tech_indicators' in st.session_state:
        data = st.session_state.tech_data
        indicators = st.session_state.tech_indicators
        
        # 根据选择显示图表
        if show_sma:
            st.subheader("移动平均线")
            plot_sma_chart(data, indicators)
        
        if show_rsi:
            st.subheader("RSI指标")
            plot_rsi_chart(indicators)
        
        if show_macd:
            st.subheader("MACD指标")
            plot_macd_chart(indicators)
        
        if show_bollinger:
            st.subheader("布林带")
            plot_bollinger_chart(data, indicators)
        
        if show_volume:
            st.subheader("成交量分析")
            plot_volume_chart(data)
        
        if show_atr:
            st.subheader("ATR (真实波幅)")
            plot_atr_chart(indicators)
        
        # 导出按钮
        st.divider()
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("导出为Excel"):
                visualizer = ExcelVisualizer()
                filepath = visualizer.generate_stock_report(
                    symbol,
                    data,
                    indicators
                )
                st.success(f"✅ 已导出到: {filepath}")


def ai_analysis_page():
    """AI分析页面"""
    st.header("🤖 AI分析")
    
    # 配置 AI API
    st.sidebar.subheader("AI 配置")
    ai_provider = st.sidebar.selectbox("AI 提供商", ["Gemini", "OpenAI"], index=0)
    
    if ai_provider == "Gemini":
        gemini_key = st.sidebar.text_input("Gemini API Key", type="password", value=os.getenv('GEMINI_API_KEY', ''))
        if gemini_key:
            os.environ['GEMINI_API_KEY'] = gemini_key
    else:
        openai_key = st.sidebar.text_input("OpenAI API Key", type="password", value=os.getenv('OPENAI_API_KEY', ''))
        if openai_key:
            os.environ['OPENAI_API_KEY'] = openai_key
    
    # 股票选择
    symbol = st.text_input("股票代码", value="^HSI")
    
    # 分析类型
    analysis_type = st.radio(
        "分析类型",
        ["基础AI分析", "情感分析", "智能顾问"]
    )
    
    # 分析按钮
    if st.button("开始AI分析", type="primary"):
        with st.spinner("AI正在分析中..."):
            try:
                if analysis_type == "基础AI分析":
                    # AI分析
                    ai_analyzer = AIAnalyzer()
                    tech_analyzer = TechnicalAnalyzer()
                    
                    # 获取技术分析
                    tech_data = tech_analyzer.analyze_stock(symbol, period='3mo')
                    signal = tech_analyzer.get_trading_signal(symbol)
                    
                    # 准备数据
                    analysis_data = {
                        '价格': {
                            '收盘价': tech_data['Close'].iloc[-1],
                            '涨跌幅': ((tech_data['Close'].iloc[-1] - tech_data['Close'].iloc[-2]) / 
                                     tech_data['Close'].iloc[-2] * 100) if len(tech_data) >= 2 else 0
                        },
                        '交易信号': signal['交易信号'],
                        '信号强度': signal['强度']
                    }
                    
                    # AI分析
                    ai_result = ai_analyzer.analyze_stock_with_ai(symbol, analysis_data)
                    
                    st.session_state.ai_result = ai_result
                    
                elif analysis_type == "情感分析":
                    # 情感分析
                    sentiment_analyzer = SentimentAnalyzer()
                    
                    # 示例文本
                    text = st.text_area(
                        "输入要分析的新闻或文本",
                        value="恆生指數今日上漲2%，市場情緒樂觀，投資者對經濟前景看好",
                        height=100
                    )
                    
                    result = sentiment_analyzer.analyze_text(text)
                    
                    st.session_state.sentiment_result = result
                    
                elif analysis_type == "智能顾问":
                    # 智能顾问
                    advisor = SmartAdvisor()
                    
                    # 综合分析
                    result = advisor.get_comprehensive_analysis(symbol)
                    
                    st.session_state.advisor_result = result
                    
            except Exception as e:
                st.error(f"❌ 错误: {str(e)}")
    
    # 显示AI分析结果
    if 'ai_result' in st.session_state:
        result = st.session_state.ai_result
        
        st.subheader("AI分析结果")
        
        # 建议
        col1, col2 = st.columns(2)
        with col1:
            st.metric("AI建议", result['recommendation'])
        with col2:
            st.metric("置信度", f"{result['confidence']:.1%}")
        
        st.divider()
        
        # 详细分析
        st.subheader("分析详情")
        st.markdown(result['analysis'])
    
    # 显示情感分析结果
    if 'sentiment_result' in st.session_state:
        result = st.session_state.sentiment_result
        
        st.subheader("情感分析结果")
        
        # 情感仪表盘
        col1, col2, col3 = st.columns(3)
        
        with col1:
            sentiment_emoji = "😊" if result['sentiment'] == 'positive' else "😔" if result['sentiment'] == 'negative' else "😐"
            st.metric("情感倾向", f"{sentiment_emoji} {result['sentiment'].upper()}")
        
        with col2:
            st.metric("情感分数", f"{result['score']:.2f}")
        
        with col3:
            st.metric("置信度", f"{result['confidence']:.1%}")
        
        st.divider()
        
        # 关键词
        if result['keywords']:
            st.subheader("关键词")
            keywords_str = " | ".join(result['keywords'])
            st.markdown(f"**{keywords_str}**")
    
    # 显示智能顾问结果
    if 'advisor_result' in st.session_state:
        result = st.session_state.advisor_result
        
        st.subheader("智能投资顾问")
        
        # 建议
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("投资建议", result['recommendation']['action'])
        
        with col2:
            st.metric("综合评分", f"{result['recommendation']['overall_score']:.1f}/10")
        
        with col3:
            st.metric("置信度", f"{result['recommendation']['confidence']:.1%}")
        
        st.divider()
        
        # 技术分析
        with st.expander("📊 技术面分析"):
            st.write(f"评分: {result['technical']['score']:.1f}/10")
            st.write(f"信号: {result['technical']['signal']}")
            st.write(f"趋势: {result['technical']['trend']}")
        
        # AI分析
        with st.expander("🤖 AI分析"):
            st.write(f"评分: {result['ai']['score']:.1f}/10")
            if 'recommendation' in result['ai']:
                st.write(f"建议: {result['ai']['recommendation']}")
        
        # 情感分析
        with st.expander("😊 情感分析"):
            st.write(f"评分: {result['sentiment']['score']:.1f}/10")
            st.write(f"情感: {result['sentiment']['overall']}")
        
        st.divider()
        
        # 投资计划
        if st.button("生成投资计划"):
            capital = st.number_input("投资金额", value=100000, min_value=1000)
            risk_tolerance = st.selectbox(
                "风险承受能力",
                ['low', 'medium', 'high']
            )
            
            plan = result.get('investment_plan', {})
            if not plan:
                advisor = SmartAdvisor()
                plan = advisor.get_investment_plan(
                    symbol,
                    capital=capital,
                    risk_tolerance=risk_tolerance
                )
            
            st.subheader("投资计划")
            st.json(plan)


def backtest_page():
    """回测页面"""
    st.header("⏱️ 回测引擎")
    
    # 侧边栏配置
    st.sidebar.subheader("回测配置")
    
    # 策略选择
    strategy_type = st.sidebar.selectbox(
        "选择策略",
        ["移动平均交叉", "RSI", "MACD", "组合策略"]
    )
    
    # 参数设置
    if strategy_type == "移动平均交叉":
        short_period = st.sidebar.number_input("短期均线", value=5, min_value=1)
        long_period = st.sidebar.number_input("长期均线", value=20, min_value=1)
        strategy = MAStrategy(short_period, long_period)
    elif strategy_type == "RSI":
        rsi_period = st.sidebar.number_input("RSI周期", value=14, min_value=1)
        oversold = st.sidebar.number_input("超卖线", value=30, min_value=1, max_value=50)
        overbought = st.sidebar.number_input("超买线", value=70, min_value=50, max_value=99)
        strategy = RSIStrategy(rsi_period, oversold, overbought)
    elif strategy_type == "MACD":
        fast_period = st.sidebar.number_input("快线周期", value=12, min_value=1)
        slow_period = st.sidebar.number_input("慢线周期", value=26, min_value=1)
        signal_period = st.sidebar.number_input("信号线周期", value=9, min_value=1)
        strategy = MACDStrategy(fast_period, slow_period, signal_period)
    else:
        # 组合策略
        strategy = MAStrategy(5, 20)  # 默认
    
    # 回测参数
    symbol = st.sidebar.text_input("股票代码", value="^HSI")
    initial_capital = st.sidebar.number_input("初始资金", value=100000, min_value=1000)
    commission = st.sidebar.number_input("手续费 (%)", value=0.1, min_value=0.0, format="%.2f") / 100
    
    # 回测按钮
    if st.sidebar.button("开始回测", type="primary"):
        with st.spinner("正在运行回测..."):
            try:
                # 创建回测引擎
                engine = BacktestEngine(
                    initial_capital=initial_capital,
                    commission=commission
                )
                
                # 获取数据
                fetcher = DataFetcher()
                data = fetcher.get_historical_data(symbol, period='2y')
                
                if data is not None and not data.empty:
                    # 运行回测
                    results = engine.run_backtest(data, strategy)
                    
                    # 保存到session state
                    st.session_state.backtest_results = results
                    st.session_state.backtest_symbol = symbol
                    st.session_state.backtest_strategy = strategy_type
                    
            except Exception as e:
                st.error(f"❌ 错误: {str(e)}")
    
    # 显示回测结果
    if 'backtest_results' in st.session_state:
        results = st.session_state.backtest_results
        symbol = st.session_state.backtest_symbol
        strategy_type = st.session_state.backtest_strategy
        
        # 标题
        st.subheader(f"{symbol} - {strategy_type}策略回测结果")
        
        # 关键指标
        col1, col2, col3, col4 = st.columns(4)
        
        summary = results['summary']
        
        with col1:
            st.metric("总收益", f"{summary['total_return']:.2f}%")
        
        with col2:
            st.metric("年化收益", f"{summary['annual_return']:.2f}%")
        
        with col3:
            st.metric("夏普比率", f"{summary['sharpe_ratio']:.2f}")
        
        with col4:
            st.metric("最大回撤", f"{summary['max_drawdown']:.2f}%")
        
        st.divider()
        
        # 资金曲线
        st.subheader("资金曲线")
        plot_equity_curve(results['equity_curve'])
        
        # 交易统计
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("交易次数", summary['total_trades'])
            st.metric("盈利交易", summary['winning_trades'])
            st.metric("亏损交易", summary['losing_trades'])
        
        with col2:
            st.metric("胜率", f"{summary['win_rate']:.2f}%")
            st.metric("平均盈利", f"{summary['avg_win']:.2f}")
            st.metric("平均亏损", f"{summary['avg_loss']:.2f}")
        
        st.divider()
        
        # 交易记录
        st.subheader("交易记录")
        if 'trades' in results and not results['trades'].empty:
            st.dataframe(
                results['trades'].style.format({
                    'entry_price': '${:.2f}',
                    'exit_price': '${:.2f}',
                    'pnl': '${:.2f}',
                    'pnl_pct': '{:.2f}%'
                }),
                use_container_width=True
            )
        
        # 导出按钮
        st.divider()
        if st.button("导出回测报告"):
            visualizer = ExcelVisualizer()
            filepath = visualizer.generate_backtest_report(
                results,
                strategy_type
            )
            st.success(f"✅ 已导出到: {filepath}")


def portfolio_page():
    """投资组合页面"""
    st.header("💼 投资组合分析")
    
    # 输入持仓
    st.subheader("输入持仓")
    
    # 添加持仓
    with st.form("add_holding"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            symbol = st.text_input("股票代码", value="6158.HK")
        
        with col2:
            shares = st.number_input("持股数", value=1000, min_value=1)
        
        with col3:
            avg_price = st.number_input("平均成本", value=0.50, min_value=0.01, step=0.01)
        
        submitted = st.form_submit_button("添加持仓")
        
        if submitted:
            if 'holdings' not in st.session_state:
                st.session_state.holdings = []
            
            st.session_state.holdings.append({
                'symbol': symbol,
                'shares': shares,
                'avg_price': avg_price
            })
    
    # 显示持仓
    if 'holdings' in st.session_state and st.session_state.holdings:
        st.subheader("当前持仓")
        
        # 获取最新价格
        fetcher = DataFetcher()
        
        holdings_data = []
        for holding in st.session_state.holdings:
            try:
                data = fetcher.get_historical_data(holding['symbol'], period='5d')
                if data is not None and not data.empty:
                    current_price = data['Close'].iloc[-1]
                else:
                    current_price = holding['avg_price']
            except:
                current_price = holding['avg_price']
            
            market_value = current_price * holding['shares']
            cost_basis = holding['avg_price'] * holding['shares']
            pnl = market_value - cost_basis
            pnl_pct = (pnl / cost_basis) * 100
            
            holdings_data.append({
                '代码': holding['symbol'],
                '持股数': holding['shares'],
                '平均成本': f"${holding['avg_price']:.2f}",
                '当前价格': f"${current_price:.2f}",
                '市值': f"${market_value:,.2f}",
                '成本': f"${cost_basis:,.2f}",
                '盈亏': f"${pnl:,.2f}",
                '盈亏%': f"{pnl_pct:.2f}%"
            })
        
        df = pd.DataFrame(holdings_data)
        st.dataframe(df, use_container_width=True)
        
        # 组合统计
        total_market_value = sum([float(h['市值'].replace('$', '').replace(',', '')) for h in holdings_data])
        total_cost = sum([float(h['成本'].replace('$', '').replace(',', '')) for h in holdings_data])
        total_pnl = total_market_value - total_cost
        total_pnl_pct = (total_pnl / total_cost) * 100
        
        st.divider()
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("组合总值", f"${total_market_value:,.2f}")
        
        with col2:
            st.metric("总盈亏", f"${total_pnl:,.2f}")
        
        with col3:
            st.metric("收益率", f"{total_pnl_pct:.2f}%")
        
        # 持仓分布饼图
        if holdings_data:
            st.subheader("持仓分布")
            plot_portfolio_pie(holdings_data)
    
    # 清空按钮
    if st.button("清空持仓"):
        st.session_state.holdings = []
        st.rerun()


def news_analysis_page():
    """新闻分析页面"""
    st.header("📰 新闻情感分析")
    
    # 输入新闻
    st.subheader("输入新闻")
    
    news_input = st.text_area(
        "输入新闻内容",
        value="恆生指數今日上漲2%，市場情緒樂觀，科技股表現突出，投資者對經濟前景看好",
        height=150
    )
    
    # 分析按钮
    if st.button("分析情感", type="primary"):
        try:
            sentiment_analyzer = SentimentAnalyzer()
            result = sentiment_analyzer.analyze_text(news_input)
            
            # 显示结果
            col1, col2, col3 = st.columns(3)
            
            with col1:
                sentiment_emoji = "😊" if result['sentiment'] == 'positive' else "😔" if result['sentiment'] == 'negative' else "😐"
                st.metric("情感倾向", f"{sentiment_emoji} {result['sentiment'].upper()}")
            
            with col2:
                st.metric("情感分数", f"{result['score']:.2f}")
            
            with col3:
                st.metric("置信度", f"{result['confidence']:.1%}")
            
            st.divider()
            
            # 详细分析
            st.subheader("分析详情")
            
            if result['keywords']:
                st.write("**关键词:**")
                keywords_str = " | ".join(result['keywords'])
                st.markdown(f"**{keywords_str}**")
            
            st.write("\n**情感说明:**")
            if result['sentiment'] == 'positive':
                st.success("新闻内容整体偏向正面，市场情绪乐观")
            elif result['sentiment'] == 'negative':
                st.error("新闻内容整体偏向负面，市场情绪悲观")
            else:
                st.info("新闻内容中性，市场情绪平稳")
            
            st.write(f"\n**情感分数:** {result['score']:.2f} (范围: -1.0 到 1.0)")
            st.write(f"**置信度:** {result['confidence']:.1%}")
            
        except Exception as e:
            st.error(f"❌ 错误: {str(e)}")


# 图表绘制函数

def plot_price_chart(data: pd.DataFrame, indicators: Dict[str, Any]):
    """绘制价格图表"""
    fig = go.Figure()
    
    # K线图
    fig.add_trace(go.Candlestick(
        x=data.index,
        open=data['Open'],
        high=data['High'],
        low=data['Low'],
        close=data['Close'],
        name='价格'
    ))
    
    # 均线
    if 'SMA' in indicators:
        for period, sma in indicators['SMA'].items():
            fig.add_trace(go.Scatter(
                x=data.index,
                y=sma,
                mode='lines',
                name=f'SMA{period}',
                line=dict(width=1)
            ))
    
    fig.update_layout(
        title='价格走势',
        xaxis_title='日期',
        yaxis_title='价格',
        xaxis_rangeslider_visible=False,
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)


def plot_rsi_chart(indicators: Union[Dict[str, Any], pd.DataFrame]):
    """绘制RSI图表"""
    if isinstance(indicators, pd.DataFrame):
        if 'RSI_14' not in indicators.columns:
            return
        rsi_data = indicators['RSI_14']
    else:
        if 'RSI' not in indicators:
            return
        rsi_data = indicators['RSI']
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=rsi_data.index,
        y=rsi_data,
        mode='lines',
        name='RSI',
        line=dict(color='purple')
    ))
    
    # 添加超买超卖线
    fig.add_hline(y=70, line_dash="dash", line_color="red", annotation_text="超买")
    fig.add_hline(y=30, line_dash="dash", line_color="green", annotation_text="超卖")
    
    fig.update_layout(
        title='RSI指标',
        xaxis_title='日期',
        yaxis_title='RSI',
        height=300
    )
    
    st.plotly_chart(fig, use_container_width=True)


def plot_macd_chart(indicators: Union[Dict[str, Any], pd.DataFrame]):
    """绘制MACD图表"""
    if isinstance(indicators, pd.DataFrame):
        if 'MACD' not in indicators.columns:
            return
        macd_line = indicators['MACD']
        signal_line = indicators['MACD_Signal']
        histogram = indicators['MACD_Histogram']
    else:
        if 'MACD' not in indicators:
            return
        macd = indicators['MACD']
        macd_line = macd['macd']
        signal_line = macd['signal']
        histogram = macd['histogram']
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=macd_line.index,
        y=macd_line,
        mode='lines',
        name='MACD',
        line=dict(color='blue')
    ))
    
    fig.add_trace(go.Scatter(
        x=signal_line.index,
        y=signal_line,
        mode='lines',
        name='Signal',
        line=dict(color='orange')
    ))
    
    fig.add_trace(go.Bar(
        x=histogram.index,
        y=histogram,
        name='Histogram'
    ))
    
    fig.update_layout(
        title='MACD指标',
        xaxis_title='日期',
        yaxis_title='数值',
        height=300
    )
    
    st.plotly_chart(fig, use_container_width=True)


def plot_bollinger_chart(data: pd.DataFrame, indicators: Dict[str, Any]):
    """绘制布林带图表"""
    if 'Bollinger_Bands' not in indicators:
        return
    
    bb = indicators['Bollinger_Bands']
    
    fig = go.Figure()
    
    # 价格
    fig.add_trace(go.Scatter(
        x=data.index,
        y=data['Close'],
        mode='lines',
        name='收盘价',
        line=dict(color='blue')
    ))
    
    # 布林带
    fig.add_trace(go.Scatter(
        x=data.index,
        y=bb['upper'],
        mode='lines',
        name='上轨',
        line=dict(color='gray', dash='dash')
    ))
    
    fig.add_trace(go.Scatter(
        x=data.index,
        y=bb['middle'],
        mode='lines',
        name='中轨',
        line=dict(color='orange')
    ))
    
    fig.add_trace(go.Scatter(
        x=data.index,
        y=bb['lower'],
        mode='lines',
        name='下轨',
        line=dict(color='gray', dash='dash')
    ))
    
    fig.update_layout(
        title='布林带',
        xaxis_title='日期',
        yaxis_title='价格',
        height=300
    )
    
    st.plotly_chart(fig, use_container_width=True)


def plot_sma_chart(data: pd.DataFrame, indicators: Dict[str, Any]):
    """绘制均线图表"""
    fig = go.Figure()
    
    # 价格
    fig.add_trace(go.Scatter(
        x=data.index,
        y=data['Close'],
        mode='lines',
        name='收盘价',
        opacity=0.5
    ))
    
    # 均线
    if 'SMA' in indicators:
        colors = ['blue', 'orange', 'green', 'red', 'purple']
        for i, (period, sma) in enumerate(indicators['SMA'].items()):
            fig.add_trace(go.Scatter(
                x=data.index,
                y=sma,
                mode='lines',
                name=f'SMA{period}',
                line=dict(color=colors[i % len(colors)])
            ))
    
    fig.update_layout(
        title='移动平均线',
        xaxis_title='日期',
        yaxis_title='价格',
        height=300
    )
    
    st.plotly_chart(fig, use_container_width=True)


def plot_volume_chart(data: pd.DataFrame):
    """绘制成交量图表"""
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=data.index,
        y=data['Volume'],
        name='成交量'
    ))
    
    fig.update_layout(
        title='成交量',
        xaxis_title='日期',
        yaxis_title='成交量',
        height=300
    )
    
    st.plotly_chart(fig, use_container_width=True)


def plot_atr_chart(indicators: Dict[str, Any]):
    """绘制ATR图表"""
    if 'ATR' not in indicators:
        return
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=indicators['ATR'].index,
        y=indicators['ATR'],
        mode='lines',
        name='ATR',
        line=dict(color='purple')
    ))
    
    fig.update_layout(
        title='ATR (真实波幅)',
        xaxis_title='日期',
        yaxis_title='ATR',
        height=300
    )
    
    st.plotly_chart(fig, use_container_width=True)


def plot_equity_curve(equity_curve: pd.DataFrame):
    """绘制资金曲线"""
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=equity_curve.index,
        y=equity_curve['equity'],
        mode='lines',
        name='资金曲线',
        line=dict(color='blue', width=2)
    ))
    
    fig.update_layout(
        title='资金曲线',
        xaxis_title='日期',
        yaxis_title='资金 (HK$)',
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)


def plot_portfolio_pie(holdings_data: List[Dict]):
    """绘制持仓分布饼图"""
    labels = [h['代码'] for h in holdings_data]
    values = [float(h['市值'].replace('$', '').replace(',', '')) for h in holdings_data]
    
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.3
    )])
    
    fig.update_layout(
        title='持仓分布',
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)


def display_technical_details(indicators: Dict[str, Any]):
    """显示技术指标详情"""
    # 创建详情表格
    details = []
    
    # 最新指标值
    if 'RSI' in indicators:
        latest_rsi = indicators['RSI'].iloc[-1]
        rsi_status = '超买' if latest_rsi > 70 else '超卖' if latest_rsi < 30 else '中性'
        details.append({
            '指标': 'RSI (14)',
            '最新值': f"{latest_rsi:.2f}",
            '状态': rsi_status
        })
    
    if 'MACD' in indicators:
        macd = indicators['MACD']['macd'].iloc[-1]
        signal = indicators['MACD']['signal'].iloc[-1]
        macd_status = '看涨' if macd > signal else '看跌'
        details.append({
            '指标': 'MACD',
            '最新值': f"{macd:.2f}",
            '状态': macd_status
        })
    
    if 'SMA' in indicators:
        sma5 = indicators['SMA'].get('SMA_5', pd.Series([np.nan])).iloc[-1]
        sma20 = indicators['SMA'].get('SMA_20', pd.Series([np.nan])).iloc[-1]
        if not pd.isna(sma5) and not pd.isna(sma20):
            trend = '上升' if sma5 > sma20 else '下降'
            details.append({
                '指标': '趋势 (5/20均线)',
                '最新值': f"{sma5:.2f} / {sma20:.2f}",
                '状态': trend
            })
    
    if details:
        df = pd.DataFrame(details)
        st.dataframe(df, use_container_width=True)


if __name__ == "__main__":
    main()
