'''
回测引擎模块
基于历史数据验证交易策略的有效性
'''

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple, Type
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Strategy:
    """交易策略基类"""
    
    def __init__(self):
        """初始化策略"""
        self.name = "Base Strategy"
    
    def generate_signal(self, data: pd.DataFrame) -> Dict:
        """
        生成交易信号
        
        Args:
            data: 历史数据
            
        Returns:
            信号字典 {'action': 'buy/sell/hold', 'quantity': x}
        """
        raise NotImplementedError("子类必须实现此方法")


class BacktestEngine:
    """回测引擎"""
    
    def __init__(self, initial_capital: float = 100000.0,
                 commission: float = 0.001,
                 slippage: float = 0.0005):
        """
        初始化回测引擎
        
        Args:
            initial_capital: 初始资金
            commission: 交易手续费率
            slippage: 滑点率
        """
        self.initial_capital = initial_capital
        self.commission = commission
        self.slippage = slippage
        self.logger = logger
        
        # 回测状态
        self.current_capital = initial_capital
        self.positions = {}  # 当前持仓 {symbol: quantity}
        self.cash = initial_capital
        self.portfolio_value = initial_capital
        self.trades = []  # 交易记录
        self.equity_curve = []  # 资金曲线
        self.daily_returns = []  # 每日收益率
        
        # 重置引擎
        self.reset()
    
    def reset(self):
        """重置回测引擎"""
        self.current_capital = self.initial_capital
        self.positions = {}
        self.cash = self.initial_capital
        self.portfolio_value = self.initial_capital
        self.trades = []
        self.equity_curve = []
        self.daily_returns = []
        self.logger.info("回测引擎已重置")
    
    def run_backtest(self, data: pd.DataFrame, 
                       strategy: Strategy) -> Dict:
        """
        运行回测
        
        Args:
            data: 历史数据（OHLCV）
            strategy: 交易策略的实例对象
            
        Returns:
            回测结果
        """
        self.logger.info(f"开始回测策略: {strategy.name}")
        self.reset()
        
        # 计算技术指标 (如果需要的话，策略内部可能会依赖)
        from .indicators import TechnicalIndicators
        ti = TechnicalIndicators()
        # 确保所有策略可能需要的指标都被计算
        # 注意: 理想情况下，应仅计算特定策略所需的指标
        data = ti.calculate_all_indicators(data)
        
        # 逐日回测
        for i in range(1, len(data)):
            # 获取当前日期和价格
            date = data.index[i]
            current_price = data['Close'].iloc[i]
            
            # 计算当前组合价值
            self._calculate_portfolio_value(current_price, date)
            
            # FIX: 调用策略实例的 generate_signal 方法，而不是调用实例本身
            signal = strategy.generate_signal(data.iloc[:i+1])
            
            # 执行交易
            self._execute_trades(signal, current_price, date)
        
        # 计算最终统计
        results = self._calculate_performance_metrics()
        
        self.logger.info("回测完成")
        
        return results
    
    def _calculate_portfolio_value(self, price: float, date: datetime):
        """计算组合价值"""
        holdings_value = sum(
            quantity * self._get_current_price(symbol, price)
            for symbol, quantity in self.positions.items()
        )
        
        self.portfolio_value = self.cash + holdings_value
        
        # 记录资金曲线
        self.equity_curve.append({
            'date': date,
            'portfolio_value': self.portfolio_value,
            'cash': self.cash,
            'holdings_value': holdings_value
        })
    
    def _get_current_price(self, symbol: str, price: float) -> float:
        """获取当前价格（简化版）"""
        # 在实际应用中，这里应该获取每只股票的实时价格
        # 简化版假设所有股票使用相同价格
        return price
    
    def _execute_trades(self, signal: Dict, price: float, date: datetime):
        """执行交易"""
        if not signal or 'action' not in signal or signal['action'] == 'hold':
            return
        
        action = signal['action']
        symbol = signal.get('symbol', 'DEFAULT')
        quantity = signal.get('quantity', 0)

        if quantity <= 0:
            return
        
        # 计算滑点后的价格
        if action == 'buy':
            execution_price = price * (1 + self.slippage)
        else:
            execution_price = price * (1 - self.slippage)
        
        # 计算交易金额
        trade_value = quantity * execution_price
        commission = trade_value * self.commission
        
        # 执行买入
        if action == 'buy':
            if self.cash >= trade_value + commission:
                self.cash -= (trade_value + commission)
                self.positions[symbol] = self.positions.get(symbol, 0) + quantity
                
                self.trades.append({
                    'date': date,
                    'action': 'buy',
                    'symbol': symbol,
                    'quantity': quantity,
                    'price': execution_price,
                    'value': trade_value,
                    'commission': commission
                })
        
        # 执行卖出
        elif action == 'sell':
            current_quantity = self.positions.get(symbol, 0)
            sell_quantity = min(quantity, current_quantity)
            
            if sell_quantity > 0:
                self.cash += (sell_quantity * execution_price - commission)
                self.positions[symbol] -= sell_quantity
                if self.positions[symbol] == 0:
                    del self.positions[symbol]
                
                self.trades.append({
                    'date': date,
                    'action': 'sell',
                    'symbol': symbol,
                    'quantity': sell_quantity,
                    'price': execution_price,
                    'value': sell_quantity * execution_price,
                    'commission': commission
                })
    
    def _calculate_performance_metrics(self) -> Dict:
        """计算性能指标"""
        if not self.equity_curve:
            return self._empty_results()

        # 转换资金曲线为DataFrame
        equity_df = pd.DataFrame(self.equity_curve)
        equity_df['date'] = pd.to_datetime(equity_df['date'])
        equity_df = equity_df.set_index('date')
        
        # 计算收益率
        equity_df['daily_return'] = equity_df['portfolio_value'].pct_change()
        
        # 基础指标
        total_return = (self.portfolio_value / self.initial_capital - 1) * 100
        annual_return = self._calculate_annual_return(equity_df)
        volatility = equity_df['daily_return'].std() * np.sqrt(252) * 100
        
        # 风险指标
        max_drawdown = self._calculate_max_drawdown(equity_df)
        sharpe_ratio = self._calculate_sharpe_ratio(equity_df)
        sortino_ratio = self._calculate_sortino_ratio(equity_df)
        
        # 交易统计
        trades_df = pd.DataFrame(self.trades)
        if not trades_df.empty:
            total_trades = len(trades_df)
            buy_trades = trades_df[trades_df['action'] == 'buy']
            sell_trades = trades_df[trades_df['action'] == 'sell']
            # A simple win rate calculation based on selling higher than average buy price (can be improved)
            # This is a simplification. A real win rate needs to match buys and sells.
            winning_trades = len(sell_trades) # Placeholder logic
            win_rate = (winning_trades / len(sell_trades) * 100) if not sell_trades.empty else 0
        else:
            total_trades = 0
            winning_trades = 0
            win_rate = 0
        
        return {
            'summary': {
                'initial_capital': self.initial_capital,
                'final_capital': self.portfolio_value,
                'total_return': round(total_return, 2),
                'annual_return': round(annual_return, 2),
                'volatility': round(volatility, 2),
                'max_drawdown': round(max_drawdown, 2),
                'sharpe_ratio': round(sharpe_ratio, 2),
                'sortino_ratio': round(sortino_ratio, 2)
            },
            'trades': {
                'total_trades': total_trades,
                'winning_trades': winning_trades,
                'win_rate': round(win_rate, 2)
            },
            'equity_curve': equity_df.reset_index(),
            'trades_history': trades_df
        }

    def _empty_results(self) -> Dict:
        """返回一个空结果字典"""
        return {
            'summary': {
                'initial_capital': self.initial_capital, 'final_capital': self.initial_capital,
                'total_return': 0, 'annual_return': 0, 'volatility': 0, 'max_drawdown': 0,
                'sharpe_ratio': 0, 'sortino_ratio': 0
            },
            'trades': {'total_trades': 0, 'winning_trades': 0, 'win_rate': 0},
            'equity_curve': pd.DataFrame(), 'trades_history': pd.DataFrame()
        }

    def _calculate_annual_return(self, equity_df: pd.DataFrame) -> float:
        """计算年化收益率"""
        if len(equity_df) < 2:
            return 0.0
        
        days = (equity_df.index[-1] - equity_df.index[0]).days
        if days == 0:
            return 0.0
        
        total_return = equity_df['portfolio_value'].iloc[-1] / self.initial_capital
        annual_return = (total_return ** (365.0 / days) - 1) * 100
        
        return annual_return
    
    def _calculate_max_drawdown(self, equity_df: pd.DataFrame) -> float:
        """计算最大回撤"""
        if len(equity_df) < 2:
            return 0.0
        
        rolling_max = equity_df['portfolio_value'].expanding().max()
        drawdown = (equity_df['portfolio_value'] - rolling_max) / rolling_max * 100
        
        return abs(drawdown.min())
    
    def _calculate_sharpe_ratio(self, equity_df: pd.DataFrame, 
                                 risk_free_rate: float = 0.02) -> float:
        """计算夏普比率"""
        returns = equity_df['daily_return'].dropna()
        
        if len(returns) < 2 or returns.std() == 0:
            return 0.0
        
        excess_return = returns.mean() - risk_free_rate / 252
        sharpe = excess_return / returns.std() * np.sqrt(252)
        
        return sharpe
    
    def _calculate_sortino_ratio(self, equity_df: pd.DataFrame,
                                 risk_free_rate: float = 0.02) -> float:
        """计算索提诺比率"""
        returns = equity_df['daily_return'].dropna()
        
        if len(returns) < 2:
            return 0.0
        
        downside_returns = returns[returns < 0]
        if len(downside_returns) == 0 or downside_returns.std() == 0:
            return 0.0
        
        excess_return = returns.mean() - risk_free_rate / 252
        downside_std = downside_returns.std()
        
        sortino = excess_return / downside_std * np.sqrt(252)
        
        return sortino


