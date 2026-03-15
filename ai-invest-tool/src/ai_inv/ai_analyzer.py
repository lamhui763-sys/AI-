"""
AI分析模块
集成多种AI工具（ChatGPT、本地LLM等）提供智能投资分析
"""

import os
import json
import logging
from typing import Dict, List, Optional, Union
from datetime import datetime
import pandas as pd

try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

try:
    from langchain.llms import OpenAI as LangchainOpenAI
    from langchain.chat_models import ChatOpenAI
    from langchain.schema import HumanMessage, SystemMessage, AIMessage
    LANGCHAIN_AVAILABLE = True
except ImportError:
    LANGCHAIN_AVAILABLE = False

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AIAnalyzer:
    """AI分析器 - 集成多种AI工具进行投资分析"""
    
    def __init__(self, config: Optional[Dict] = None):
        """
        初始化AI分析器
        
        Args:
            config: 配置字典，包含API密钥等
        """
        self.config = config or {}
        self.logger = logger
        
        # 从配置中获取API密钥
        self.openai_api_key = self.config.get('openai_api_key') or os.getenv('OPENAI_API_KEY')
        self.openai_model = self.config.get('openai_model', 'gpt-4')
        
        # 初始化AI客户端
        self.openai_client = None
        self._init_openai()
    
    def _init_openai(self):
        """初始化OpenAI客户端"""
        if self.openai_api_key and OPENAI_AVAILABLE:
            try:
                openai.api_key = self.openai_api_key
                self.openai_client = openai
                self.logger.info("OpenAI客户端初始化成功")
            except Exception as e:
                self.logger.error(f"OpenAI客户端初始化失败: {e}")
        else:
            if not self.openai_api_key:
                self.logger.warning("未提供OpenAI API密钥")
            if not OPENAI_AVAILABLE:
                self.logger.warning("OpenAI库未安装")
    
    def analyze_stock_with_ai(self, symbol: str, technical_data: Dict, 
                               market_news: Optional[List[Dict]] = None) -> Dict:
        """
        使用AI分析股票
        
        Args:
            symbol: 股票代码
            technical_data: 技术分析数据
            market_news: 市场新闻列表
            
        Returns:
            AI分析结果
        """
        self.logger.info(f"开始AI分析股票: {symbol}")
        
        # 构建分析提示
        prompt = self._build_analysis_prompt(symbol, technical_data, market_news)
        
        # 调用AI分析
        ai_response = self._call_openai(prompt)
        
        # 解析AI响应
        result = self._parse_ai_response(ai_response)
        
        return result
    
    def get_investment_advice(self, symbol: str, technical_data: Dict,
                               portfolio_data: Optional[Dict] = None) -> Dict:
        """
        获取投资建议
        
        Args:
            symbol: 股票代码
            technical_data: 技术分析数据
            portfolio_data: 投资组合数据
            
        Returns:
            投资建议
        """
        self.logger.info(f"获取投资建议: {symbol}")
        
        # 构建投资建议提示
        prompt = self._build_investment_prompt(symbol, technical_data, portfolio_data)
        
        # 调用AI
        ai_response = self._call_openai(prompt)
        
        # 解析响应
        advice = self._parse_investment_advice(ai_response)
        
        return advice
    
    def generate_report(self, symbol: str, technical_data: Dict,
                       ai_analysis: Dict, news: Optional[List[Dict]] = None) -> str:
        """
        生成综合分析报告
        
        Args:
            symbol: 股票代码
            technical_data: 技术分析数据
            ai_analysis: AI分析结果
            news: 市场新闻
            
        Returns:
            格式化的报告
        """
        prompt = self._build_report_prompt(symbol, technical_data, ai_analysis, news)
        
        report = self._call_openai(prompt)
        
        return report
    
    def explain_indicator(self, indicator_name: str, value: float,
                         context: Optional[str] = None) -> str:
        """
        解释技术指标
        
        Args:
            indicator_name: 指标名称
            value: 指标值
            context: 上下文信息
            
        Returns:
            指标解释
        """
        prompt = f"""
请解释以下技术指标的当前状态和含义：

指标名称: {indicator_name}
当前值: {value}
上下文: {context if context else '无'}

请用简洁明了的语言解释：
1. 这个指标的含义
2. 当前值的含义
3. 对投资的启示
4. 风险提示

请用繁体中文回答。
"""
        
        explanation = self._call_openai(prompt)
        return explanation
    
    def compare_stocks(self, stocks_data: Dict[str, Dict]) -> Dict:
        """
        比较多只股票
        
        Args:
            stocks_data: 股票数据字典 {symbol: data}
            
        Returns:
            比较分析结果
        """
        self.logger.info(f"比较 {len(stocks_data)} 只股票")
        
        prompt = self._build_comparison_prompt(stocks_data)
        
        comparison = self._call_openai(prompt)
        
        return self._parse_comparison(comparison)
    
    def sentiment_analysis(self, text: str) -> Dict:
        """
        情感分析
        
        Args:
            text: 要分析的文本
            
        Returns:
            情感分析结果
        """
        prompt = f"""
请对以下文本进行情感分析：

文本内容: {text}

请分析：
1. 整体情感（正面/负面/中性）
2. 情感强度（1-10分）
3. 关键情感词
4. 对投资的启示

请以JSON格式返回，使用繁体中文。
"""
        
        response = self._call_openai(prompt)
        return self._parse_json_response(response)
    
    def generate_trading_plan(self, symbol: str, analysis: Dict,
                              risk_tolerance: str = 'medium') -> Dict:
        """
        生成交易计划
        
        Args:
            symbol: 股票代码
            analysis: 分析数据
            risk_tolerance: 风险承受能力 (low, medium, high)
            
        Returns:
            交易计划
        """
        prompt = self._build_trading_plan_prompt(symbol, analysis, risk_tolerance)
        
        plan = self._call_openai(prompt)
        
        return self._parse_trading_plan(plan)
    
    def _build_analysis_prompt(self, symbol: str, technical_data: Dict,
                                news: Optional[List[Dict]] = None) -> str:
        """构建分析提示"""
        prompt = f"""
你是一位专业的港股分析师。请分析以下股票：

股票代码: {symbol}

技术指标数据:
{json.dumps(technical_data, ensure_ascii=False, indent=2)}
"""
        
        if news:
            prompt += "\n市场新闻:\n"
            for item in news:
                prompt += f"- {item.get('title', '')}: {item.get('summary', '')}\n"
        
        prompt += """
请提供以下分析：
1. 技面分析（基于技术指标）
2. 趋势判断
3. 风险评估
4. 操作建议（买入/持有/卖出）
5. 目标价位（如有）
6. 止损价位（如有）

请以JSON格式返回，使用繁体中文。
"""
        
        return prompt
    
    def _build_investment_prompt(self, symbol: str, technical_data: Dict,
                                  portfolio_data: Optional[Dict] = None) -> str:
        """构建投资建议提示"""
        prompt = f"""
你是一位投资顾问。请为以下股票提供投资建议：

股票代码: {symbol}

技术分析:
{json.dumps(technical_data, ensure_ascii=False, indent=2)}
"""
        
        if portfolio_data:
            prompt += f"\n当前投资组合:\n{json.dumps(portfolio_data, ensure_ascii=False, indent=2)}\n"
        
        prompt += """
请提供：
1. 是否建议投资（是/否/观望）
2. 建议仓位比例
3. 买入时机
4. 风险提示
5. 投资理由

请以JSON格式返回，使用繁体中文。
"""
        
        return prompt
    
    def _build_report_prompt(self, symbol: str, technical_data: Dict,
                             ai_analysis: Dict, news: Optional[List[Dict]] = None) -> str:
        """构建报告提示"""
        prompt = f"""
请为以下股票生成一份专业的投资分析报告：

股票代码: {symbol}

技术指标:
{json.dumps(technical_data, ensure_ascii=False, indent=2)}

AI分析:
{json.dumps(ai_analysis, ensure_ascii=False, indent=2)}
"""
        
        if news:
            prompt += "\n相关新闻:\n"
            for item in news:
                prompt += f"- {item.get('title', '')}\n"
        
        prompt += """
请生成一份结构清晰、内容专业的投资分析报告，包含：
1. 报告摘要
2. 技术面分析
3. 风险评估
4. 投资建议
5. 结论

请使用繁体中文，格式清晰易读。
"""
        
        return prompt
    
    def _build_comparison_prompt(self, stocks_data: Dict[str, Dict]) -> str:
        """构建比较提示"""
        prompt = "请比较以下股票的技术指标和投资价值：\n\n"
        
        for symbol, data in stocks_data.items():
            prompt += f"{symbol}:\n"
            prompt += f"{json.dumps(data, ensure_ascii=False, indent=2)}\n\n"
        
        prompt += """
请提供：
1. 各股票的优势和劣势
2. 投资价值排名
3. 不同投资风格的选择建议

请以JSON格式返回，使用繁体中文。
"""
        
        return prompt
    
    def _build_trading_plan_prompt(self, symbol: str, analysis: Dict,
                                    risk_tolerance: str) -> str:
        """构建交易计划提示"""
        prompt = f"""
请为以下股票制定详细的交易计划：

股票代码: {symbol}
风险承受能力: {risk_tolerance}

分析数据:
{json.dumps(analysis, ensure_ascii=False, indent=2)}

请提供详细的交易计划：
1. 入场点位
2. 止损点位
3. 目标价位
4. 仓位管理
5. 时间周期
6. 风险控制措施

请以JSON格式返回，使用繁体中文。
"""
        
        return prompt
    
    def _call_openai(self, prompt: str, temperature: float = 0.7) -> str:
        """调用OpenAI API"""
        if not self.openai_client:
            self.logger.warning("OpenAI客户端未初始化，返回模拟响应")
            return self._get_mock_response(prompt)
        
        try:
            response = self.openai_client.ChatCompletion.create(
                model=self.openai_model,
                messages=[
                    {"role": "system", "content": "你是一位专业的港股分析师和投资顾问。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=temperature,
                max_tokens=1500
            )
            
            return response.choices[0].message.content
        
        except Exception as e:
            self.logger.error(f"调用OpenAI API失败: {e}")
            return self._get_mock_response(prompt)
    
    def _parse_ai_response(self, response: str) -> Dict:
        """解析AI响应"""
        try:
            # 尝试解析JSON
            if '{' in response and '}' in response:
                start = response.find('{')
                end = response.rfind('}') + 1
                json_str = response[start:end]
                return json.loads(json_str)
        except Exception as e:
            self.logger.warning(f"解析JSON响应失败: {e}")
        
        # 如果无法解析JSON，返回原始响应
        return {
            'raw_response': response,
            'status': 'success'
        }
    
    def _parse_investment_advice(self, response: str) -> Dict:
        """解析投资建议"""
        return self._parse_json_response(response)
    
    def _parse_json_response(self, response: str) -> Dict:
        """解析JSON响应"""
        try:
            if '{' in response and '}' in response:
                start = response.find('{')
                end = response.rfind('}') + 1
                json_str = response[start:end]
                return json.loads(json_str)
        except Exception as e:
            self.logger.warning(f"解析JSON失败: {e}")
        
        return {'raw_response': response}
    
    def _parse_comparison(self, response: str) -> Dict:
        """解析比较结果"""
        return self._parse_json_response(response)
    
    def _parse_trading_plan(self, response: str) -> Dict:
        """解析交易计划"""
        return self._parse_json_response(response)
    
    def _get_mock_response(self, prompt: str) -> str:
        """获取模拟响应（当API不可用时）"""
        return json.dumps({
            'status': 'mock',
            'message': 'API未配置，返回模拟响应',
            '建议': '请配置OpenAI API密钥以获取真实AI分析',
            '技术面分析': '基于技术指标的初步分析',
            '趋势判断': '需要更多数据进行准确判断',
            '风险评估': '中等风险',
            '操作建议': '观望'
        }, ensure_ascii=False, indent=2)


class LocalLLMAnalyzer:
    """本地LLM分析器 - 使用本地大语言模型"""
    
    def __init__(self, config: Optional[Dict] = None):
        """初始化本地LLM分析器"""
        self.config = config or {}
        self.logger = logger
        
        # 检查是否可用
        self.available = False
        self._check_availability()
    
    def _check_availability(self):
        """检查本地LLM是否可用"""
        try:
            # 可以添加对本地LLM（如llama.cpp、Ollama等）的支持
            import requests
            self.available = True
            self.logger.info("本地LLM可用")
        except ImportError:
            self.logger.warning("本地LLM不可用")
    
    def analyze(self, prompt: str) -> str:
        """使用本地LLM分析"""
        if not self.available:
            return "本地LLM不可用"
        
        # 这里可以集成本地LLM
        # 例如通过API调用Ollama、llama.cpp等
        return "本地LLM分析功能开发中"


class HybridAIAnalyzer:
    """混合AI分析器 - 结合多种AI工具"""
    
    def __init__(self, config: Optional[Dict] = None):
        """初始化混合AI分析器"""
        self.config = config or {}
        self.logger = logger
        
        # 初始化各个AI分析器
        self.openai_analyzer = AIAnalyzer(config)
        self.local_analyzer = LocalLLMAnalyzer(config)
    
    def analyze_with_consensus(self, symbol: str, technical_data: Dict) -> Dict:
        """
        使用多个AI工具进行共识分析
        
        Args:
            symbol: 股票代码
            technical_data: 技术分析数据
            
        Returns:
            共识分析结果
        """
        results = {}
        
        # 获取OpenAI分析
        try:
            openai_result = self.openai_analyzer.analyze_stock_with_ai(
                symbol, technical_data
            )
            results['openai'] = openai_result
        except Exception as e:
            self.logger.error(f"OpenAI分析失败: {e}")
            results['openai'] = {'error': str(e)}
        
        # 获取本地LLM分析（如果可用）
        try:
            local_result = self.local_analyzer.analyze(
                f"分析股票{symbol}: {json.dumps(technical_data)}"
            )
            results['local'] = {'response': local_result}
        except Exception as e:
            self.logger.error(f"本地LLM分析失败: {e}")
        
        # 生成共识
        consensus = self._generate_consensus(results)
        
        return {
            'individual_results': results,
            'consensus': consensus
        }
    
    def _generate_consensus(self, results: Dict) -> Dict:
        """生成共识分析"""
        # 这里可以实现多个AI结果的共识逻辑
        # 例如：投票机制、权重平均等
        
        consensus = {
            'recommendation': '观望',
            'confidence': 'medium',
            'sources_count': len(results),
            'analysis': '综合多个AI工具的分析结果'
        }
        
        return consensus
