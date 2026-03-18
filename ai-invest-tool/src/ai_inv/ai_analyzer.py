'''
AI分析器模块 - 使用Google Gemini Pro
'''

import google.generativeai as genai
import os
import pandas as pd
import json
import re
import logging

# 引入streamlit以访问secrets
try:
    import streamlit as st
except ImportError:
    st = None

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AIAnalyzer:
    """
    使用Google Gemini Pro进行AI股票分析。
    """
    def __init__(self, api_key: str = None):
        """
        初始化AI分析器。
        优先使用传入的api_key，否则从环境变量或Streamlit secrets中查找。
        """
        try:
            # 优先从Streamlit secrets获取（在Streamlit Cloud环境中）
            if st and hasattr(st, 'secrets') and "GEMINI_API_KEY" in st.secrets:
                api_key = st.secrets["GEMINI_API_KEY"]
            
            # 否则，从环境变量获取
            if not api_key:
                api_key = os.environ.get("GEMINI_API_KEY")

            if not api_key:
                raise ValueError("Gemini API Key not found. Please set it in st.secrets or as an environment variable.")

            genai.configure(api_key=api_key)
            # 修复：根据用户反馈和最新的API模型列表，改用 'gemini-1.5-flash-latest'
            self.model = genai.GenerativeModel('gemini-1.5-flash-latest')
            logger.info("AIAnalyzer initialized successfully with model 'gemini-1.5-flash-latest'.")
        except Exception as e:
            logger.error(f"Error initializing AIAnalyzer: {e}")
            # 重新引发异常，以便UI可以捕获并显示它
            raise e

    def _create_prompt(self, symbol: str, technical_data: pd.DataFrame) -> str:
        """
        根据最新的技术数据创建详细的AI分析提示。
        """
        # 提取最新的技术指标
        latest_indicators = technical_data.iloc[-1]
        
        summary = f"股票代码: {symbol}\n"
        summary += "最新技术指标:\n"
        
        # 安全地提取关键指标
        rsi = latest_indicators.get('RSI')
        if rsi is not None and not pd.isna(rsi):
            summary += f"- RSI(14): {rsi:.2f}\n"

        macd = latest_indicators.get('MACD')
        macd_signal = latest_indicators.get('MACD_signal')
        if macd is not None and macd_signal is not None and not pd.isna(macd):
            summary += f"- MACD: {macd:.2f} (信号线: {macd_signal:.2f})\n"
            if macd > macd_signal:
                summary += "  - 状态: 看涨 (金叉趋势)\n"
            else:
                summary += "  - 状态: 看跌 (死叉趋势)\n"
        
        # 提取SMA趋势
        sma_cols = sorted([col for col in technical_data.columns if col.startswith('SMA_')])
        if len(sma_cols) >= 2:
            short_sma_col = sma_cols[0]
            long_sma_col = sma_cols[-1]
            short_sma = latest_indicators.get(short_sma_col)
            long_sma = latest_indicators.get(long_sma_col)
            if short_sma is not None and long_sma is not None and not pd.isna(short_sma):
                summary += f"- 移动平均线: 短期({short_sma_col}) = {short_sma:.2f}, 长期({long_sma_col}) = {long_sma:.2f}\n"
                if short_sma > long_sma:
                    summary += "  - 趋势: 上升趋势 (黄金交叉)\n"
                else:
                    summary += "  - 趋势: 下降趋势 (死亡交叉)\n"
        
        latest_close = latest_indicators.get('Close')
        if latest_close:
            summary += f"- 最新收盘价: {latest_close:.2f}\n"

        prompt = f"""
        你是一位专业的金融分析师。基于以下为股票 {symbol} 提供的最新技术分析数据，请提供一份简洁、专业的投资分析报告。

        **技术数据摘要:**
        {summary}

        **你的任务:**
        1.  **投资建议 (recommendation):** 基于以上数据，明确给出你的投资建议。选项必须是以下之一：'强烈买入', '买入', '持有', '卖出', '强烈卖出'。
        2.  **分析 (analysis):** 提供一个简洁的分析，解释你为什么会给出这个建议。分析应结合提供的技术指标（如RSI状态、MACD交叉、移动平均线趋势等）来支持你的观点。

        **输出格式要求:**
        请严格按照以下JSON格式返回你的分析，不要添加任何额外的解释或标记。

        {{ "recommendation": "你的建议", "analysis": "你的分析内容" }}
        """
        logger.info(f"Generated prompt for {symbol}")
        return prompt

    def _parse_response(self, response_text: str) -> dict:
        """
        从AI的响应中解析出JSON对象。
        """
        logger.info(f"Raw AI response: {response_text}")
        # 使用正则表达式去除 ```json ... ``` 等标记
        match = re.search(r'\{.*\}', response_text, re.DOTALL)
        if match:
            json_str = match.group(0)
            try:
                return json.loads(json_str)
            except json.JSONDecodeError as e:
                logger.error(f"Failed to decode JSON from AI response: {e}\nResponse text: {json_str}")
                return {"error": "AI返回了无效的格式"}
        else:
            logger.error(f"No JSON object found in AI response: {response_text}")
            return {"error": "AI未能生成有效的分析"}

    def analyze_stock_with_ai(self, symbol: str, technical_data: pd.DataFrame) -> dict:
        """
        使用AI分析股票。

        Args:
            symbol: 股票代码。
            technical_data: 包含技术指标的DataFrame。

        Returns:
            一个包含分析结果的字典，或包含错误信息的字典。
        """
        if technical_data is None or technical_data.empty:
            return {"error": "技术数据为空，无法进行AI分析"}

        try:
            prompt = self._create_prompt(symbol, technical_data)
            
            # 调用Gemini API
            response = self.model.generate_content(prompt)
            
            # 解析响应
            result = self._parse_response(response.text)
            return result

        except Exception as e:
            logger.error(f"An exception occurred during AI analysis for {symbol}: {e}", exc_info=True)
            return {"error": f"AI分析服务出现意外错误: {str(e)}"}
