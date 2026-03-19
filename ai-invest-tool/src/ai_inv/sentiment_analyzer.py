"""
情感分析模块
分析市场新闻、社交媒體、財報等的情感傾向
"""

import logging
from typing import Dict, List, Optional, Tuple
import re
from datetime import datetime

import streamlit as st
import os
import json
import google.generativeai as genai

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 嘗試獲取 API Key 的輔助函數
def get_api_key():
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        try:
            if st and hasattr(st, 'secrets'):
                api_key = st.secrets.get('GEMINI_API_KEY')
        except Exception: pass
    return api_key


class SentimentAnalyzer:
    """情感分析器"""
    
    def __init__(self, config: Optional[Dict] = None):
        """初始化情感分析器"""
        self.config = config or {}
        self.logger = logger
        
        # 初始化情感詞典 (備用方案)
        self.positive_words = self._load_positive_words()
        self.negative_words = self._load_negative_words()
        
        # 初始化 Gemini
        self.api_key = get_api_key()
        self.ai_enabled = False
        if self.api_key:
            try:
                genai.configure(api_key=self.api_key)
                self.model = genai.GenerativeModel('gemini-3.1-flash-lite-preview')
                self.ai_enabled = True
                logger.info("Gemini API 已為情感分析啟用 (gemini-3.1-flash-lite-preview)")
            except Exception as e:
                logger.error(f"Gemini 初始化失敗: {e}")

        # 初始化分词器
        if not self.ai_enabled:
            try:
                import jieba
                jieba.initialize()
                self.jieba_available = True
                logger.info("jieba分词器初始化成功")
            except ImportError:
                self.jieba_available = False
    
    def _load_positive_words(self) -> set:
        """加载正面情感词"""
        # 港股投资相关的正面词汇
        words = {
            '上涨', '升', '漲', '增長', '增', '好轉', '向好', '突破', '創新高', '創紀錄',
            '盈利', '盈利增長', '業績', '佳績', '優異', '強勁', '穩健', '持續', '穩定',
            '收購', '並購', '合作', '戰略合作', '股東', '回購', '增持', '看好', '推薦',
            '強勁增長', '領先', '優勢', '競爭力', '市場份額', '擴張', '擴大', '發展',
            '機遇', '利好', '利好消息', '積極', '正面', '樂觀', '信心', '強勁',
            '回升', '反弹', '轉強', '轉好', '改善', '優化', '升級', '升級', '革新',
            '成功', '達標', '超預期', '勝預期', '亮麗', '輝煌', '優秀', '出色',
            '支撐', '支撐位', '阻力', '阻力位', '技術面', '基本面', '利好', '看漲',
            '牛市', '牛', '牛氣', '多頭', '買入', '持有', '長線', '長期', '投資',
            '估值', '低估', '合理', '吸引', '值得', '機會', '入場', '建倉', '加倉'
        }
        return words
    
    def _load_negative_words(self) -> set:
        """加载负面情感词"""
        # 港股投资相关的负面词汇
        words = {
            '下跌', '跌', '跌', '下跌', '下滑', '回落', '暴跌', '暴跌', '急跌', '大跌',
            '虧損', '虧', '業績下滑', '業績倒退', '倒退', '衰退', '收縮', '萎縮',
            '風險', '危機', '危機', '困難', '挑戰', '壓力', '擔憂', '憂慮', '負面',
            '下跌', '調低', '下調', '降級', '減持', '減倉', '拋售', '拋', '售',
            '看淡', '不看好', '悲觀', '利空', '利空消息', '負面影響', '衝擊',
            '疲軟', '疲弱', '轉弱', '轉差', '惡化', '惡化', '惡化', '惡化',
            '失敗', '不達預期', '低於預期', '差於預期', '遜預期', '失望', '令人失望',
            '壓力', '阻力', '支撐', '跌破', '跌破', '跌破', '跌破支撐',
            '熊市', '熊', '熊氣', '空頭', '賣出', '減持', '做空', '短線', '短期',
            '高估', '泡沫', '風險', '危險', '危險', '謹慎', '警惕', '注意',
            '監管', '調查', '處罰', '罰款', '訴訟', '糾紛', '爭議', '質疑'
        }
        return words
    
    def analyze_text(self, text: str) -> Dict:
        """
        分析文本情感
        """
        if self.ai_enabled:
            return self._analyze_text_with_ai(text)
        return self._analyze_text_with_dictionary(text)

    def _analyze_text_with_ai(self, text: str) -> Dict:
        """使用 AI 分析文本情感"""
        prompt = f"""
        請分析以下財經新聞的情感傾向，並以 JSON 格式返回。
        情感分為: positive, negative, neutral。
        分數範圍為: -1.0 (極度負面) 到 1.0 (極度正面)。
        同時提取 3-5 個關鍵詞。
        
        新聞內容: {text}
        
        請嚴格遵守以下 JSON 格式：
        {{
            "sentiment": "positive/negative/neutral",
            "score": 0.5,
            "keywords": ["關鍵詞1", "關鍵詞2"],
            "summary": "一句話簡短總結這條新聞"
        }}
        """
        try:
            response = self.model.generate_content(prompt)
            # 更強大的 JSON 提取方式
            text_resp = response.text
            match = re.search(r'\{.*\}', text_resp, re.DOTALL)
            if match:
                json_str = match.group()
                data = json.loads(json_str)
            else:
                data = json.loads(text_resp.strip())
            
            # 確保所有必要字段都存在
            return {
                'sentiment': data.get('sentiment', 'neutral'),
                'score': float(data.get('score', 0.0)),
                'keywords': data.get('keywords', []),
                'summary': data.get('summary', '無摘要'),
                'positive_words': [],
                'negative_words': [],
                'confidence': 0.9,
                'method': 'gemini'
            }
        except Exception as e:
            logger.error(f"AI 情感分析失敗: {e}")
            return self._analyze_text_with_dictionary(text)

    def _analyze_text_with_dictionary(self, text: str) -> Dict:
        """使用詞典方法分析文本情感 (備用)"""
        # 预处理
        cleaned_text = self._preprocess_text(text)
        
        # 分词
        words = self._tokenize(cleaned_text)
        
        # 计算情感分数
        sentiment_score = self._calculate_sentiment_score(words)
        
        # 确定情感类别
        sentiment_label = self._determine_sentiment(sentiment_score)
        
        # 提取情感词
        positive_found = self._extract_sentiment_words(words, self.positive_words)
        negative_found = self._extract_sentiment_words(words, self.negative_words)
        
        return {
            'sentiment': sentiment_label,
            'score': sentiment_score,
            'strength': self._calculate_strength(sentiment_score),
            'positive_words': list(positive_found),
            'negative_words': list(negative_found),
            'positive_count': len(positive_found),
            'negative_count': len(negative_found),
            'total_words': len(words),
            'confidence': self._calculate_confidence(sentiment_score, len(words))
        }
    
    def analyze_news(self, news_items: List[Dict]) -> Dict:
        """
        分析新闻列表的情感
        """
        return self.batch_analyze_news(news_items)
    
    def analyze_sentiment_trend(self, sentiment_history: List[Dict]) -> Dict:
        """
        分析情感趋势
        """
        if not sentiment_history:
            return {'trend': 'unknown', 'message': '无历史数据'}
        
        scores = [item.get('score', 0) for item in sentiment_history]
        
        # 计算趋势
        if len(scores) < 3:
            return {'trend': 'insufficient_data', 'message': '数据不足'}
        
        # 简单线性趋势
        recent_avg = sum(scores[-3:]) / 3
        earlier_avg = sum(scores[-6:-3]) / 3 if len(scores) >= 6 else scores[0]
        
        if recent_avg > earlier_avg + 0.1:
            trend = 'improving'
            message = '情感趨向正面'
        elif recent_avg < earlier_avg - 0.1:
            trend = 'declining'
            message = '情感趨向負面'
        else:
            trend = 'stable'
            message = '情感保持穩定'
        
        return {
            'trend': trend,
            'message': message,
            'recent_score': recent_avg,
            'earlier_score': earlier_avg,
            'change': recent_avg - earlier_avg
        }
    
    def _preprocess_text(self, text: str) -> str:
        """预处理文本"""
        # 转换为小写
        text = text.lower()
        # 移除特殊字符
        text = re.sub(r'[^\w\s\u4e00-\u9fff]', ' ', text)
        # 移除多余空格
        text = ' '.join(text.split())
        return text
    
    def _tokenize(self, text: str) -> List[str]:
        """分词"""
        if hasattr(self, 'jieba_available') and self.jieba_available:
            import jieba
            return list(jieba.cut(text))
        else:
            return text.split()
    
    def _calculate_sentiment_score(self, words: List[str]) -> float:
        """计算情感分数"""
        positive_count = sum(1 for word in words if word in self.positive_words)
        negative_count = sum(1 for word in words if word in self.negative_words)
        total = positive_count + negative_count
        if total == 0:
            return 0.0
        return (positive_count - negative_count) / total
    
    def _determine_sentiment(self, score: float) -> str:
        """确定情感类别"""
        if score > 0.2:
            return 'positive'
        elif score < -0.2:
            return 'negative'
        else:
            return 'neutral'
    
    def _calculate_strength(self, score: float) -> str:
        """计算情感强度"""
        abs_score = abs(score)
        if abs_score > 0.6:
            return 'strong'
        elif abs_score > 0.3:
            return 'moderate'
        else:
            return 'weak'
    
    def _extract_sentiment_words(self, words: List[str], sentiment_words: set) -> set:
        """提取情感词"""
        return set(word for word in words if word in sentiment_words)
    
    def _calculate_confidence(self, score: float, word_count: int) -> float:
        """计算置信度"""
        if word_count < 5:
            return 0.3
        base_confidence = min(abs(score) * 1.5, 1.0)
        word_factor = min(word_count / 20.0, 1.0)
        return round(base_confidence * word_factor, 2)


