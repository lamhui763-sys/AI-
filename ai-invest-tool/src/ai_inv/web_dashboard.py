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
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../'))

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
    
    st.sidebar.subheader("股票配置")
    symbol_input = st.sidebar.text_input(
        "股票代码（多个用逗号分隔）",
        value="^HSI"
    )
    symbols = [s.strip() for s in symbol_input.split(',')]
    
    period = st.sidebar.selectbox(
        "时间周期",
        ['1mo', '3mo', '6mo', '1y', '2y', '5y'],
        index=2
    )
    
    if st.sidebar.button("开始分析", type="primary"):
        with st.spinner("正在获取数据并分析..."):
            fetcher = DataFetcher()
            analyzer = TechnicalAnalyzer()
            results = []
            for symbol in symbols:
                try:
                    data = fetcher.get_historical_data(symbol, period=period)
                    if data is not None and not data.empty:
                        indicators = analyzer.analyze_stock(symbol, period=period)
                        signal = analyzer.get_trading_signal(symbol)
                        results.append({
                            'symbol': symbol, 'data': data, 'indicators': indicators,
                            'signal': signal, 'error': None
                        })
                    else:
                        results.append({'symbol': symbol, 'data': None, 'indicators': None, 'signal': None, 'error': "无法获取数据"})
                except Exception as e:
                    results.append({'symbol': symbol, 'data': None, 'indicators': None, 'signal': None, 'error': str(e)})
            st.session_state.analysis_results = results
    
    if 'analysis_results' in st.session_state:
        results = st.session_state.analysis_results
        tab_names = [r['symbol'] for r in results]
        tabs = st.tabs(tab_names)
        
        for i, (tab, result) in enumerate(zip(tabs, results)):
            with tab:
                if result['error']:
                    st.error(f"❌ 错误: {result['error']}")
                else:
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        latest_price = result['data']['Close'].iloc[-1]
                        st.metric("最新价格", f"HK${latest_price:.2f}")
                    with col2:
                        if len(result['data']) >= 2:
                            prev_close = result['data']['Close'].iloc[-2]
                            change = latest_price - prev_close
                            change_pct = (change / prev_close) * 100 if prev_close != 0 else 0
                            st.metric("日涨跌", f"{change:+.2f}", f"{change_pct:+.2f}%")
                    with col3:
                        st.metric("交易信号", result['signal']['交易信号'])
                    with col4:
                        st.metric("信号强度", result['signal']['强度'])
                    
                    st.divider()
                    st.subheader("价格走势")
                    plot_price_chart(result['data'], result['indicators'])
                    st.subheader("技术指标")
                    c1, c2 = st.columns(2)
                    with c1:
                        plot_rsi_chart(result['indicators'])
                    with c2:
                        plot_macd_chart(result['indicators'])
                    with st.expander("📋 详细技术分析"):
                        display_technical_details(result['indicators'])

def technical_analysis_page():
    """技术分析页面"""
    st.header("🔬 技术分析")
    symbol = st.text_input("股票代码", value="^HSI")
    st.subheader("选择技术指标")
    
    c1, c2, c3 = st.columns(3)
    with c1:
        show_sma = st.checkbox("移动平均线 (SMA)", value=True)
        show_rsi = st.checkbox("RSI", value=True)
    with c2:
        show_macd = st.checkbox("MACD", value=True)
        show_bollinger = st.checkbox("布林带", value=True)
    with c3:
        show_volume = st.checkbox("成交量", value=True)
        show_atr = st.checkbox("ATR", value=True)
        
    if st.button("生成分析", type="primary"):
        with st.spinner("正在计算技术指标..."):
            try:
                fetcher = DataFetcher()
                data = fetcher.get_historical_data(symbol, period='1y')
                if data is not None and not data.empty:
                    indicators = TechnicalIndicators()
                    all_indicators = indicators.calculate_all_indicators(data)
                    st.session_state.tech_data = data
                    st.session_state.tech_indicators = all_indicators
            except Exception as e:
                st.error(f"❌ 错误: {str(e)}")
    
    if 'tech_data' in st.session_state and 'tech_indicators' in st.session_state:
        data = st.session_state.tech_data
        indicators = st.session_state.tech_indicators
        if show_sma: plot_sma_chart(data, indicators)
        if show_rsi: plot_rsi_chart(indicators)
        if show_macd: plot_macd_chart(indicators)
        if show_bollinger: plot_bollinger_chart(data, indicators)
        if show_volume: plot_volume_chart(data)
        if show_atr: plot_atr_chart(indicators)

