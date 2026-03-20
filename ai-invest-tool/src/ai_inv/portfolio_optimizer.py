"""
投资组合优化模块
使用现代投资组合理论优化投资组合
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PortfolioOptimizer:
    """投资组合优化器"""
    
    def __init__(self, risk_free_rate: float = 0.02):
        """
        初始化投资组合优化器
        
        Args:
            risk_free_rate: 无风险利率
        """
        self.risk_free_rate = risk_free_rate
        self.logger = logger
    
    def optimize_portfolio(self, returns: pd.DataFrame,
                           method: str = 'sharpe',
                           constraints: Optional[Dict] = None) -> Dict:
        """
        优化投资组合
        
        Args:
            returns: 收益率数据 DataFrame（列名为股票代码）
            method: 优化方法 ('sharpe', 'min_variance', 'max_return', 'equal_weight')
            constraints: 约束条件
            
        Returns:
            优化结果
        """
        self.logger.info(f"开始优化投资组合，方法: {method}")
        
        # 计算统计量
        mean_returns = returns.mean()
        cov_matrix = returns.cov()
        
        num_assets = len(mean_returns)
        
        if method == 'equal_weight':
            weights = np.array([1.0 / num_assets] * num_assets)
        elif method == 'sharpe':
            weights = self._optimize_sharpe(mean_returns, cov_matrix)
        elif method == 'min_variance':
            weights = self._optimize_min_variance(mean_returns, cov_matrix)
        elif method == 'max_return':
            weights = self._optimize_max_return(mean_returns, cov_matrix, constraints)
        else:
            raise ValueError(f"未知的优化方法: {method}")
        
        # 计算组合统计
        portfolio_return = np.sum(mean_returns * weights) * 252
        portfolio_volatility = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights))) * np.sqrt(252)
        portfolio_sharpe = (portfolio_return - self.risk_free_rate) / portfolio_volatility
        
        result = {
            'weights': dict(zip(mean_returns.index, weights)),
            'expected_return': portfolio_return,
            'volatility': portfolio_volatility,
            'sharpe_ratio': portfolio_sharpe,
            'method': method
        }
        
        self.logger.info(f"投资组合优化完成")
        
        return result
    
    def _optimize_sharpe(self, mean_returns: pd.Series,
                         cov_matrix: pd.DataFrame) -> np.ndarray:
        """优化夏普比率"""
        num_assets = len(mean_returns)
        
        # 使用简化的梯度下降法
        weights = np.array([1.0 / num_assets] * num_assets)
        
        for _ in range(1000):
            # 计算梯度
            portfolio_return = np.dot(weights, mean_returns) * 252
            portfolio_vol = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights))) * np.sqrt(252)
            sharpe = (portfolio_return - self.risk_free_rate) / portfolio_vol
            
            # 计算数值梯度
            epsilon = 1e-5
            grad = np.zeros(num_assets)
            
            for i in range(num_assets):
                weights_plus = weights.copy()
                weights_plus[i] += epsilon
                
                return_plus = np.dot(weights_plus, mean_returns) * 252
                vol_plus = np.sqrt(np.dot(weights_plus.T, np.dot(cov_matrix, weights_plus))) * np.sqrt(252)
                sharpe_plus = (return_plus - self.risk_free_rate) / vol_plus
                
                grad[i] = (sharpe_plus - sharpe) / epsilon
            
            # 更新权重
            weights = weights + 0.01 * grad
            
            # 归一化
            weights = np.abs(weights)
            weights = weights / weights.sum()
        
        return weights
    
    def _optimize_min_variance(self, mean_returns: pd.Series,
                                cov_matrix: pd.DataFrame) -> np.ndarray:
        """优化最小方差"""
        num_assets = len(mean_returns)
        
        # 简化的最小方差方法
        inv_cov = np.linalg.inv(cov_matrix.values)
        ones = np.ones(num_assets)
        
        weights = np.dot(inv_cov, ones)
        weights = weights / weights.sum()
        
        return weights
    
    def _optimize_max_return(self, mean_returns: pd.Series,
                               cov_matrix: pd.DataFrame,
                               constraints: Optional[Dict]) -> np.ndarray:
        """优化最大收益"""
        max_volatility = constraints.get('max_volatility', 0.3) if constraints else 0.3
        max_volatility = max_volatility / np.sqrt(252)  # 转换为日波动率
        
        num_assets = len(mean_returns)
        
        # 找到收益最高的股票
        max_return_idx = mean_returns.argmax()
        weights = np.zeros(num_assets)
        weights[max_return_idx] = 1.0
        
        # 如果风险超过限制，使用等权重
        portfolio_vol = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
        if portfolio_vol > max_volatility:
            weights = np.array([1.0 / num_assets] * num_assets)
        
        return weights
    
    def calculate_efficient_frontier(self, returns: pd.DataFrame,
                                     num_portfolios: int = 100) -> pd.DataFrame:
        """
        计算有效前沿
        
        Args:
            returns: 收益率数据
            num_portfolios: 投资组合数量
            
        Returns:
            有效前沿数据
        """
        self.logger.info("计算有效前沿")
        
        mean_returns = returns.mean()
        cov_matrix = returns.cov()
        num_assets = len(mean_returns)
        
        results = []
        
        for _ in range(num_portfolios):
            # 随机生成权重
            weights = np.random.random(num_assets)
            weights = weights / weights.sum()
            
            # 计算组合统计
            portfolio_return = np.sum(mean_returns * weights) * 252
            portfolio_volatility = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights))) * np.sqrt(252)
            sharpe_ratio = (portfolio_return - self.risk_free_rate) / portfolio_volatility
            
            results.append({
                'return': portfolio_return,
                'volatility': portfolio_volatility,
                'sharpe_ratio': sharpe_ratio,
                'weights': weights
            })
        
        df = pd.DataFrame(results)
        
        return df
    
    def monte_carlo_simulation(self, returns: pd.DataFrame,
                                num_simulations: int = 1000,
                                num_portfolios: int = 100) -> pd.DataFrame:
        """
        蒙特卡洛模拟
        
        Args:
            returns: 收益率数据
            num_simulations: 模拟次数
            num_portfolios: 每次模拟的组合数量
            
        Returns:
            模拟结果
        """
        self.logger.info(f"开始蒙特卡洛模拟，共 {num_simulations} 次")
        
        mean_returns = returns.mean()
        cov_matrix = returns.cov()
        num_assets = len(mean_returns)
        
        results = []
        
        for _ in range(num_simulations):
            for _ in range(num_portfolios):
                # 随机生成权重
                weights = np.random.random(num_assets)
                weights = weights / weights.sum()
                
                # 计算组合统计
                portfolio_return = np.sum(mean_returns * weights) * 252
                portfolio_volatility = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights))) * np.sqrt(252)
                sharpe_ratio = (portfolio_return - self.risk_free_rate) / portfolio_volatility
                
                results.append({
                    'return': portfolio_return,
                    'volatility': portfolio_volatility,
                    'sharpe_ratio': sharpe_ratio,
                    'weights': weights
                })
        
        df = pd.DataFrame(results)
        
        self.logger.info(f"蒙特卡洛模拟完成，共 {len(df)} 个组合")
        
        return df


class RiskManager:
    """风险管理器"""
    
    def __init__(self, max_position_size: float = 0.2,
                   max_portfolio_risk: float = 0.25):
        """
        初始化风险管理器
        
        Args:
            max_position_size: 最大单只股票仓位比例
            max_portfolio_risk: 最大组合风险
        """
        self.max_position_size = max_position_size
        self.max_portfolio_risk = max_portfolio_risk
        self.logger = logger
    
    def calculate_position_size(self, capital: float, 
                                 risk_per_trade: float = 0.02,
                                 stop_loss_pct: float = 0.05) -> float:
        """
        计算仓位大小
        
        Args:
            capital: 总资金
            risk_per_trade: 每笔交易风险比例
            stop_loss_pct: 止损比例
            
        Returns:
            仓位大小
        """
        # 基于风险的仓位计算
        position_size = capital * risk_per_trade / stop_loss_pct
        
        # 限制最大仓位
        max_position = capital * self.max_position_size
        position_size = min(position_size, max_position)
        
        return position_size
    
    def check_risk(self, portfolio_value: float,
                    positions: Dict,
                    current_prices: Dict) -> Dict:
        """
        检查组合风险
        
        Args:
            portfolio_value: 组合价值
            positions: 持仓 {symbol: quantity}
            current_prices: 当前价格
            
        Returns:
            风险检查结果
        """
        warnings = []
        
        # 检查单只股票仓位
        for symbol, quantity in positions.items():
            position_value = quantity * current_prices.get(symbol, 0)
            position_pct = position_value / portfolio_value
            
            if position_pct > self.max_position_size:
                warnings.append({
                    'type': 'position_risk',
                    'symbol': symbol,
                    'message': f'{symbol} 仓位过大: {position_pct:.2%} (上限: {self.max_position_size:.2%})'
                })
        
        # 检查组合集中度
        top_positions = sorted(
            [(s, q * current_prices.get(s, 0) / portfolio_value) 
             for s, q in positions.items()],
            key=lambda x: x[1],
            reverse=True
        )
        
        if top_positions:
            top_position_pct = top_positions[0][1]
            if top_position_pct > self.max_position_size:
                warnings.append({
                    'type': 'concentration_risk',
                    'symbol': top_positions[0][0],
                    'message': f'最大持仓比例: {top_position_pct:.2%} (上限: {self.max_position_size:.2%})'
                })
        
        return {
            'has_warnings': len(warnings) > 0,
            'warnings': warnings,
            'risk_level': self._assess_risk_level(warnings)
        }
    
    def _assess_risk_level(self, warnings: List) -> str:
        """评估风险等级"""
        if len(warnings) == 0:
            return 'low'
        elif len(warnings) <= 2:
            return 'medium'
        else:
            return 'high'
    
    def generate_stop_loss(self, entry_price: float,
                           method: str = 'fixed',
                           params: Optional[Dict] = None) -> float:
        """
        生成止损价格
        
        Args:
            entry_price: 入场价格
            method: 止损方法 ('fixed', 'atr', 'trailing')
            params: 参数
            
        Returns:
            止损价格
        """
        params = params or {}
        
        if method == 'fixed':
            # 固定百分比止损
            loss_pct = params.get('loss_pct', 0.05)
            return entry_price * (1 - loss_pct)
        
        elif method == 'atr':
            # 基于ATR的止损
            atr_multiplier = params.get('atr_multiplier', 2.0)
            atr = params.get('atr', entry_price * 0.02)  # 默认ATR为价格的2%
            return entry_price - atr * atr_multiplier
        
        elif method == 'trailing':
            # 移动止损
            high_since_entry = params.get('high_since_entry', entry_price)
            trailing_pct = params.get('trailing_pct', 0.05)
            return max(entry_price, high_since_entry * (1 - trailing_pct))
        
        else:
            raise ValueError(f"未知的止损方法: {method}")


class PerformanceAnalyzer:
    """性能分析器"""
    
    def __init__(self):
        """初始化性能分析器"""
        self.logger = logger
    
    def analyze_performance(self, equity_curve: pd.DataFrame,
                            benchmark: Optional[pd.DataFrame] = None) -> Dict:
        """
        分析性能
        
        Args:
            equity_curve: 资金曲线
            benchmark: 基准数据
            
        Returns:
            性能分析结果
        """
        # 计算收益率
        returns = equity_curve['portfolio_value'].pct_change().dropna()
        
        # 基础指标
        total_return = (equity_curve['portfolio_value'].iloc[-1] / 
                       equity_curve['portfolio_value'].iloc[0] - 1) * 100
        
        annual_return = self._calculate_annual_return(equity_curve)
        volatility = returns.std() * np.sqrt(252) * 100
        
        # 风险指标
        max_drawdown = self._calculate_max_drawdown(equity_curve)
        sharpe_ratio = self._calculate_sharpe_ratio(returns)
        sortino_ratio = self._calculate_sortino_ratio(returns)
        
        # 其他指标
        calmar_ratio = annual_return / abs(max_drawdown) if max_drawdown != 0 else 0
        skewness = returns.skew()
        kurtosis = returns.kurtosis()
        
        result = {
            'return_metrics': {
                'total_return': round(total_return, 2),
                'annual_return': round(annual_return, 2),
                'volatility': round(volatility, 2)
            },
            'risk_metrics': {
                'max_drawdown': round(max_drawdown, 2),
                'sharpe_ratio': round(sharpe_ratio, 2),
                'sortino_ratio': round(sortino_ratio, 2),
                'calmar_ratio': round(calmar_ratio, 2)
            },
            'distribution_metrics': {
                'skewness': round(skewness, 2),
                'kurtosis': round(kurtosis, 2)
            }
        }
        
        # 如果有基准，计算相对指标
        if benchmark is not None:
            result['relative_metrics'] = self._calculate_relative_metrics(
                equity_curve, benchmark
            )
        
        return result
    
    def _calculate_annual_return(self, equity_curve: pd.DataFrame) -> float:
        """计算年化收益率"""
        days = (equity_curve.index[-1] - equity_curve.index[0]).days
        if days == 0:
            return 0.0
        
        total_return = equity_curve['portfolio_value'].iloc[-1] / equity_curve['portfolio_value'].iloc[0]
        annual_return = (total_return ** (365.0 / days) - 1) * 100
        
        return annual_return
    
    def _calculate_max_drawdown(self, equity_curve: pd.DataFrame) -> float:
        """计算最大回撤"""
        rolling_max = equity_curve['portfolio_value'].expanding().max()
        drawdown = (equity_curve['portfolio_value'] - rolling_max) / rolling_max * 100
        
        return abs(drawdown.min())
    
    def _calculate_sharpe_ratio(self, returns: pd.Series,
                                 risk_free_rate: float = 0.02) -> float:
        """计算夏普比率"""
        if len(returns) == 0 or returns.std() == 0:
            return 0.0
        
        excess_return = returns.mean() - risk_free_rate / 252
        sharpe = excess_return / returns.std() * np.sqrt(252)
        
        return sharpe
    
    def _calculate_sortino_ratio(self, returns: pd.Series,
                                  risk_free_rate: float = 0.02) -> float:
        """计算索提诺比率"""
        downside_returns = returns[returns < 0]
        
        if len(downside_returns) == 0 or downside_returns.std() == 0:
            return 0.0
        
        excess_return = returns.mean() - risk_free_rate / 252
        downside_std = downside_returns.std()
        
        sortino = excess_return / downside_std * np.sqrt(252)
        
        return sortino
    
    def _calculate_relative_metrics(self, equity_curve: pd.DataFrame,
                                     benchmark: pd.DataFrame) -> Dict:
        """计算相对指标"""
        # 对齐数据
        aligned_equity = equity_curve.reindex(benchmark.index).fillna(method='ffill')
        
        # 计算相对收益
        equity_returns = aligned_equity['portfolio_value'].pct_change().dropna()
        benchmark_returns = benchmark.pct_change().dropna()
        
        # Alpha和Beta
        cov_matrix = np.cov(equity_returns, benchmark_returns)
        beta = cov_matrix[0, 1] / cov_matrix[1, 1]
        alpha = equity_returns.mean() - beta * benchmark_returns.mean()
        
        # 信息比率
        excess_returns = equity_returns - benchmark_returns
        information_ratio = excess_returns.mean() / excess_returns.std() * np.sqrt(252)
        
        return {
            'beta': round(beta, 2),
            'alpha': round(alpha * 252, 2),
            'information_ratio': round(information_ratio, 2)
        }