class NewsSentimentAnalyzer:
    """新闻情感分析器"""
    
    def __init__(self, config: Optional[Dict] = None):
        """初始化新闻情感分析器"""
        self.config = config or {}
        self.sentiment_analyzer = SentimentAnalyzer(config)
        self.logger = logger
    
    def analyze_news_sentiment(self, news_data: Dict) -> Dict:
        """
        分析新闻情感
        """
        title = news_data.get('title', '')
        summary = news_data.get('summary', '')
        content = news_data.get('content', '')
        
        # 综合分析
        full_text = f"{title} {summary} {content}"
        
        result = self.sentiment_analyzer.analyze_text(full_text)
        
        # 添加新闻特定信息
        result['title'] = title
        result['news_source'] = news_data.get('source', 'unknown')
        result['news_time'] = news_data.get('time', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        result['news_url'] = news_data.get('url', '')
        
        return result
    
    def batch_analyze_news(self, news_list: List[Dict]) -> Dict:
        """
        批量分析新闻
        """
        individual_results = []
        all_scores = []
        
        for news in news_list:
            try:
                result = self.analyze_news_sentiment(news)
                individual_results.append(result)
                all_scores.append(result['score'])
            except Exception as e:
                self.logger.error(f"分析新闻失败: {e}")
        
        # 计算总体情感
        if all_scores:
            avg_score = sum(all_scores) / len(all_scores)
            overall_sentiment = self.sentiment_analyzer._determine_sentiment(avg_score)
        else:
            avg_score = 0.0
            overall_sentiment = 'neutral'
        
        return {
            'overall_sentiment': overall_sentiment,
            'average_score': avg_score,
            'news_analyzed': len(individual_results),
            'positive_count': sum(1 for r in individual_results if r['sentiment'] == 'positive'),
            'negative_count': sum(1 for r in individual_results if r['sentiment'] == 'negative'),
            'neutral_count': sum(1 for r in individual_results if r['sentiment'] == 'neutral'),
            'individual_results': individual_results,
            'analysis_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
    
    def get_sentiment_summary(self, analysis: Dict) -> str:
        """
        根据分析结果生成综合总结
        """
        if not analysis or not analysis.get('individual_results'):
            return "無可用新聞資料進行總結。"
            
        # 獲取前幾條新聞作為背景
        news_summaries = []
        for r in analysis.get('individual_results', []):
            title = r.get('title', '無標題')
            summ = r.get('summary', '無摘要')
            news_summaries.append(f"- {title}: {summ}")
            
        prompt = f"""
        請根據以下多條財經新聞的分析結果，寫一個簡短的「市場分析總結」（約 100-200 字）。
        考慮整體情感趨向（{analysis.get('overall_sentiment', 'neutral')}）和平均分數（{analysis.get('average_score', 0.0):.2f}）。
        
        新聞摘要列表：
        {chr(10).join(news_summaries[:5])}
        
        請用繁體中文回答，包含「整體評價」和「操盤建議」。
        """
        
        try:
            if self.sentiment_analyzer.ai_enabled:
                response = self.sentiment_analyzer.model.generate_content(prompt)
                return response.text
            else:
                return f"由於 AI 未啟用，無法生成深度總結。當前整體情感為 {analysis.get('overall_sentiment', 'neutral')}，平均得分 {analysis.get('average_score', 0.0):.2f}。"
        except Exception as e:
            error_msg = str(e)
            if "400" in error_msg and "location" in error_msg.lower():
                return "⚠️ **AI 市場總結暫時無法生成**：偵測到 API 地區限制 (User location is not supported)。\n\n💡 **修復建議**：\n1. 請確認您的環境可以使用 Google Gemini 服務。\n2. 嘗試使用 VPN 或代理伺服器切換至支援區域（如美國、日本、台灣等）。\n3. 檢查您的 Gemini API Key 是否正確且有效。"
            return f"生成總結時出錯: {error_msg}"
