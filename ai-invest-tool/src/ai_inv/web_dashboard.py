'''
Web仪表板模块 - 修正AI分析页面参数错误
使用Streamlit创建交互式Web界面
'''

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import sys
import os

# 确保可以找到我们项目中的模块
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from src.ai_inv.technical_analyzer import TechnicalAnalyzer
from src.ai_inv.ai_analyzer import AIAnalyzer
from src.ai_inv.sentiment_analyzer import SentimentAnalyzer
from src.ai_inv.smart_advisor import SmartAdvisor
from src.ai_inv.backtester import BacktestEngine, MAStrategy, RSIStrategy, MACDStrategy
from src.ai_inv.data_fetcher import DataFetcher
from src.ai_inv.indicators import TechnicalIndicators

# --- 绘图函数 ---

def plot_price_chart(data):
    if data is None or data.empty: return
    fig = go.Figure(data=[go.Candlestick(x=data.index, open=data['Open'], high=data['High'], low=data['Low'], close=data['Close'], name='K线')])
    sma_cols = [col for col in data.columns if 'SMA' in col]
    for col in sma_cols:
        fig.add_trace(go.Scatter(x=data.index, y=data[col], mode='lines', name=col.replace('_', ' ')))
    fig.update_layout(title='价格走势', xaxis_rangeslider_visible=False)
    st.plotly_chart(fig, use_container_width=True)

def plot_rsi_chart(data):
    if data is None or 'RSI' not in data.columns or data['RSI'].dropna().empty: return
    fig = go.Figure(go.Scatter(x=data.index, y=data['RSI'], name='RSI'))
    fig.add_hline(y=70, line_dash="dash", line_color="red", annotation_text="超买")
    fig.add_hline(y=30, line_dash="dash", line_color="green", annotation_text="超卖")
    fig.update_layout(title='RSI 指标', yaxis_range=[0,100])
    st.plotly_chart(fig, use_container_width=True)

def plot_macd_chart(data):
    if data is None or not all(k in data.columns for k in ['MACD', 'MACD_signal', 'MACD_hist']): return
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data.index, y=data['MACD'], name='MACD', line_color='#1f77b4'))
    fig.add_trace(go.Scatter(x=data.index, y=data['MACD_signal'], name='Signal', line_color='#ff7f0e'))
    colors = ['#2ca02c' if v >= 0 else '#d62728' for v in data['MACD_hist']]
    fig.add_trace(go.Bar(x=data.index, y=data['MACD_hist'], name='Histogram', marker_color=colors))
    fig.update_layout(title='MACD 指标')
    st.plotly_chart(fig, use_container_width=True)

def plot_bollinger_chart(data):
    if data is None or not all(k in data.columns for k in ['BB_upper', 'BB_middle', 'BB_lower']): return
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data.index, y=data['Close'], name='收盘价', line_color='blue'))
    fig.add_trace(go.Scatter(x=data.index, y=data['BB_upper'], name='上轨', line=dict(dash='dash', color='gray')))
    fig.add_trace(go.Scatter(x=data.index, y=data['BB_middle'], name='中轨', line=dict(color='gray', width=1.5)))
    fig.add_trace(go.Scatter(x=data.index, y=data['BB_lower'], name='下轨', line=dict(dash='dash', color='gray')))
    fig.update_layout(title='布林带')
    st.plotly_chart(fig, use_container_width=True)

def plot_volume_chart(data):
    if data is None or 'Volume' not in data.columns: return
    fig = go.Figure(go.Bar(x=data.index, y=data['Volume'], name='成交量'))
    fig.update_layout(title='成交量')
    st.plotly_chart(fig, use_container_width=True)

def plot_equity_curve(equity_curve):
    if equity_curve is None or equity_curve.empty: return
    fig = go.Figure(go.Scatter(x=equity_curve.index, y=equity_curve['equity'], name='资金曲线'))
    fig.update_layout(title='资金曲线', yaxis_title='资产净值')
    st.plotly_chart(fig, use_container_width=True)

def plot_portfolio_pie(df):
    if df is None or df.empty: return
    fig = px.pie(df, names='代码', values='市值', title='持仓分布', hole=0.3)
    st.plotly_chart(fig, use_container_width=True)

