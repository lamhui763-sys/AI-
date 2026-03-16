"""
AI分析模块
集成多種AI工具（Gemini、ChatGPT等）提供智能投資分析
"""

import os
import json
import logging
from typing import Dict, List, Optional, Union
from datetime import datetime
import pandas as pd

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AIAnalyzer:
    """AI分析器 - 集成多種AI工具進行投資分析"""
    
    def __init__(self, config: Optional[Dict] = None):
        """
        初始化AI分析器
        
        Args:
            config: 配置字典，包含API密鑰等
        """
        self.config = config or {}
        self.logger = logger
        
        # 從配置中獲取API密鑰
        self.gemini_api_key = self.config.get('gemini_api_key') or os.getenv('GEMINI_API_KEY')
        self.openai_api_key = self.config.get('openai_api_key') or os.getenv('OPENAI_API_KEY')
        
        self.openai_model = self.config.get('openai_model', 'gpt-4')
        self.gemini_model_name = self.config.get('gemini_model', 'gemini-1.5-flash')
        
        # 優先使用 Gemini
        self.use_gemini = bool(self.gemini_api_key and GEMINI_AVAILABLE)
        
        # 初始化AI客戶端
        self.openai_client = None
        self.gemini_model = None
        
        if self.use_gemini:
            self._init_gemini()
        else:
            self._init_openai()
    
    def _init_gemini(self):
        """初始化Gemini客戶端"""
        if self.gemini_api_key and GEMINI_AVAILABLE:
            try:
                genai.configure(api_key=self.gemini_api_key)
                self.gemini_model = genai.GenerativeModel(self.gemini_model_name)
                self.logger.info(f"Gemini客戶端初始化成功 (模型: {self.gemini_model_name})")
            except Exception as e:
                self.logger.error(f"Gemini客戶端初始化失敗: {e}")
                self.use_gemini = False
                self._init_openai()
    
    def _init_openai(self):
        """初始化OpenAI客戶端"""
        if self.openai_api_key and OPENAI_AVAILABLE:
            try:
                openai.api_key = self.openai_api_key
                self.openai_client = openai
                self.logger.info("OpenAI客戶端初始化成功")
            except Exception as e:
                self.logger.error(f"OpenAI客戶端初始化失敗: {e}")
        else:
            if not self.openai_api_key and not self.gemini_api_key:
                self.logger.warning("未提供任何 AI API 密鑰")
    
    def _call_ai(self, prompt: str, temperature: float = 0.7) -> str:
        """統一調用 AI 接口"""
        if self.use_gemini and self.gemini_model:
            return self._call_gemini(prompt, temperature)
        elif self.openai_client:
            return self._call_openai(prompt, temperature)
        else:
            self.logger.warning("AI客戶端未初始化，返回模擬響應")
            return self._get_mock_response(prompt)

    def _call_gemini(self, prompt: str, temperature: float = 0.7) -> str:
        """調用 Gemini API"""
        try:
            response = self.gemini_model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=temperature,
                    max_output_tokens=2048,
                )
            )
            return response.text
        except Exception as e:
            self.logger.error(f"調用 Gemini API 失敗: {e}")
            if self.openai_client:
                return self._call_openai(prompt, temperature)
            return self._get_mock_response(prompt)

    def _call_openai(self, prompt: str, temperature: float = 0.7) -> str:
        """調用 OpenAI API"""
        try:
            # 兼容新舊版本 OpenAI SDK
            if hasattr(self.openai_client, 'ChatCompletion'):
                response = self.openai_client.ChatCompletion.create(
                    model=self.openai_model,
                    messages=[
                        {"role": "system", "content": "你是一位專業的港股分析師和投資顧問。"},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=temperature,
                    max_tokens=1500
                )
                return response.choices[0].message.content
            else:
                # 假設是新版 SDK
                from openai import OpenAI
                client = OpenAI(api_key=self.openai_api_key)
                response = client.chat.completions.create(
                    model=self.openai_model,
                    messages=[
                        {"role": "system", "content": "你是一位專業的港股分析師和投資顧問。"},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=temperature,
                )
                return response.choices[0].message.content
        except Exception as e:
            self.logger.error(f"調用 OpenAI API 失敗: {e}")
            return self._get_mock_response(prompt)

    def analyze_stock_with_ai(self, symbol: str, technical_data: Dict, 
                               market_news: Optional[List[Dict]] = None) -> Dict:
        """使用AI分析股票"""
        self.logger.info(f"開始AI分析股票: {symbol}")
        prompt = self._build_analysis_prompt(symbol, technical_data, market_news)
        ai_response = self._call_ai(prompt)
        return self._parse_ai_response(ai_response)
    
    def get_investment_advice(self, symbol: str, technical_data: Dict,
                               portfolio_data: Optional[Dict] = None) -> Dict:
        """獲取投資建議"""
        self.logger.info(f"獲取投資建議: {symbol}")
        prompt = self._build_investment_prompt(symbol, technical_data, portfolio_data)
        ai_response = self._call_ai(prompt)
        return self._parse_investment_advice(ai_response)
    
    def generate_report(self, symbol: str, technical_data: Dict,
                       ai_analysis: Dict, news: Optional[List[Dict]] = None) -> str:
        """生成綜合分析報告"""
        prompt = self._build_report_prompt(symbol, technical_data, ai_analysis, news)
        return self._call_ai(prompt)
    
    def explain_indicator(self, indicator_name: str, value: float,
                         context: Optional[str] = None) -> str:
        """解釋技術指標"""
        prompt = f"""
請解釋以下技術指標的當前狀態和含義：

指標名稱: {indicator_name}
當前值: {value}
上下文: {context if context else '無'}

請用簡潔明了的語言解釋：
1. 這個指標的含義
2. 當前值的含義
3. 對投資的啟示
4. 風險提示

請用繁體中文回答。
"""
        return self._call_ai(prompt)
    
    def compare_stocks(self, stocks_data: Dict[str, Dict]) -> Dict:
        """比較多隻股票"""
        self.logger.info(f"比較 {len(stocks_data)} 只股票")
        prompt = self._build_comparison_prompt(stocks_data)
        comparison = self._call_ai(prompt)
        return self._parse_comparison(comparison)
    
    def sentiment_analysis(self, text: str) -> Dict:
        """情感分析"""
        prompt = f"""
請對以下文本進行情感分析：

文本內容: {text}

請分析：
1. 整體情感（正面/負面/中性）
2. 情感強度（1-10分）
3. 關鍵情感詞
4. 對投資的啟示

請以JSON格式返回，使用繁體中文。
"""
        response = self._call_ai(prompt)
        return self._parse_json_response(response)
    
    def generate_trading_plan(self, symbol: str, analysis: Dict,
                              risk_tolerance: str = 'medium') -> Dict:
        """生成交易計劃"""
        prompt = self._build_trading_plan_prompt(symbol, analysis, risk_tolerance)
        plan = self._call_ai(prompt)
        return self._parse_trading_plan(plan)
    
    def _build_analysis_prompt(self, symbol: str, technical_data: Dict,
                                news: Optional[List[Dict]] = None) -> str:
        """構建分析提示"""
        prompt = f"""
你是一位專業的港股分析師。請分析以下股票：

股票代碼: {symbol}

技術指標數據:
{json.dumps(technical_data, ensure_ascii=False, indent=2)}
"""
        if news:
            prompt += "\n市場新聞:\n"
            for item in news:
                prompt += f"- {item.get('title', '')}: {item.get('summary', '')}\n"
        
        prompt += """
請提供以下分析：
1. 技面分析（基於技術指標）
2. 趨勢判斷
3. 風險評估
4. 操作建議（買入/持有/賣出）
5. 目標價位（如有）
6. 止損價位（如有）

請以JSON格式返回，使用繁體中文。
"""
        return prompt
    
    def _build_investment_prompt(self, symbol: str, technical_data: Dict,
                                  portfolio_data: Optional[Dict] = None) -> str:
        """構建投資建議提示"""
        prompt = f"""
你是一位投資顧問。請為以下股票提供投資建議：

股票代碼: {symbol}

技術分析:
{json.dumps(technical_data, ensure_ascii=False, indent=2)}
"""
        if portfolio_data:
            prompt += f"\n當前投資組合:\n{json.dumps(portfolio_data, ensure_ascii=False, indent=2)}\n"
        
        prompt += """
請提供：
1. 是否建議投資（是/否/觀望）
2. 建議倉位比例
3. 買入時機
4. 風險提示
5. 投資理由

請以JSON格式返回，使用繁體中文。
"""
        return prompt
    
    def _build_report_prompt(self, symbol: str, technical_data: Dict,
                             ai_analysis: Dict, news: Optional[List[Dict]] = None) -> str:
        """構建報告提示"""
        prompt = f"""
請為以下股票生成一份專業的投資分析報告：

股票代碼: {symbol}

技術指標:
{json.dumps(technical_data, ensure_ascii=False, indent=2)}

AI分析:
{json.dumps(ai_analysis, ensure_ascii=False, indent=2)}
"""
        if news:
            prompt += "\n相關新聞:\n"
            for item in news:
                prompt += f"- {item.get('title', '')}\n"
        
        prompt += """
請生成一份結構清晰、內容專業的投資分析報告，包含：
1. 報告摘要
2. 技術面分析
3. 風險評估
4. 投資建議
5. 結論

請使用繁體中文，格式清晰易讀。
"""
        return prompt
    
    def _build_comparison_prompt(self, stocks_data: Dict[str, Dict]) -> str:
        """構建比較提示"""
        prompt = "請比較以下股票的技术指標和投資價值：\n\n"
        for symbol, data in stocks_data.items():
            prompt += f"{symbol}:\n"
            prompt += f"{json.dumps(data, ensure_ascii=False, indent=2)}\n\n"
        
        prompt += """
請提供：
1. 各股票的優勢和劣勢
2. 投資價值排名
3. 不同投資風格的選擇建議

請以JSON格式返回，使用繁體中文。
"""
        return prompt
    
    def _build_trading_plan_prompt(self, symbol: str, analysis: Dict,
                                    risk_tolerance: str) -> str:
        """構建交易計劃提示"""
        prompt = f"""
請為以下股票制定詳細的交易計劃：

股票代碼: {symbol}
風險承受能力: {risk_tolerance}

分析數據:
{json.dumps(analysis, ensure_ascii=False, indent=2)}

請提供詳細的交易計劃：
1. 入場點位
2. 止損點位
3. 目標價位
4. 倉位管理
5. 時間週期
6. 風險控制措施

請以JSON格式返回，使用繁體中文。
"""
        return prompt
    
    def _parse_ai_response(self, response: str) -> Dict:
        """解析AI響應"""
        return self._parse_json_response(response)
    
    def _parse_investment_advice(self, response: str) -> Dict:
        """解析投資建議"""
        return self._parse_json_response(response)
    
    def _parse_comparison(self, response: str) -> Dict:
        """解析比較結果"""
        return self._parse_json_response(response)
    
    def _parse_trading_plan(self, response: str) -> Dict:
        """解析交易計劃"""
        return self._parse_json_response(response)
    
    def _parse_json_response(self, response: str) -> Dict:
        """解析JSON響應"""
        try:
            # 尋找 JSON 塊
            if "```json" in response:
                json_str = response.split("```json")[1].split("```")[0].strip()
            elif "```" in response:
                json_str = response.split("```")[1].split("```")[0].strip()
            else:
                json_str = response.strip()
            
            return json.loads(json_str)
        except Exception as e:
            self.logger.error(f"解析JSON響應失敗: {e}")
            return {"error": "解析失敗", "raw_response": response}
    
    def _get_mock_response(self, prompt: str) -> str:
        """獲取模擬響應（當 API 不可用時）"""
        return "AI 分析暫不可用，請檢查 API 密鑰配置。"
