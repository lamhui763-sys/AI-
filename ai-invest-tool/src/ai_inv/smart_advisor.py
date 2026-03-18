"""
智能投资顾问模块
结合技术分析、AI分析和情感分析，提供综合投资建议
"""

import logging
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import json

from .technical_analyzer import TechnicalAnalyzer
from .ai_analyzer import AIAnalyzer
from .sentiment_analyzer import SentimentAnalyzer, NewsSentimentAnalyzer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SmartAdvisor:
    """智能投资顾问 - 综合分析并提供投资建议"""
    
    def __init__(self, config: Optional[Dict] = None):
        """
        初始化智能投资顾问
        
        Args:
            config: 配置字典
        """
        self.config = config or {}
        self.logger = logger
        
        # 初始化各个分析器
        self.technical_analyzer = TechnicalAnalyzer(config)
        self.ai_analyzer = AIAnalyzer(config)
        self.hybrid_analyzer = self.ai_analyzer  # 保持兼容性，指向同一個實例
        self.sentiment_analyzer = SentimentAnalyzer(config)
        self.news_analyzer = NewsSentimentAnalyzer(config)
    
    def get_comprehensive_analysis(self, symbol: str, 
                                    period: str = '1y',
                                    include_news: bool = True) -> Dict:
        """
        获取综合分析
        
        Args:
            symbol: 股票代码
            period: 分析周期
            include_news: 是否包含新闻分析
            
        Returns:
            综合分析结果
        """
        self.logger.info(f"开始综合分析: {symbol}")
        
        # 1. 技术分析
        technical_data = self.technical_analyzer.analyze_stock(symbol, period=period)
        technical_summary = self.technical_analyzer.get_trading_signal(symbol, period)
        
        # 2. AI分析
        ai_analysis = self.ai_analyzer.analyze_stock_with_ai(symbol, technical_summary)
        
        # 3. 情感分析（如果提供新闻）
        sentiment_summary = None
        if include_news:
            # 这里可以接入实际的新闻API
            # 目前使用模拟新闻
            mock_news = self._get_mock_news(symbol)
            sentiment_summary = self.news_analyzer.batch_analyze_news(mock_news)
        
        # 4. 综合建议
        recommendation = self._generate_recommendation(
            technical_summary,
            ai_analysis,
            sentiment_summary
        )
        
        result = {
            'symbol': symbol,
            'analysis_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'technical_analysis': technical_summary,
            'ai_analysis': ai_analysis,
            'sentiment_analysis': sentiment_summary,
            'recommendation': recommendation
        }
        
        self.logger.info(f"综合分析完成: {symbol}")
        
        return result
    
    def get_investment_plan(self, symbol: str, 
                             capital: float,
                             risk_tolerance: str = 'medium',
                             investment_goal: str = 'growth') -> Dict:
        """
        获取投资计划
        
        Args:
            symbol: 股票代码
            capital: 投资本金
            risk_tolerance: 风险承受能力 (low, medium, high)
            investment_goal: 投资目标 (growth, income, balance)
            
        Returns:
            投资计划
        """
        self.logger.info(f"制定投资计划: {symbol}, 本金: {capital}")
        
        # 获取综合分析
        analysis = self.get_comprehensive_analysis(symbol)
        
        # 获取技术分析数据
        technical_data = self.technical_analyzer.analyze_stock(symbol, period='1y')
        latest = technical_data.iloc[-1]
        
        # 生成投资计划
        plan = {
            'symbol': symbol,
            'capital': capital,
            'risk_tolerance': risk_tolerance,
            'investment_goal': investment_goal,
            'plan_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            
            # 入场策略
            'entry_strategy': self._generate_entry_strategy(
                latest, analysis['recommendation'], risk_tolerance
            ),
            
            # 止损止盈
            'stop_loss': self._calculate_stop_loss(latest, risk_tolerance),
            'take_profit': self._calculate_take_profit(latest, risk_tolerance),
            
            # 仓位管理
            'position_size': self._calculate_position_size(
                capital, risk_tolerance, analysis['recommendation']
            ),
            
            # 风险控制
            'risk_control': self._generate_risk_control(risk_tolerance),
            
            # 时间周期
            'time_horizon': self._determine_time_horizon(investment_goal),
            
            # 监控指标
            'monitoring_indicators': self._get_monitoring_indicators()
        }
        
        return plan
    
    def generate_detailed_report(self, symbol: str, 
                                  include_charts: bool = False) -> str:
        """
        生成详细报告
        
        Args:
            symbol: 股票代码
            include_charts: 是否包含图表
            
        Returns:
            格式化的报告
        """
        # 获取综合分析
        analysis = self.get_comprehensive_analysis(symbol)
        
        # 获取技术分析数据
        technical_data = self.technical_analyzer.analyze_stock(symbol, period='1y')
        
        # 使用AI生成报告
        report = self.ai_analyzer.generate_report(
            symbol,
            analysis['technical_analysis'],
            analysis['ai_analysis'],
            analysis.get('sentiment_analysis')
        )
        
        # 添加综合建议部分
        detailed_report = f"""
{'='*70}
{symbol} 综合投资分析报告
{'='*70}

报告生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

{'='*70}
一、AI生成分析
{'='*70}

{report}

{'='*70}
二、综合投资建议
{'='*70}

建议操作: {analysis['recommendation']['action']}
建议理由: {analysis['recommendation']['reason']}
风险等级: {analysis['recommendation']['risk_level']}
置信度: {analysis['recommendation']['confidence']}

{'='*70}
三、详细分析分解
{'='*70}

技术面评分: {analysis['recommendation']['technical_score']}/10
AI分析评分: {analysis['recommendation']['ai_score']}/10
情感分析评分: {analysis['recommendation']['sentiment_score']}/10

{'='*70}
四、风险提示
{'='*70}

{self._generate_risk_warnings(analysis)}

{'='*70}
五、免责声明
{'='*70}

本报告仅供参考，不构成投资建议。投资有风险，入市需谨慎。
请根据自身情况做出投资决策。

{'='*70}
"""
        
        return detailed_report
    
    def compare_multiple_stocks(self, symbols: List[str]) -> Dict:
        """
        比较多只股票
        
        Args:
            symbols: 股票代码列表
            
        Returns:
            比较结果
        """
        self.logger.info(f"比较 {len(symbols)} 只股票")
        
        stock_analyses = {}
        
        for symbol in symbols:
            try:
                analysis = self.get_comprehensive_analysis(symbol, include_news=False)
                stock_analyses[symbol] = analysis
            except Exception as e:
                self.logger.error(f"分析股票 {symbol} 失败: {e}")
        
        # 使用AI进行综合比较
        comparison = self.ai_analyzer.compare_stocks(stock_analyses)
        
        # 计算排名
        rankings = self._calculate_rankings(stock_analyses)
        
        return {
            'stocks_analyzed': len(stock_analyses),
            'comparison': comparison,
            'rankings': rankings,
            'recommendations': self._generate_comparative_recommendations(rankings)
        }
    
    def get_portfolio_advice(self, portfolio: Dict) -> Dict:
        """
        获取投资组合建议
        
        Args:
            portfolio: 投资组合数据
            
        Returns:
            投资组合建议
        """
        self.logger.info("分析投资组合")
        
        holdings = portfolio.get('holdings', {})
        
        # 分析每只持仓
        holding_analyses = {}
        for symbol, holding in holdings.items():
            try:
                analysis = self.get_comprehensive_analysis(symbol)
                holding_analyses[symbol] = {
                    'analysis': analysis,
                    'holding': holding,
                    'current_value': holding.get('quantity', 0) * holding.get('avg_price', 0),
                    'pnl': self._calculate_pnl(holding, analysis['technical_analysis'])
                }
            except Exception as e:
                self.logger.error(f"分析持仓 {symbol} 失败: {e}")
        
        # 生成投资组合建议
        portfolio_advice = self._generate_portfolio_advice(holding_analyses)
        
        return {
            'portfolio_value': portfolio.get('total_value', 0),
            'holdings_analyzed': len(holding_analyses),
            'holding_analyses': holding_analyses,
            'portfolio_advice': portfolio_advice
        }
    
    def _generate_recommendation(self, technical: Dict, ai: Dict, 
                                   sentiment: Optional[Dict]) -> Dict:
        """生成综合建议"""
        # 计算各部分得分
        technical_score = self._calculate_technical_score(technical)
        ai_score = self._calculate_ai_score(ai)
        sentiment_score = self._calculate_sentiment_score(sentiment) if sentiment else 5.0
        
        # 加权总分
        total_score = (technical_score * 0.4 + ai_score * 0.4 + sentiment_score * 0.2)
        
        # 确定建议
        if total_score >= 7.5:
            action = 'strong_buy'
            reason = '多项指标显示强烈买入信号'
            risk_level = '低'
        elif total_score >= 6.0:
            action = 'buy'
            reason = '技术面和AI分析均偏多'
            risk_level = '中低'
        elif total_score >= 4.0:
            action = 'hold'
            reason = '指标显示中性，建议观望'
            risk_level = '中'
        elif total_score >= 2.5:
            action = 'sell'
            reason = '技术面偏空，建议减仓'
            risk_level = '中高'
        else:
            action = 'strong_sell'
            reason = '多项指标显示强烈卖出信号'
            risk_level = '高'
        
        # 计算置信度
        confidence = min(abs(total_score - 5.0) / 5.0 * 100, 100)
        
        return {
            'action': action,
            'reason': reason,
            'risk_level': risk_level,
            'confidence': f"{confidence:.1f}%",
            'total_score': round(total_score, 2),
            'technical_score': round(technical_score, 2),
            'ai_score': round(ai_score, 2),
            'sentiment_score': round(sentiment_score, 2) if sentiment else 5.0
        }
    
    def _calculate_technical_score(self, technical: Dict) -> float:
        """计算技术分析得分"""
        score = 5.0  # 基础分
        
        # 交易信号加分
        signal = technical.get('交易信号', 'HOLD')
        strength = technical.get('信号强度', 0)
        
        if signal in ['STRONG BUY', 'BUY']:
            score += strength * 0.5
        elif signal in ['STRONG SELL', 'SELL']:
            score -= strength * 0.5
        
        # RSI调整
        try:
            rsi_str = technical.get('动量指标', {}).get('RSI', 50)
            rsi = float(rsi_str) if isinstance(rsi_str, str) else rsi_str
            
            if 30 < rsi < 70:
                score += 0.5
            elif rsi < 30:
                score += 0.3
            elif rsi > 70:
                score -= 0.3
        except:
            pass
        
        return max(0.0, min(10.0, score))
    
    def _calculate_ai_score(self, ai: Dict) -> float:
        """计算AI分析得分"""
        score = 5.0  # 基础分
        
        # 从AI分析中提取建议
        recommendation = ai.get('操作建议', '').lower()
        
        if '買' in recommendation or '買入' in recommendation:
            score += 2.0
        elif '賣' in recommendation or '賣出' in recommendation:
            score -= 2.0
        
        return max(0.0, min(10.0, score))
    
    def _calculate_sentiment_score(self, sentiment: Dict) -> float:
        """计算情感分析得分"""
        if not sentiment:
            return 5.0
        
        overall = sentiment.get('overall_sentiment', 'neutral')
        avg_score = sentiment.get('average_score', 0.0)
        
        score = 5.0 + avg_score * 2.0
        
        if overall == 'positive':
            score += 1.0
        elif overall == 'negative':
            score -= 1.0
        
        return max(0.0, min(10.0, score))
    
    def _generate_entry_strategy(self, latest: Dict, recommendation: Dict,
                                   risk_tolerance: str) -> Dict:
        """生成入场策略"""
        action = recommendation['action']
        current_price = float(latest['Close'])
        
        if action in ['buy', 'strong_buy']:
            # 分批建仓策略
            if risk_tolerance == 'low':
                return {
                    'strategy': '分批建仓',
                    'first_entry': current_price,
                    'batch_count': 3,
                    'interval_days': 3,
                    'total_percentage': 60
                }
            elif risk_tolerance == 'high':
                return {
                    'strategy': '一次性建仓',
                    'entry_price': current_price,
                    'total_percentage': 80
                }
            else:  # medium
                return {
                    'strategy': '分批建仓',
                    'first_entry': current_price,
                    'batch_count': 2,
                    'interval_days': 5,
                    'total_percentage': 70
                }
        else:
            return {
                'strategy': '观望',
                'reason': '当前不适合建仓'
            }
    
    def _calculate_stop_loss(self, latest: Dict, risk_tolerance: str) -> float:
        """计算止损位"""
        current_price = float(latest['Close'])
        
        if risk_tolerance == 'low':
            stop_loss_percentage = 5.0
        elif risk_tolerance == 'high':
            stop_loss_percentage = 10.0
        else:  # medium
            stop_loss_percentage = 7.5
        
        return current_price * (1 - stop_loss_percentage / 100)
    
    def _calculate_take_profit(self, latest: Dict, risk_tolerance: str) -> float:
        """计算止盈位"""
        current_price = float(latest['Close'])
        
        if risk_tolerance == 'low':
            take_profit_percentage = 10.0
        elif risk_tolerance == 'high':
            take_profit_percentage = 25.0
        else:  # medium
            take_profit_percentage = 15.0
        
        return current_price * (1 + take_profit_percentage / 100)
    
    def _calculate_position_size(self, capital: float, risk_tolerance: str,
                                  recommendation: Dict) -> float:
        """计算仓位大小"""
        action = recommendation['action']
        
        base_percentage = 0.3  # 基础30%
        
        if risk_tolerance == 'low':
            base_percentage = 0.2
        elif risk_tolerance == 'high':
            base_percentage = 0.4
        
        if action in ['strong_buy', 'buy']:
            position_percentage = base_percentage
        elif action in ['strong_sell', 'sell']:
            position_percentage = 0.0
        else:
            position_percentage = base_percentage * 0.5
        
        return capital * position_percentage
    
    def _generate_risk_control(self, risk_tolerance: str) -> List[str]:
        """生成风险控制措施"""
        controls = [
            '严格执行止损',
            '控制单一股票仓位',
            '分散投资风险',
            '定期复盘调整'
        ]
        
        if risk_tolerance == 'low':
            controls.extend([
                '使用小仓位试探',
                '快速止盈止损',
                '避免追高杀跌'
            ])
        elif risk_tolerance == 'high':
            controls.extend([
                '可以承受较大波动',
                '关注长期趋势',
                '避免过度交易'
            ])
        
        return controls
    
    def _determine_time_horizon(self, investment_goal: str) -> str:
        """确定投资时间周期"""
        if investment_goal == 'growth':
            return '中短期 (3-12个月)'
        elif investment_goal == 'income':
            return '中长期 (6-24个月)'
        else:  # balance
            return '中期 (6-12个月)'
    
    def _get_monitoring_indicators(self) -> List[str]:
        """获取监控指标"""
        return [
            '价格走势',
            '成交量变化',
            'RSI指标',
            'MACD信号',
            '市场新闻',
            '行业动态'
        ]
    
    def _get_mock_news(self, symbol: str) -> List[Dict]:
        """获取模拟新闻（用于测试）"""
        return [
            {
                'title': f'{symbol} 業績超預期，股價上漲',
                'summary': '公司季度盈利增长15%，超出市场预期',
                'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'source': '财经新闻'
            },
            {
                'title': f'分析師看好{symbol}長期發展',
                'summary': '多家投行给予买入评级',
                'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'source': '证券日报'
            }
        ]
    
    def _calculate_pnl(self, holding: Dict, technical: Dict) -> Dict:
        """计算盈亏"""
        quantity = holding.get('quantity', 0)
        avg_price = holding.get('avg_price', 0)
        
        try:
            current_price = float(technical.get('价格', {}).get('收盘价', avg_price))
        except:
            current_price = avg_price
        
        invested = quantity * avg_price
        current_value = quantity * current_price
        pnl = current_value - invested
        pnl_percentage = (pnl / invested * 100) if invested > 0 else 0
        
        return {
            'invested': invested,
            'current_value': current_value,
            'pnl': pnl,
            'pnl_percentage': round(pnl_percentage, 2)
        }
    
    def _generate_risk_warnings(self, analysis: Dict) -> str:
        """生成风险提示"""
        warnings = []
        
        rec = analysis['recommendation']
        if rec['risk_level'] == '高':
            warnings.append('当前风险等级较高，建议谨慎操作')
        
        if rec['confidence'] and float(rec['confidence'].rstrip('%')) < 60:
            warnings.append('分析置信度较低，建议进一步验证')
        
        if not warnings:
            warnings.append('当前风险可控，但仍需注意市场波动')
        
        return '\n'.join(f'• {w}' for w in warnings)
    
    def _calculate_rankings(self, analyses: Dict) -> List[Dict]:
        """计算股票排名"""
        rankings = []
        
        for symbol, analysis in analyses.items():
            score = analysis['recommendation']['total_score']
            rankings.append({
                'symbol': symbol,
                'score': score,
                'action': analysis['recommendation']['action']
            })
        
        # 按分数排序
        rankings.sort(key=lambda x: x['score'], reverse=True)
        
        return rankings
    
    def _generate_comparative_recommendations(self, rankings: List[Dict]) -> Dict:
        """生成比较建议"""
        if not rankings:
            return {'message': '无比较数据'}
        
        top_stock = rankings[0]
        bottom_stock = rankings[-1]
        
        return {
            'best_performer': top_stock['symbol'],
            'worst_performer': bottom_stock['symbol'],
            'recommendation': f"建议重点关注 {top_stock['symbol']}，谨慎对待 {bottom_stock['symbol']}"
        }
    
    def _generate_portfolio_advice(self, analyses: Dict) -> Dict:
        """生成投资组合建议"""
        buy_stocks = []
        sell_stocks = []
        hold_stocks = []
        
        for symbol, data in analyses.items():
            action = data['analysis']['recommendation']['action']
            pnl = data.get('pnl', {})
            pnl_pct = pnl.get('pnl_percentage', 0)
            
            stock_advice = {
                'symbol': symbol,
                'current_action': action,
                'pnl_percentage': pnl_pct,
                'suggested_action': action
            }
            
            if action in ['buy', 'strong_buy']:
                buy_stocks.append(stock_advice)
            elif action in ['sell', 'strong_sell']:
                sell_stocks.append(stock_advice)
            else:
                hold_stocks.append(stock_advice)
        
        return {
            'buy_recommendations': buy_stocks,
            'sell_recommendations': sell_stocks,
            'hold_recommendations': hold_stocks,
            'summary': {
                'buy_count': len(buy_stocks),
                'sell_count': len(sell_stocks),
                'hold_count': len(hold_stocks)
            }
        }