class MAStrategy(Strategy):
    """移动平均策略"""
    
    def __init__(self, short_period: int = 5, long_period: int = 20):
        """
        初始化移动平均策略
        
        Args:
            short_period: 短期均线周期
            long_period: 长期均线周期
        """
        super().__init__()
        self.name = f"MA({short_period},{long_period})"
        self.short_period = short_period
        self.long_period = long_period
    
    def generate_signal(self, data: pd.DataFrame) -> Dict:
        """生成移动平均交叉信号"""
        # 确保指标名称与 indicators.py 中生成的一致
        short_ma_col = f'SMA_{self.short_period}'
        long_ma_col = f'SMA_{self.long_period}'

        if len(data) < self.long_period or short_ma_col not in data.columns or long_ma_col not in data.columns:
            return {'action': 'hold'}
        
        latest = data.iloc[-1]
        prev = data.iloc[-2]
        
        # 安全地获取指标
        short_ma = latest.get(short_ma_col)
        long_ma = latest.get(long_ma_col)
        prev_short_ma = prev.get(short_ma_col)
        prev_long_ma = prev.get(long_ma_col)

        if short_ma is None or long_ma is None or prev_short_ma is None or prev_long_ma is None:
             return {'action': 'hold'}
        
        # 金叉：短期均线上穿长期均线
        if short_ma > long_ma and prev_short_ma <= prev_long_ma:
            return {
                'action': 'buy',
                'symbol': 'DEFAULT',
                'quantity': 100  # 固定数量
            }
        
        # 死叉：短期均线下穿长期均线
        elif short_ma < long_ma and prev_short_ma >= prev_long_ma:
            # 卖出所有持仓
            return {
                'action': 'sell',
                'symbol': 'DEFAULT',
                'quantity': 100  # 固定数量
            }
        
        return {'action': 'hold'}


