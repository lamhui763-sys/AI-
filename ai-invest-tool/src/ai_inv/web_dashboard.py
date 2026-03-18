'''
Web仪表板模块 - 决定性修复版本
使用Streamlit创建交互式Web界面
'''

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import sys
import os

# 确保可以找到我们项目中的模块
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from src.ai_inv.technical_analyzer import TechnicalAnalyzer
from src.ai_inv.ai_analyzer import AIAnalyzer
from src.ai_inv.sentiment_analyzer import SentimentAnalyzer
from src.ai_inv.smart_advisor import SmartAdvisor
from src.ai_inv.backtester import BacktestEngine, MAStrategy, RSIStrategy, MACDStrategy
from src.ai_inv.data_fetcher import DataFetcher # 确保导入

# --- 绘图函数 (重构后，只接收一个DataFrame) ---

def plot_price_chart(data):
    """从包含所有指标的DataFrame绘制价格和SMA图表"""
    if data is None or data.empty: return
    fig = go.Figure(data=[go.Candlestick(x=data.index, open=data['Open'], high=data['High'], low=data['Low'], close=data['Close'], name='K线')])
    
    # 自动查找并绘制所有SMA线
    sma_cols = [col for col in data.columns if 'SMA' in col]
    for col in sma_cols:
        fig.add_trace(go.Scatter(x=data.index, y=data[col], mode='lines', name=col.replace('_', ' ')))
             
    fig.update_layout(title='价格走势', xaxis_rangeslider_visible=False)
    st.plotly_chart(fig, use_container_width=True)

def plot_rsi_chart(data):
    """从DataFrame绘制RSI图表"""
    if data is None or 'RSI' not in data.columns or data['RSI'].dropna().empty: return
    fig = go.Figure(go.Scatter(x=data.index, y=data['RSI'], name='RSI'))
    fig.add_hline(y=70, line_dash="dash", line_color="red", annotation_text="超买")
    fig.add_hline(y=30, line_dash="dash", line_color="green", annotation_text="超卖")
    fig.update_layout(title='RSI 指标', yaxis_range=[0,100])
    st.plotly_chart(fig, use_container_width=True)

def plot_macd_chart(data):
    """从DataFrame绘制MACD图表"""
    # 检查所需的所有列是否存在
    if data is None or not all(k in data.columns for k in ['MACD', 'MACD_signal', 'MACD_hist']): return
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data.index, y=data['MACD'], name='MACD', line_color='#1f77b4'))
    fig.add_trace(go.Scatter(x=data.index, y=data['MACD_signal'], name='Signal', line_color='#ff7f0e'))
    # 为柱状图上色
    colors = ['#2ca02c' if v >= 0 else '#d62728' for v in data['MACD_hist']]
    fig.add_trace(go.Bar(x=data.index, y=data['MACD_hist'], name='Histogram', marker_color=colors))
    fig.update_layout(title='MACD 指标')
    st.plotly_chart(fig, use_container_width=True)

def display_technical_details(data):
    """显示关键技术指标的摘要表格"""
    details = []
    if data is None or data.empty: return

    # 安全地获取RSI
    if 'RSI' in data.columns and not data['RSI'].dropna().empty:
        rsi = data['RSI'].iloc[-1]
        if not pd.isna(rsi):
            status = '超买' if rsi > 70 else '超卖' if rsi < 30 else '中性'
            details.append(['RSI', f'{rsi:.2f}', status])

    # 安全地获取MACD
    if 'MACD' in data.columns and 'MACD_signal' in data.columns and not data['MACD'].dropna().empty:
        macd = data['MACD'].iloc[-1]
        sig = data['MACD_signal'].iloc[-1]
        if not pd.isna(macd) and not pd.isna(sig):
            status = '看涨 (金叉)' if macd > sig else '看跌 (死叉)'
            details.append(['MACD', f'{macd:.2f}', status])
            
    # 安全地获取趋势
    sma_cols = sorted([col for col in data.columns if col.startswith('SMA_')])
    if len(sma_cols) >= 2:
        short_sma_col = sma_cols[0]
        long_sma_col = sma_cols[-1]
        if not data[short_sma_col].dropna().empty and not data[long_sma_col].dropna().empty:
            sma_short = data[short_sma_col].iloc[-1]
            sma_long = data[long_sma_col].iloc[-1]
            if not pd.isna(sma_short) and not pd.isna(sma_long):
                status = '上升趋势' if sma_short > sma_long else '下降趋势'
                details.append([f'趋势 ({short_sma_col}/{long_sma_col})'.replace('_',' '), f'{sma_short:.2f}/{sma_long:.2f}', status])
    
    if details:
        df = pd.DataFrame(details, columns=['指标','最新值','状态'])
        st.dataframe(df, hide_index=True, use_container_width=True)


# --- 页面函数 ---