def display_technical_details(data):
    details = []
    if data is None or data.empty: return
    if 'RSI' in data.columns and not data['RSI'].dropna().empty:
        rsi = data['RSI'].iloc[-1]
        if not pd.isna(rsi): details.append(['RSI', f'{rsi:.2f}', '超买' if rsi > 70 else '超卖' if rsi < 30 else '中性'])
    if all(k in data.columns for k in ['MACD', 'MACD_signal']) and not data['MACD'].dropna().empty:
        macd, sig = data['MACD'].iloc[-1], data['MACD_signal'].iloc[-1]
        if not pd.isna(macd) and not pd.isna(sig): details.append(['MACD', f'{macd:.2f}', '看涨 (金叉)' if macd > sig else '看跌 (死叉)'])
    sma_cols = sorted([col for col in data.columns if col.startswith('SMA_')])
    if len(sma_cols) >= 2:
        short_sma_col, long_sma_col = sma_cols[0], sma_cols[-1]
        if not data[short_sma_col].dropna().empty and not data[long_sma_col].dropna().empty:
            sma_short, sma_long = data[short_sma_col].iloc[-1], data[long_sma_col].iloc[-1]
            if not pd.isna(sma_short) and not pd.isna(sma_long): details.append([f'趋势 ({short_sma_col}/{long_sma_col})'.replace('_',' '), f'{sma_short:.2f}/{sma_long:.2f}', '上升趋势' if sma_short > sma_long else '下降趋势'])
    if details:
        st.dataframe(pd.DataFrame(details, columns=['指标','最新值','状态']), hide_index=True, use_container_width=True)


# --- 页面函数 ---

def stock_analysis_page():
    st.header("📊 股票分析")
    st.sidebar.subheader("股票配置")
    symbol_input = st.sidebar.text_input("股票代码（多个用逗号分隔）", value="^HSI")
    symbols = [s.strip() for s in symbol_input.split(',') if s.strip()]
    period = st.sidebar.selectbox("时间周期", ['1mo', '3mo', '6mo', '1y', '2y', '5y'], index=3)
    analyzer = TechnicalAnalyzer()

    if st.sidebar.button("开始分析", type="primary"):
        if not symbols: st.warning("请输入至少一个股票代码。"); return
        with st.spinner("正在获取数据并分析..."):
            results = []
            for symbol in symbols:
                try:
                    indicators_df = analyzer.analyze_stock(symbol, period=period)
                    if indicators_df is not None and not indicators_df.empty:
                        signal = analyzer.get_trading_signal(indicators_df)
                        results.append({'symbol': symbol, 'indicators_df': indicators_df, 'signal': signal, 'error': None})
                    else:
                        results.append({'symbol': symbol, 'indicators_df': None, 'signal': None, 'error': "无法获取或分析数据"})
                except Exception as e:
                    st.error(f"分析 {symbol} 时出现意外错误: {e}")
                    results.append({'symbol': symbol, 'indicators_df': None, 'signal': None, 'error': str(e)})
            st.session_state.analysis_results = results
    
    if 'analysis_results' in st.session_state:
        results = st.session_state.analysis_results
        if not results: return
        tabs = st.tabs([r['symbol'] for r in results])
        for tab, result in zip(tabs, results):
            with tab:
                indicators_df = result.get('indicators_df')
                if result.get('error'): st.error(f"❌ 错误: {result['error']}"); continue
                if indicators_df is None or indicators_df.empty: st.warning("未找到该股票的数据或数据不足。") ; continue
                
                col1, col2, col3, col4 = st.columns(4)
                latest_price = indicators_df['Close'].iloc[-1]
                col1.metric("最新价格", f"HK${latest_price:,.2f}")
                if len(indicators_df) >= 2:
                    prev_close = indicators_df['Close'].iloc[-2]
                    change = latest_price - prev_close
                    col2.metric("日涨跌", f"{change:+.2f}", f"{(change/prev_close*100):+.2f}%")
                signal_data = result.get('signal', {})
                col3.metric("交易信号", signal_data.get('交易信号', 'N/A'))
                col4.metric("信号强度", signal_data.get('强度', 'N/A'))
                
                st.divider()
                st.subheader("图表分析")
                plot_price_chart(indicators_df)
                c1, c2 = st.columns(2)
                with c1: plot_rsi_chart(indicators_df)
                with c2: plot_macd_chart(indicators_df)
                with st.expander("📋 详细技术指标"): display_technical_details(indicators_df)

