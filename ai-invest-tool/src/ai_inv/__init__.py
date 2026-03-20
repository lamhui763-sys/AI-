"""
AI Investment Tool - Main Entry Point
AI投资工具主程序

Author: WorkBuddy AI
Version: 1.0.0
Date: 2026-03-12
"""

import os
import sys
import logging
from pathlib import Path

# 嘗試導入 yaml，如果不可用則使用內置方法
try:
    import yaml
    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False
    print("Warning: PyYAML not installed. Using default configuration.")

# 移除導入以避免循環
# from .data_fetcher import DataFetcher
# from .technical_analyzer import TechnicalAnalyzer
# from .ai_analyzer import AIAnalyzer
# from .backtesting import BacktestingEngine
# from .excel_integration import ExcelIntegrator


class InvestmentTool:
    """AI投资工具主类"""

    def __init__(self, config_path='config.yaml'):
        """
        初始化投资工具

        Args:
            config_path: 配置文件路径
        """
        self.config = self._load_config(config_path)
        self._setup_logging()

        # 初始化各个模块
        self.data_fetcher = DataFetcher(self.config)
        self.technical_analyzer = TechnicalAnalyzer(self.config)
        self.ai_analyzer = AIAnalyzer(self.config)
        self.backtesting_engine = BacktestingEngine(self.config)
        self.excel_integrator = ExcelIntegrator(self.config)

        self.logger.info("AI Investment Tool initialized successfully")

    def _load_config(self, config_path):
        """加载配置文件"""
        try:
            if YAML_AVAILABLE:
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = yaml.safe_load(f)
                return config
            else:
                print(f"PyYAML not available, using default config")
                return self._get_default_config()
        except FileNotFoundError:
            print(f"配置文件 {config_path} 未找到，使用默认配置")
            return self._get_default_config()
        except Exception as e:
            print(f"加载配置文件失败: {e}，使用默认配置")
            return self._get_default_config()

    def _get_default_config(self):
        """获取默认配置"""
        return {
            'openai': {'api_key': '', 'model': 'gpt-4'},
            'hk_stocks': {
                'watchlist': ['6158.HK', '7200.HK', '^HSI'],
                'default_period': '1y',
                'default_interval': '1d'
            }
        }

    def _setup_logging(self):
        """设置日志"""
        log_level = self.config.get('logging', {}).get('level', 'INFO')
        logging.basicConfig(
            level=getattr(logging, log_level),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('./logs/ai_inv.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)

    def analyze_stock(self, symbol, period=None, interval=None):
        """
        分析单只股票

        Args:
            symbol: 股票代码 (如 '6158.HK')
            period: 时间周期 (如 '1y', '2y', '5y')
            interval: 数据间隔 (如 '1d', '1wk', '1mo')

        Returns:
            dict: 分析结果
        """
        self.logger.info(f"Analyzing stock: {symbol}")

        # 使用默认参数
        period = period or self.config['hk_stocks']['default_period']
        interval = interval or self.config['hk_stocks']['default_interval']

        try:
            # 1. 获取数据
            data = self.data_fetcher.fetch_stock_data(symbol, period, interval)

            if data is None or data.empty:
                return {'error': f'无法获取 {symbol} 的数据'}

            # 2. 技术分析
            technical_signals = self.technical_analyzer.analyze(data)

            # 3. AI分析
            ai_analysis = None
            if self.config.get('ai_analysis', {}).get('enabled', True):
                ai_analysis = self.ai_analyzer.analyze(
                    symbol, data, technical_signals
                )

            # 4. 综合建议
            recommendation = self._generate_recommendation(
                technical_signals, ai_analysis
            )

            # 5. 返回结果
            result = {
                'symbol': symbol,
                'current_price': data['Close'].iloc[-1],
                'period': period,
                'technical_indicators': technical_signals,
                'ai_analysis': ai_analysis,
                'recommendation': recommendation,
                'data': data
            }

            self.logger.info(f"Analysis completed for {symbol}")
            return result

        except Exception as e:
            self.logger.error(f"Error analyzing {symbol}: {str(e)}")
            return {'error': str(e)}

    def backtest_strategy(self, strategy, symbol, start_date, end_date=None):
        """
        回测交易策略

        Args:
            strategy: 交易策略函数
            symbol: 股票代码
            start_date: 开始日期
            end_date: 结束日期 (可选)

        Returns:
            dict: 回测结果
        """
        self.logger.info(f"Backtesting strategy on {symbol}")

        try:
            # 获取历史数据
            data = self.data_fetcher.fetch_historical_data(
                symbol, start_date, end_date
            )

            if data is None or data.empty:
                return {'error': '无法获取历史数据'}

            # 执行回测
            backtest_results = self.backtesting_engine.run(
                strategy, data, self.config['backtesting']
            )

            self.logger.info(f"Backtest completed for {symbol}")
            return backtest_results

        except Exception as e:
            self.logger.error(f"Error in backtesting: {str(e)}")
            return {'error': str(e)}

    def watchlist_analysis(self):
        """
        分析关注列表中的所有股票

        Returns:
            dict: 所有股票的分析结果
        """
        self.logger.info("Starting watchlist analysis")

        watchlist = self.config['hk_stocks']['watchlist']
        results = {}

        for symbol in watchlist:
            result = self.analyze_stock(symbol)
            results[symbol] = result

        return results

    def update_excel_reports(self):
        """更新Excel报告"""
        self.logger.info("Updating Excel reports")

        try:
            # 分析关注列表
            results = self.watchlist_analysis()

            # 更新Excel文件
            self.excel_integrator.update_reports(results)

            self.logger.info("Excel reports updated successfully")
            return True

        except Exception as e:
            self.logger.error(f"Error updating Excel: {str(e)}")
            return False

    def _generate_recommendation(self, technical_signals, ai_analysis):
        """
        生成综合投资建议

        Args:
            technical_signals: 技术分析信号
            ai_analysis: AI分析结果

        Returns:
            dict: 投资建议
        """
        # 基础分数
        score = 50

        # 技术指标评分
        if technical_signals:
            # 移动平均信号
            ma_signal = technical_signals.get('ma_signal', 'hold')
            if ma_signal == 'buy':
                score += 20
            elif ma_signal == 'sell':
                score -= 20

            # RSI信号
            rsi = technical_signals.get('rsi', 50)
            if rsi < 30:  # 超卖
                score += 15
            elif rsi > 70:  # 超买
                score -= 15

            # MACD信号
            macd_signal = technical_signals.get('macd_signal', 'hold')
            if macd_signal == 'buy':
                score += 15
            elif macd_signal == 'sell':
                score -= 15

        # AI分析调整
        if ai_analysis:
            ai_score = ai_analysis.get('score', 50)
            score = (score * 0.6) + (ai_score * 0.4)

        # 生成建议
        if score >= 75:
            action = 'strong_buy'
            sentiment = '强烈买入'
        elif score >= 60:
            action = 'buy'
            sentiment = '买入'
        elif score >= 40:
            action = 'hold'
            sentiment = '持有'
        elif score >= 25:
            action = 'sell'
            sentiment = '卖出'
        else:
            action = 'strong_sell'
            sentiment = '强烈卖出'

        return {
            'action': action,
            'sentiment': sentiment,
            'score': round(score, 2),
            'confidence': 'high' if abs(score - 50) > 20 else 'medium'
        }


def main():
    """主函数"""
    # 创建工具实例
    tool = InvestmentTool()

    # 示例：分析港股
    print("=" * 60)
    print("AI Investment Tool - 智能投资分析")
    print("=" * 60)

    # 分析6158.HK (正荣控股)
    print("\n📊 分析 6158.HK (正荣控股)")
    print("-" * 60)
    result = tool.analyze_stock('6158.HK')

    if 'error' not in result:
        print(f"当前价格: HKD {result['current_price']:.2f}")
        print(f"技术信号: {result['technical_indicators']}")
        print(f"AI分析: {result['ai_analysis']}")
        print(f"\n投资建议: {result['recommendation']['sentiment']}")
        print(f"操作建议: {result['recommendation']['action']}")
        print(f"置信度: {result['recommendation']['confidence']}")
    else:
        print(f"错误: {result['error']}")

    # 分析7200.HK (普天通信)
    print("\n" + "=" * 60)
    print("📊 分析 7200.HK (普天通信)")
    print("-" * 60)
    result = tool.analyze_stock('7200.HK')

    if 'error' not in result:
        print(f"当前价格: HKD {result['current_price']:.2f}")
        print(f"技术信号: {result['technical_indicators']}")
        print(f"AI分析: {result['ai_analysis']}")
        print(f"\n投资建议: {result['recommendation']['sentiment']}")
        print(f"操作建议: {result['recommendation']['action']}")
    else:
        print(f"错误: {result['error']}")

    # 分析HSI (恒生指数)
    print("\n" + "=" * 60)
    print("📊 分析 ^HSI (恒生指数)")
    print("-" * 60)
    result = tool.analyze_stock('^HSI')

    if 'error' not in result:
        print(f"当前点位: {result['current_price']:.2f}")
        print(f"技术信号: {result['technical_indicators']}")
        print(f"AI分析: {result['ai_analysis']}")
        print(f"\n投资建议: {result['recommendation']['sentiment']}")
        print(f"操作建议: {result['recommendation']['action']}")
    else:
        print(f"错误: {result['error']}")


if __name__ == '__main__':
    main()