class RSIStrategy(Strategy):
    """RSI策略"""
    
    def __init__(self, period: int = 14, oversold: float = 30.0, overbought: float = 70.0):
        """
        初始化RSI策略
        
        Args:
            period: RSI周期
            oversold: 超卖阈值
            overbought: 超买阈值
        """
        super().__init__()
        self.name = f"RSI({period})"
        self.period = period
        self.oversold = oversold
        self.overbought = overbought
    
    def generate_signal(self, data: pd.DataFrame) -> Dict:
        """生成RSI信号"""
        rsi_col = f'RSI_{self.period}'
        if len(data) < self.period or rsi_col not in data.columns:
            return {'action': 'hold'}
        
        latest = data.iloc[-1]
        prev = data.iloc[-2]
        
        rsi = latest.get(rsi_col, 50)
        prev_rsi = prev.get(rsi_col, 50)
        
        # RSI从超卖区向上穿越
        if rsi > self.oversold and prev_rsi <= self.oversold:
            return {
                'action': 'buy',
                'symbol': 'DEFAULT',
                'quantity': 100
            }
        
        # RSI从超买区向下穿越
        elif rsi < self.overbought and prev_rsi >= self.overbought:
            return {
                'action': 'sell',
                'symbol': 'DEFAULT',
                'quantity': 100
            }
        
        return {'action': 'hold'}


class MACDStrategy(Strategy):
    """MACD策略"""
    
    def __init__(self, fast_period: int = 12, slow_period: int = 26, signal_period: int = 9):
        """
        初始化MACD策略
        
        Args:
            fast_period: 快线周期
            slow_period: 慢线周期
            signal_period: 信号线周期
        """
        super().__init__()
        self.name = f"MACD({fast_period},{slow_period},{signal_period})"
        self.fast_period = fast_period
        self.slow_period = slow_period
        self.signal_period = signal_period
    
    def generate_signal(self, data: pd.DataFrame) -> Dict:
        """生成MACD信号"""
        hist_col = 'MACD_Histogram'
        if len(data) < self.slow_period + self.signal_period or hist_col not in data.columns:
            return {'action': 'hold'}
        
        latest = data.iloc[-1]
        prev = data.iloc[-2]
        
        macd_hist = latest.get(hist_col)
        prev_macd_hist = prev.get(hist_col)

        if macd_hist is None or prev_macd_hist is None:
            return {'action': 'hold'}
        
        # MACD柱状图由负转正（金叉）
        if macd_hist > 0 and prev_macd_hist <= 0:
            return {
                'action': 'buy',
                'symbol': 'DEFAULT',
                'quantity': 100
            }
        
        # MACD柱状图由正转负（死叉）
        elif macd_hist < 0 and prev_macd_hist >= 0:
            return {
                'action': 'sell',
                'symbol': 'DEFAULT',
                'quantity': 100
            }
        
        return {'action': 'hold'}