def stock_analysis_page():
    """股票分析页面 - 经过重构以确保稳健性"""
    st.header("📊 股票分析")
    
    st.sidebar.subheader("股票配置")
    symbol_input = st.sidebar.text_input(
        "股票代码（多个用逗号分隔）",
        value="^HSI"
    )
    symbols = [s.strip() for s in symbol_input.split(',') if s.strip()]
    
    period = st.sidebar.selectbox(
        "时间周期",
        ['1mo', '3mo', '6mo', '1y', '2y', '5y'],
        index=3 # 默认改为1年
    )
    
    # 初始化/获取分析器
    # @st.cache_resource
    # def get_analyzer():
    #     return TechnicalAnalyzer()
    # analyzer = get_analyzer()
    # Streamlit Cloud的缓存机制可能与本地不同，暂时禁用以确保最新代码运行
    analyzer = TechnicalAnalyzer()

    if st.sidebar.button("开始分析", type="primary"):
        if not symbols:
            st.warning("请输入至少一个股票代码。")
            return

        with st.spinner("正在获取数据并分析..."):
            results = []
            for symbol in symbols:
                try:
                    # 核心步骤：调用重构后的 analyze_stock
                    indicators_df = analyzer.analyze_stock(symbol, period=period)
                    
                    if indicators_df is not None and not indicators_df.empty:
                        # 从DataFrame中获取信号
                        signal = analyzer.get_trading_signal(indicators_df)
                        results.append({
                            'symbol': symbol, 
                            'indicators_df': indicators_df, 
                            'signal': signal, 
                            'error': None
                        })
                    else:
                        results.append({'symbol': symbol, 'indicators_df': None, 'signal': None, 'error': "无法获取或分析数据"})
                
                except Exception as e:
                    st.error(f"分析 {symbol} 时出现意外错误: {e}")
                    results.append({'symbol': symbol, 'indicators_df': None, 'signal': None, 'error': str(e)})
            
            st.session_state.analysis_results = results
    
    # --- 显示结果 --- 
    if 'analysis_results' in st.session_state:
        results = st.session_state.analysis_results
        if not results: return

        tab_names = [r['symbol'] for r in results]
        tabs = st.tabs(tab_names)
        
        for tab, result in zip(tabs, results):
            with tab:
                # 根本性的错误修复点：使用明确的、无歧义的条件检查
                indicators_df = result.get('indicators_df')
                if result.get('error'):
                    st.error(f"❌ 错误: {result['error']}")
                elif indicators_df is None or indicators_df.empty:
                    st.warning("未找到该股票的数据或数据不足以进行分析。")
                else:
                    # --- 显示指标 --- 
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        latest_price = indicators_df['Close'].iloc[-1]
                        st.metric("最新价格", f"HK${latest_price:,.2f}")
                    with col2:
                        if len(indicators_df) >= 2:
                            prev_close = indicators_df['Close'].iloc[-2]
                            change = latest_price - prev_close
                            change_pct = (change / prev_close) * 100 if prev_close != 0 else 0
                            st.metric("日涨跌", f"{change:+.2f}", f"{change_pct:+.2f}%")
                    
                    # 安全地显示信号
                    signal_data = result.get('signal', {})
                    with col3:
                        st.metric("交易信号", signal_data.get('交易信号', 'N/A'))
                    with col4:
                        st.metric("信号强度", signal_data.get('强度', 'N/A'))
                    
                    st.divider()
                    
                    # --- 绘图 --- 
                    st.subheader("图表分析")
                    plot_price_chart(indicators_df)
                    
                    c1, c2 = st.columns(2)
                    with c1:
                        plot_rsi_chart(indicators_df)
                    with c2:
                        plot_macd_chart(indicators_df)
                        
                    with st.expander("📋 详细技术指标"):
                        display_technical_details(indicators_df)


# --- 其他页面 (保持结构，但确保其健壮性) ---

def technical_analysis_page():
    st.header("🔬 单独技术分析")
    # (这部分逻辑与主分析页类似，可以后续实现或简化)
    st.info("此功能正在开发中。请使用上面的“股票分析”页面进行综合分析。")

def ai_analysis_page():
    st.header("🤖 AI分析")
    st.info("此功能正在开发中。")

def backtest_page():
    st.header("⏱️ 回测引擎")
    st.info("此功能正在开发中。")

def portfolio_page():
    st.header("💼 投资组合分析")
    st.info("此功能正在开发中。")

def news_analysis_page():
    st.header("📰 新闻情感分析")
    st.info("此功能正在开发中。")


def main():
    """主函数 - Streamlit应用"""
    st.set_page_config(page_title="AI投资分析工具", page_icon="📈", layout="wide")
    
    st.sidebar.title("📈 AI投资分析工具")
    page = st.sidebar.radio(
        "选择功能",
        ["股票分析", "技术分析", "AI分析", "回测引擎", "投资组合", "新闻分析"]
    )
    
    page_map = {
        "股票分析": stock_analysis_page,
        "技术分析": technical_analysis_page,
        "AI分析": ai_analysis_page,
        "回测引擎": backtest_page,
        "投资组合": portfolio_page,
        "新闻分析": news_analysis_page
    }
    page_function = page_map.get(page, stock_analysis_page)
    page_function()

if __name__ == "__main__":
    main()