def ai_analysis_page():
    """AI分析页面"""
    st.header("🤖 AI分析")
    st.sidebar.subheader("AI 配置")
    
    api_key_configured = False
    try:
        if 'GEMINI_API_KEY' in st.secrets and st.secrets['GEMINI_API_KEY']:
            os.environ['GEMINI_API_KEY'] = st.secrets['GEMINI_API_KEY']
            api_key_configured = True
    except Exception:
        if os.getenv('GEMINI_API_KEY'):
            api_key_configured = True

    if not api_key_configured:
        st.warning("请在 Streamlit Cloud 的 Secrets 中或本地环境变量中设置 GEMINI_API_KEY。")
        st.info("💡 如何设置 (Cloud): 进入应用的 'Settings' -> 'Secrets'，添加名为 `GEMINI_API_KEY` 的新密钥。")
        st.stop()

    symbol = st.text_input("股票代码", value="^HSI")
    analysis_type = st.radio("分析类型", ["基础AI分析", "智能顾问"])

    if st.button("开始AI分析", type="primary"):
        for key in ['ai_result', 'advisor_result']: 
            if key in st.session_state: del st.session_state[key]

        with st.spinner("AI正在分析中..."):
            try:
                if analysis_type == "基础AI分析":
                    analyzer = AIAnalyzer()
                    result = analyzer.analyze_stock_with_ai(symbol)
                    st.session_state.ai_result = result
                elif analysis_type == "智能顾问":
                    advisor = SmartAdvisor()
                    result = advisor.get_comprehensive_analysis(symbol)
                    st.session_state.advisor_result = result
            except Exception as e:
                st.error(f"❌ 分析时发生错误: {e}")

    if 'ai_result' in st.session_state:
        result = st.session_state.ai_result
        st.subheader("AI分析结果")
        st.metric("AI建议", result.get('recommendation', 'N/A'))
        st.markdown(result.get('analysis', '分析内容不可用。'))

    if 'advisor_result' in st.session_state:
        result = st.session_state.advisor_result
        st.subheader("智能投资顾问")
        if result.get("error"):
            st.error(f"❌ 分析失败: {result['error'] }")
        else:
            rec = result['recommendation']
            c1, c2, c3 = st.columns(3)
            c1.metric("投资建议", rec['action'])
            c2.metric("综合评分", f"{rec['overall_score']:.1f}/10")
            c3.metric("置信度", f"{rec['confidence']:.1%}")
            with st.expander("📊 技术面分析", expanded=True):
                tech = result['technical']
                st.write(f"评分: {tech['score']}/10 | 信号: {tech['signal']} | 趋势: {tech['trend']}")
            with st.expander("🤖 AI分析", expanded=True):
                ai = result['ai']
                st.write(f"评分: {ai['score']}/10 | 建议: {ai.get('recommendation', 'N/A')}")
            with st.expander("😊 情感分析", expanded=True):
                sent = result['sentiment']
                st.write(f"评分: {sent['score']}/10 | 情感: {sent['overall']}")