def technical_analysis_page():
    st.header("🔬 技术分析")
    symbol = st.text_input("股票代码", value="^HSI")
    
    st.subheader("选择技术指标")
    c1, c2, c3 = st.columns(3)
    show_sma = c1.checkbox("移动平均线 (SMA)", value=True)
    show_rsi = c1.checkbox("RSI", value=True)
    show_macd = c2.checkbox("MACD", value=True)
    show_bollinger = c2.checkbox("布林带", value=True)
    show_volume = c3.checkbox("成交量", value=True)

    if st.button("生成分析", type="primary"):
        with st.spinner("正在计算技术指标..."):
            try:
                data = DataFetcher().get_historical_data(symbol, period='1y')
                if data is not None and not data.empty:
                    st.session_state.tech_indicators_df = TechnicalIndicators().calculate_all_indicators(data)
                else:
                    st.warning("无法获取数据。")
                    st.session_state.pop('tech_indicators_df', None)
            except Exception as e: st.error(f"❌ 错误: {e}")

    if 'tech_indicators_df' in st.session_state and st.session_state.tech_indicators_df is not None:
        df = st.session_state.tech_indicators_df
        plot_price_chart(df) if show_sma else None
        plot_rsi_chart(df) if show_rsi else None
        plot_macd_chart(df) if show_macd else None
        plot_bollinger_chart(df) if show_bollinger else None
        plot_volume_chart(df) if show_volume else None

def ai_analysis_page():
    st.header("🤖 AI分析")
    if not (('GEMINI_API_KEY' in st.secrets and st.secrets['GEMINI_API_KEY']) or os.getenv('GEMINI_API_KEY')):
        st.warning("请在 Streamlit Cloud 的 Secrets 中或本地环境变量中设置 GEMINI_API_KEY。") ; st.stop()

    symbol = st.text_input("股票代码", value="^HSI")
    if st.button("开始AI分析", type="primary"):
        st.session_state.pop('ai_result', None)
        with st.spinner("AI正在分析中..."):
            try:
                # --- BUG FIX START ---
                # 1. 获取技术分析数据
                tech_analyzer = TechnicalAnalyzer()
                technical_data_df = tech_analyzer.analyze_stock(symbol, period='3mo')

                if technical_data_df is None or technical_data_df.empty:
                    st.error("无法获取用于AI分析的技术数据。")
                    return
                
                # 2. 将技术数据摘要传递给AI分析器
                technical_summary = tech_analyzer.get_trading_signal(technical_data_df)
                ai_analyzer = AIAnalyzer()
                st.session_state.ai_result = ai_analyzer.analyze_stock_with_ai(symbol, technical_summary)
                # --- BUG FIX END ---

            except Exception as e:
                st.error(f"❌ 分析时发生错误: {e}")
    
    if 'ai_result' in st.session_state and st.session_state.ai_result:
        res = st.session_state.ai_result
        st.subheader("AI分析结果") 
        if res:
            st.metric("AI建议", res.get('recommendation', 'N/A'))
            st.markdown(res.get('analysis', '分析内容不可用。'))
        else:
            st.warning("AI分析未返回有效结果。")

def backtest_page():
    st.header("⏱️ 回测引擎")
    st.sidebar.subheader("回测配置")
    strategy_type = st.sidebar.selectbox("选择策略", ["移动平均交叉", "RSI", "MACD"])
    if strategy_type == "移动平均交叉": strategy = MAStrategy(st.sidebar.number_input("短期均线", value=5), st.sidebar.number_input("长期均线", value=20))
    elif strategy_type == "RSI": strategy = RSIStrategy(st.sidebar.number_input("RSI周期", value=14), st.sidebar.number_input("超卖线", value=30), st.sidebar.number_input("超买线", value=70))
    else: strategy = MACDStrategy(st.sidebar.number_input("快线周期", value=12), st.sidebar.number_input("慢线周期", value=26), st.sidebar.number_input("信号线周期", value=9))
    
    symbol = st.sidebar.text_input("回测股票代码", value="^HSI")
    capital = st.sidebar.number_input("初始资金", value=100000)
    if st.sidebar.button("开始回测", type="primary"):
        with st.spinner("正在运行回测..."):
            try:
                data = DataFetcher().get_historical_data(symbol, period='2y')
                if data is not None and not data.empty:
                    st.session_state.backtest_results = BacktestEngine(capital).run_backtest(data, strategy)
                else: st.warning("无法获取数据进行回测。")
            except Exception as e: st.error(f"❌ 错误: {e}")

    if 'backtest_results' in st.session_state:
        res = st.session_state.backtest_results
        st.subheader(f"{symbol} - {strategy_type}策略回测结果")
        summary = res.get('summary', {})
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("总收益", f"{summary.get('total_return', 0):.2f}%")
        c2.metric("年化收益", f"{summary.get('annual_return', 0):.2f}%")
        c3.metric("夏普比率", f"{summary.get('sharpe_ratio', 0):.2f}")
        c4.metric("最大回撤", f"{summary.get('max_drawdown', 0):.2f}%")
        if 'equity_curve' in res: plot_equity_curve(res['equity_curve'])
        with st.expander("交易统计与记录"):
            c1, c2 = st.columns(2)
            c1.metric("总交易数", summary.get('total_trades', 0))
            c1.metric("胜率", f"{summary.get('win_rate', 0):.2f}%")
            c2.metric("盈利交易数", summary.get('winning_trades', 0))
            c2.metric("亏损交易数", summary.get('losing_trades', 0))
            if 'trades' in res: st.dataframe(res['trades'], use_container_width=True)