class CombinedStrategy(Strategy):
    """组合策略"""
    
    def __init__(self, strategies: List[Strategy], weights: Optional[List[float]] = None):
        """
        初始化组合策略
        
        Args:
            strategies: 策略列表
            weights: 权重列表
        """
        super().__init__()
        self.name = "Combined"
        self.strategies = strategies
        
        if weights is None:
            self.weights = [1.0 / len(strategies)] * len(strategies)
        else:
            self.weights = weights
    
    def generate_signal(self, data: pd.DataFrame) -> Dict:
        """生成组合信号"""
        buy_votes = 0
        sell_votes = 0
        
        for strategy in self.strategies:
            signal = strategy.generate_signal(data)
            
            if signal['action'] == 'buy':
                buy_votes += 1
            elif signal['action'] == 'sell':
                sell_votes += 1
        
        # 投票机制
        if buy_votes > len(self.strategies) / 2:
            return {
                'action': 'buy',
                'symbol': 'DEFAULT',
                'quantity': 100
            }
        elif sell_votes > len(self.strategies) / 2:
            return {
                'action': 'sell',
                'symbol': 'DEFAULT',
                'quantity': 100
            }
        
        return {'action': 'hold'}


class BacktestReport:
    """回测报告生成器"""
    
    @staticmethod
    def generate_report(results: Dict, strategy_name: str) -> str:
        """
        生成回测报告
        
        Args:
            results: 回测结果
            strategy_name: 策略名称
            
        Returns:
            格式化的报告
        """
        summary = results['summary']
        trades = results['trades']
        
        report = f"""
{'='*70}
回测报告 - {strategy_name}
{'='*70}

报告生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

{'='*70}
一、收益指标
{'='*70}

初始资金: HK${summary['initial_capital']:,.2f}
最终资金: HK${summary['final_capital']:,.2f}
总收益率: {summary['total_return']:.2f}%
年化收益率: {summary['annual_return']:.2f}%

{'='*70}
二、风险指标
{'='*70}

波动率: {summary['volatility']:.2f}%
最大回撤: {summary['max_drawdown']:.2f}%
夏普比率: {summary['sharpe_ratio']:.2f}
索提诺比率: {summary['sortino_ratio']:.2f}

{'='*70}
三、交易统计
{'='*70}

总交易次数: {trades['total_trades']}
盈利交易次数: {trades['winning_trades']}
胜率: {trades['win_rate']:.2f}%

{'='*70}
四、评估
{'='*70}
"""
        
        # 添加评估
        if summary['total_return'] > 20:
            report += "表现优秀！总收益率超过20%\n"
        elif summary['total_return'] > 10:
            report += "表现良好。总收益率在10%-20%之间\n"
        elif summary['total_return'] > 0:
            report += "表现一般。总收益率在0%-10%之间\n"
        else:
            report += "表现不佳。总收益率为负\n"
        
        if summary['sharpe_ratio'] > 1.5:
            report += "风险调整后收益优秀（夏普比率 > 1.5）\n"
        elif summary['sharpe_ratio'] > 1.0:
            report += "风险调整后收益良好（夏普比率 > 1.0）\n"
        else:
            report += "风险调整后收益一般（夏普比率 <= 1.0）\n"
        
        if summary['max_drawdown'] < 10:
            report += "风险控制优秀（最大回撤 < 10%）\n"
        elif summary['max_drawdown'] < 20:
            report += "风险控制良好（最大回撤 < 20%）\n"
        else:
            report += "风险控制有待改进（最大回撤 >= 20%）\n"
        
        report += f"\n{'='*70}\n"
        
        return report
    
    @staticmethod
    def export_results(results: Dict, filepath: str, format: str = 'excel'):
        """
        导出回测结果
        
        Args:
            results: 回测结果
            filepath: 文件路径
            format: 格式（excel/csv）
        """
        equity_df = results['equity_curve']
        trades_df = results['trades_history']
        
        if format == 'excel':
            with pd.ExcelWriter(filepath) as writer:
                equity_df.to_excel(writer, sheet_name='资金曲线', index=False)
                trades_df.to_excel(writer, sheet_name='交易记录', index=False)
        elif format == 'csv':
            equity_df.to_csv(filepath.replace('.csv', '_equity.csv'), index=False)
            trades_df.to_csv(filepath.replace('.csv', '_trades.csv'), index=False)