def backtest_page():
    """回测页面"""
    st.header("⏱️ 回测引擎")
    st.sidebar.subheader("回测配置")
    strategy_type = st.sidebar.selectbox("选择策略", ["移动平均交叉", "RSI", "MACD"])

    if strategy_type == "移动平均交叉":
        p1 = st.sidebar.number_input("短期均线", value=5, min_value=1)
        p2 = st.sidebar.number_input("长期均线", value=20, min_value=1)
        strategy = MAStrategy(p1, p2)
    elif strategy_type == "RSI":
        p1 = st.sidebar.number_input("RSI周期", value=14, min_value=1)
        p2 = st.sidebar.number_input("超卖线", value=30, min_value=1, max_value=50)
        p3 = st.sidebar.number_input("超买线", value=70, min_value=50, max_value=99)
        strategy = RSIStrategy(p1, p2, p3)
    else: # MACD
        p1 = st.sidebar.number_input("快线周期", value=12, min_value=1)
        p2 = st.sidebar.number_input("慢线周期", value=26, min_value=1)
        p3 = st.sidebar.number_input("信号线周期", value=9, min_value=1)
        strategy = MACDStrategy(p1, p2, p3)

    symbol = st.sidebar.text_input("回测股票代码", value="^HSI")
    capital = st.sidebar.number_input("初始资金", value=100000, min_value=1000)
    commission = st.sidebar.number_input("手续费 (%)", value=0.1, min_value=0.0, format="%.2f") / 100

    if st.sidebar.button("开始回测", type="primary"):
        with st.spinner("正在运行回测..."):
            try:
                engine = BacktestEngine(initial_capital=capital, commission=commission)
                fetcher = DataFetcher()
                data = fetcher.get_historical_data(symbol, period='2y')
                if data is not None and not data.empty:
                    results = engine.run_backtest(data, strategy)
                    st.session_state.backtest_results = results
            except Exception as e:
                st.error(f"❌ 错误: {str(e)}")

    if 'backtest_results' in st.session_state:
        res = st.session_state.backtest_results
        st.subheader(f"{symbol} - {strategy_type}策略回测结果")
        summary = res['summary']
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("总收益", f"{summary['total_return']:.2f}%")
        c2.metric("年化收益", f"{summary['annual_return']:.2f}%")
        c3.metric("夏普比率", f"{summary['sharpe_ratio']:.2f}")
        c4.metric("最大回撤", f"{summary['max_drawdown']:.2f}%")
        st.subheader("资金曲线")
        plot_equity_curve(res['equity_curve'])
        st.subheader("交易统计")
        c1, c2 = st.columns(2)
        c1.metric("交易次数", summary['total_trades'])
        c1.metric("盈利交易", summary['winning_trades'])
        c1.metric("亏损交易", summary['losing_trades'])
        c2.metric("胜率", f"{summary['win_rate']:.2f}%")
        c2.metric("平均盈利", f"{summary['avg_win']:.2f}")
        c2.metric("平均亏损", f"{summary['avg_loss']:.2f}")
        with st.expander("交易记录"):
            st.dataframe(res['trades'])