def portfolio_page():
    st.header("💼 投资组合分析")
    if 'holdings' not in st.session_state: st.session_state.holdings = []
    with st.form("add_holding_form"): 
        c1, c2, c3 = st.columns(3)
        symbol, shares, price = c1.text_input("代码"), c2.number_input("股数", min_value=1), c3.number_input("成本价", min_value=0.0)
        if st.form_submit_button("添加持仓"):
            if symbol and shares > 0 and price > 0:
                st.session_state.holdings.append({'symbol': symbol, 'shares': shares, 'price': price})
                st.rerun()
            else:
                st.warning("请输入有效的持仓信息。")

    if st.session_state.holdings:
        portfolio_df = pd.DataFrame(st.session_state.holdings)
        fetcher = DataFetcher()
        current_prices = [fetcher.get_current_price(h['symbol']) for h in st.session_state.holdings]
        portfolio_df['current_price'] = [p if p is not None else 0 for p in current_prices]
        portfolio_df = portfolio_df[portfolio_df['current_price'] > 0] # 过滤掉获取价格失败的行
        
        if not portfolio_df.empty:
            portfolio_df['cost'] = portfolio_df['shares'] * portfolio_df['price']
            portfolio_df['market_value'] = portfolio_df['shares'] * portfolio_df['current_price']
            portfolio_df['pnl'] = portfolio_df['market_value'] - portfolio_df['cost']
            portfolio_df['pnl_pct'] = (portfolio_df['pnl'] / portfolio_df['cost']) * 100

            st.subheader("当前持仓")
            st.dataframe(portfolio_df, hide_index=True, use_container_width=True)
            total_cost, total_value = portfolio_df['cost'].sum(), portfolio_df['market_value'].sum()
            if total_cost > 0:
                c1, c2, c3 = st.columns(3)
                c1.metric("组合总值", f"${total_value:,.2f}")
                c2.metric("总盈亏", f"${(total_value - total_cost):,.2f}")
                c3.metric("总收益率", f"{(total_value/total_cost - 1):.2%}")
                plot_portfolio_pie(portfolio_df.rename(columns={'symbol':'代码', 'market_value':'市值'}))
        
        if st.button("清空持仓"): st.session_state.holdings = []; st.rerun()

def news_analysis_page():
    st.header("📰 新闻情感分析")
    if not (('GEMINI_API_KEY' in st.secrets and st.secrets['GEMINI_API_KEY']) or os.getenv('GEMINI_API_KEY')):
        st.warning("请在 Secrets 中设置您的 GEMINI_API_KEY。") ; st.stop()
    news_input = st.text_area("输入新闻内容进行分析", "", height=200)
    if st.button("分析情感", type="primary"):
        if not news_input.strip(): st.warning("请输入新闻内容。")
        else:
            with st.spinner("AI 正在分析新闻..."):
                try:
                    res = SentimentAnalyzer().analyze_text(news_input)
                    st.subheader("分析结果")
                    sentiment = res.get('sentiment', 'neutral')
                    emoji = {"positive": "😊", "negative": "😔", "neutral": "😐"}.get(sentiment)
                    c1,c2 = st.columns(2) 
                    c1.metric("情感倾向", f"{emoji} {sentiment.upper()}")
                    c2.metric("情感分数", f"{res.get('score', 0):.2f}")
                    if res.get('keywords'): st.write("**关键词:** " + " | ".join(res.get('keywords', [])))
                except Exception as e: st.error(f"❌ 分析时发生错误: {e}")

def main():
    st.set_page_config(page_title="AI投资分析工具", page_icon="📈", layout="wide")
    st.sidebar.title("📈 AI投资分析工具")
    page_map = {
        "股票分析": stock_analysis_page,
        "技术分析": technical_analysis_page,
        "AI分析": ai_analysis_page,
        "回测引擎": backtest_page,
        "投资组合": portfolio_page,
        "新闻分析": news_analysis_page
    }
    page = st.sidebar.radio("选择功能", page_map.keys())
    page_map[page]()

if __name__ == "__main__":
    main()
