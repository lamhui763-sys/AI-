"""
情感分析模块
分析市场新闻、社交媒体、财报等的情感倾向
"""

import logging
from typing import Dict, List, Optional, Tuple
import re
from datetime import datetime

try:
    import jieba
    JIEBA_AVAILABLE = True
except ImportError:
    JIEBA_AVAILABLE = False

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SentimentAnalyzer:
    """情感分析器"""
    
    def __init__(self, config: Optional[Dict] = None):
        """初始化情感分析器"""
        self.config = config or {}
        self.logger = logger
        
        # 初始化情感词典
        self.positive_words = self._load_positive_words()
        self.negative_words = self._load_negative_words()
        
        # 初始化分词器
        if JIEBA_AVAILABLE:
            jieba.initialize()
            logger.info("jieba分词器初始化成功")
    
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
        
        Args:
            text: 要分析的文本
            
        Returns:
            情感分析结果
        """
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
        
        Args:
            news_items: 新闻列表
            
        Returns:
            综合情感分析结果
        """
        total_score = 0
        all_positive = []
        all_negative = []
        detailed_results = []
        
        for item in news_items:
            text = item.get('title', '') + ' ' + item.get('summary', '')
            result = self.analyze_text(text)
            
            total_score += result['score']
            all_positive.extend(result['positive_words'])
            all_negative.extend(result['negative_words'])
            detailed_results.append({
                'title': item.get('title', ''),
                'sentiment': result['sentiment'],
                'score': result['score']
            })
        
        avg_score = total_score / len(news_items) if news_items else 0
        overall_sentiment = self._determine_sentiment(avg_score)
        
        return {
            'overall_sentiment': overall_sentiment,
            'average_score': avg_score,
            'positive_words': list(set(all_positive)),
            'negative_words': list(set(all_negative)),
            'news_count': len(news_items),
            'detailed_results': detailed_results,
            'analysis_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
    
    def analyze_sentiment_trend(self, sentiment_history: List[Dict]) -> Dict:
        """
        分析情感趋势
        
        Args:
            sentiment_history: 历史情感数据列表
            
        Returns:
            趋势分析结果
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
            message = '情感趋向正面'
        elif recent_avg < earlier_avg - 0.1:
            trend = 'declining'
            message = '情感趋向负面'
        else:
            trend = 'stable'
            message = '情感保持稳定'
        
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
        if JIEBA_AVAILABLE:
            return list(jieba.cut(text))
        else:
            # 简单按空格分割
            return text.split()
    
    def _calculate_sentiment_score(self, words: List[str]) -> float:
        """计算情感分数"""
        positive_count = sum(1 for word in words if word in self.positive_words)
        negative_count = sum(1 for word in words if word in self.negative_words)
        
        total = positive_count + negative_count
        
        if total == 0:
            return 0.0
        
        # 计算归一化分数 (-1 到 1)
        score = (positive_count - negative_count) / total
        
        return score
    
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
    
    def _extract_sentiment_words(self, words: List[str], 
                                   sentiment_words: set) -> set:
        """提取情感词"""
        return set(word for word in words if word in sentiment_words)
    
    def _calculate_confidence(self, score: float, word_count: int) -> float:
        """计算置信度"""
        if word_count < 5:
            return 0.3
        
        # 基于分数绝对值和词数量的置信度
        base_confidence = min(abs(score) * 1.5, 1.0)
        word_factor = min(word_count / 20.0, 1.0)
        
        confidence = base_confidence * word_factor
        
        return round(confidence, 2)


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
        
        Args:
            news_data: 新闻数据
            
        Returns:
            情感分析结果
        """
        title = news_data.get('title', '')
        summary = news_data.get('summary', '')
        content = news_data.get('content', '')
        
        # 综合分析
        full_text = f"{title} {summary} {content}"
        
        result = self.sentiment_analyzer.analyze_text(full_text)
        
        # 添加新闻特定信息
        result['news_source'] = news_data.get('source', 'unknown')
        result['news_time'] = news_data.get('time', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        result['news_url'] = news_data.get('url', '')
        
        return result
    
    def batch_analyze_news(self, news_list: List[Dict]) -> Dict:
        """
        批量分析新闻
        
        Args:
            news_list: 新闻列表
            
        Returns:
            批量分析结果
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
    
    def get_sentiment_summary(self, news_list: List[Dict]) -> str:
        """
        获取情感摘要
        
        Args:
            news_list: 新闻列表
            
        Returns:
            文本摘要
        """
        analysis = self.batch_analyze_news(news_list)
        
        summary = f"""
新闻情感分析摘要
{'='*50}

分析新闻数量: {analysis['news_analyzed']}
分析时间: {analysis['analysis_time']}

整体情感: {analysis['overall_sentiment']}
平均分数: {analysis['average_score']:.2f}

情感分布:
- 正面新闻: {analysis['positive_count']} 条
- 负面新闻: {analysis['negative_count']} 条
- 中性新闻: {analysis['neutral_count']} 条

{'='*50}
"""
        
        return summary