def portfolio_page():
    """投资组合页面"""
    st.header("💼 投资组合分析")
    st.subheader("输入持仓")

    if 'holdings' not in st.session_state: st.session_state.holdings = []

    with st.form("add_holding"):
        c1, c2, c3 = st.columns(3)
        symbol = c1.text_input("股票代码", value="6158.HK")
        shares = c2.number_input("持股数", value=1000, min_value=1)
        avg_price = c3.number_input("平均成本", value=0.50, min_value=0.01, step=0.01)
        if st.form_submit_button("添加持仓"):
            st.session_state.holdings.append({'symbol': symbol, 'shares': shares, 'avg_price': avg_price})
            st.rerun()

    if st.session_state.holdings:
        st.subheader("当前持仓")
        fetcher = DataFetcher()
        data = []
        for h in st.session_state.holdings:
            price_data = fetcher.get_historical_data(h['symbol'], period='5d')
            price = price_data['Close'].iloc[-1] if price_data is not None else h['avg_price']
            market_val = price * h['shares']
            cost = h['avg_price'] * h['shares']
            pnl = market_val - cost
            pnl_pct = (pnl / cost) * 100 if cost != 0 else 0
            data.append([h['symbol'], h['shares'], h['avg_price'], price, market_val, cost, pnl, pnl_pct])
        
        df = pd.DataFrame(data, columns=['代码', '持股数', '平均成本', '当前价格', '市值', '成本', '盈亏', '盈亏%'])
        st.dataframe(df, use_container_width=True, hide_index=True,
            column_config={
                "平均成本": st.column_config.NumberColumn(format="$%.2f"),
                "当前价格": st.column_config.NumberColumn(format="$%.2f"),
                "市值": st.column_config.NumberColumn(format="$%.2f"),
                "成本": st.column_config.NumberColumn(format="$%.2f"),
                "盈亏": st.column_config.NumberColumn(format="$%.2f"),
                "盈亏%": st.column_config.NumberColumn(format="%.2f%%"),
            })

        total_market_value = df['市值'].sum()
        total_cost = df['成本'].sum()
        total_pnl = total_market_value - total_cost
        total_pnl_pct = (total_pnl / total_cost) * 100 if total_cost != 0 else 0
        
        c1, c2, c3 = st.columns(3)
        c1.metric("组合总值", f"${total_market_value:,.2f}")
        c2.metric("总盈亏", f"${total_pnl:,.2f}")
        c3.metric("收益率", f"{total_pnl_pct:.2f}%")
        
        st.subheader("持仓分布")
        plot_portfolio_pie(df)

    if st.button("清空持仓"):
        st.session_state.holdings = []
        st.rerun()

def news_analysis_page():
    """新闻分析页面"""
    st.header("📰 新闻情感分析")
    
    api_key_configured = False
    try:
        if 'GEMINI_API_KEY' in st.secrets and st.secrets['GEMINI_API_KEY']:
            os.environ['GEMINI_API_KEY'] = st.secrets['GEMINI_API_KEY']
            api_key_configured = True
    except Exception:
        if os.getenv('GEMINI_API_KEY'): api_key_configured = True

    if not api_key_configured:
        st.warning("请在 Secrets 中设置您的 GEMINI_API_KEY。")
        st.stop()

    news_input = st.text_area("输入新闻内容进行分析", "", height=150)
    
    if st.button("分析情感", type="primary"):
        if not news_input.strip():
            st.warning("请输入新闻内容。")
        else:
            with st.spinner("AI 正在分析新闻..."):
                try:
                    analyzer = SentimentAnalyzer()
                    result = analyzer.analyze_text(news_input)
                    
                    st.subheader("情感分析结果")
                    c1, c2, c3 = st.columns(3)
                    emoji = "😊" if result['sentiment'] == 'positive' else "😔" if result['sentiment'] == 'negative' else "😐"
                    c1.metric("情感倾向", f"{emoji} {result['sentiment'].upper()}")
                    c2.metric("情感分数", f"{result['score']:.2f}")
                    c3.metric("置信度", f"{result['confidence']:.1%}")
                    
                    if result.get('keywords'):
                        st.write("**关键词:** " + " | ".join(result['keywords']))
                except Exception as e:
                    st.error(f"❌ 分析时发生错误: {e}")

# --- Plotting Functions ---
def plot_price_chart(data, indicators):
    fig = go.Figure(go.Candlestick(x=data.index, open=data['Open'], high=data['High'], low=data['Low'], close=data['Close'], name='价格'))
    for period, sma in indicators.get('SMA', {}).items():
        fig.add_trace(go.Scatter(x=data.index, y=sma, mode='lines', name=f'SMA{period}'))
    fig.update_layout(title='价格走势', xaxis_rangeslider_visible=False)
    st.plotly_chart(fig, use_container_width=True)

def plot_rsi_chart(indicators):
    rsi_data = indicators.get('RSI', pd.Series())
    if rsi_data.empty: return
    fig = go.Figure(go.Scatter(x=rsi_data.index, y=rsi_data, name='RSI'))
    fig.add_hline(y=70, line_dash="dash", line_color="red")
    fig.add_hline(y=30, line_dash="dash", line_color="green")
    fig.update_layout(title='RSI 指标')
    st.plotly_chart(fig, use_container_width=True)

def plot_macd_chart(indicators):
    macd_data = indicators.get('MACD', {})
    if not macd_data: return
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=macd_data['macd'].index, y=macd_data['macd'], name='MACD'))
    fig.add_trace(go.Scatter(x=macd_data['signal'].index, y=macd_data['signal'], name='Signal'))
    fig.add_trace(go.Bar(x=macd_data['histogram'].index, y=macd_data['histogram'], name='Histogram'))
    fig.update_layout(title='MACD 指标')
    st.plotly_chart(fig, use_container_width=True)

def plot_bollinger_chart(data, indicators):
    bb = indicators.get('Bollinger_Bands', {})
    if not bb: return
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data.index, y=data['Close'], name='收盘价'))
    fig.add_trace(go.Scatter(x=data.index, y=bb['upper'], name='上轨', line=dict(dash='dash')))
    fig.add_trace(go.Scatter(x=data.index, y=bb['middle'], name='中轨'))
    fig.add_trace(go.Scatter(x=data.index, y=bb['lower'], name='下轨', line=dict(dash='dash')))
    fig.update_layout(title='布林带')
    st.plotly_chart(fig, use_container_width=True)

def plot_sma_chart(data, indicators):
    fig = go.Figure(go.Scatter(x=data.index, y=data['Close'], name='收盘价', opacity=0.7))
    for period, sma in indicators.get('SMA', {}).items():
        fig.add_trace(go.Scatter(x=data.index, y=sma, mode='lines', name=f'SMA{period}'))
    fig.update_layout(title='移动平均线')
    st.plotly_chart(fig, use_container_width=True)

def plot_volume_chart(data):
    fig = go.Figure(go.Bar(x=data.index, y=data['Volume'], name='成交量'))
    fig.update_layout(title='成交量')
    st.plotly_chart(fig, use_container_width=True)

def plot_atr_chart(indicators):
    atr_data = indicators.get('ATR', pd.Series())
    if atr_data.empty: return
    fig = go.Figure(go.Scatter(x=atr_data.index, y=atr_data, name='ATR'))
    fig.update_layout(title='ATR (真实波幅)')
    st.plotly_chart(fig, use_container_width=True)

def plot_equity_curve(equity_curve):
    fig = go.Figure(go.Scatter(x=equity_curve.index, y=equity_curve['equity'], name='资金曲线'))
    fig.update_layout(title='资金曲线')
    st.plotly_chart(fig, use_container_width=True)

def plot_portfolio_pie(df):
    fig = go.Figure(go.Pie(labels=df['代码'], values=df['市值'], hole=0.3))
    fig.update_layout(title='持仓分布')
    st.plotly_chart(fig, use_container_width=True)

def display_technical_details(indicators):
    details = []
    if 'RSI' in indicators:
        rsi = indicators['RSI'].iloc[-1]
        status = '超买' if rsi > 70 else '超卖' if rsi < 30 else '中性'
        details.append(['RSI', f'{rsi:.2f}', status])
    if 'MACD' in indicators:
        macd = indicators['MACD']['macd'].iloc[-1]
        sig = indicators['MACD']['signal'].iloc[-1]
        status = '看涨' if macd > sig else '看跌'
        details.append(['MACD', f'{macd:.2f}', status])
    if 'SMA' in indicators:
        sma5 = indicators['SMA'].get('SMA_5', pd.Series([np.nan])).iloc[-1]
        sma20 = indicators['SMA'].get('SMA_20', pd.Series([np.nan])).iloc[-1]
        if not pd.isna(sma5) and not pd.isna(sma20):
            status = '上升' if sma5 > sma20 else '下降'
            details.append(['趋势', f'{sma5:.2f}/{sma20:.2f}', status])
    if details:
        df = pd.DataFrame(details, columns=['指标','最新值','状态'])
        st.dataframe(df, hide_index=True, use_container_width=True)

if __name__ == "__main__":
    main()
