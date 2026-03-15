# 回测引擎使用指南

## 📊 模块概述

回测引擎是AI投资工具的核心验证模块，用于基于历史数据验证交易策略的有效性：

### 🎯 核心功能

1. **策略回测** - 验证交易策略的历史表现
2. **性能评估** - 计算收益率、风险指标
3. **策略对比** - 比较多个策略的表现
4. **参数优化** - 寻找最优策略参数
5. **风险管理** - 仓位计算、风险控制
6. **投资组合优化** - 现代投资组合理论应用
7. **性能分析** - 详细的性能指标分析

## 🏗️ 模块架构

```
回测引擎模块
├── backtester.py             # 回测引擎核心
│   ├── BacktestEngine        # 回测引擎
│   ├── Strategy              # 策略基类
│   ├── MAStrategy            # 移动平均策略
│   ├── RSIStrategy           # RSI策略
│   ├── MACDStrategy          # MACD策略
│   ├── CombinedStrategy      # 组合策略
│   └── BacktestReport        # 报告生成器
│
├── portfolio_optimizer.py    # 投资组合优化
│   ├── PortfolioOptimizer    # 投资组合优化器
│   ├── RiskManager           # 风险管理器
│   └── PerformanceAnalyzer    # 性能分析器
│
└── examples/
    └── backtest_example.py   # 使用示例
```

## 📖 详细使用指南

### 1. 基本回测

```python
from src.ai_inv.backtester import BacktestEngine, MAStrategy

# 创建回测引擎
engine = BacktestEngine(
    initial_capital=100000,  # 初始资金
    commission=0.001,       # 手续费率0.1%
    slippage=0.0005         # 滑点率0.05%
)

# 准备历史数据
data = get_historical_data('^HSI')  # 您的数据获取函数

# 创建策略
strategy = MAStrategy(short_period=5, long_period=20)

# 运行回测
results = engine.run_backtest(data, strategy)

# 查看结果
print(f"总收益率: {results['summary']['total_return']:.2f}%")
print(f"年化收益率: {results['summary']['annual_return']:.2f}%")
print(f"最大回撤: {results['summary']['max_drawdown']:.2f}%")
print(f"夏普比率: {results['summary']['sharpe_ratio']:.2f}")
```

### 2. 使用不同策略

#### 移动平均策略

```python
from src.ai_inv.backtester import MAStrategy

# 创建MA策略
strategy = MAStrategy(short_period=5, long_period=20)

# 策略逻辑：
# - 短期均线上穿长期均线 → 金叉 → 买入
# - 短期均线下穿长期均线 → 死叉 → 卖出

results = engine.run_backtest(data, strategy)
```

#### RSI策略

```python
from src.ai_inv.backtester import RSIStrategy

# 创建RSI策略
strategy = RSIStrategy(
    period=14,       # RSI周期
    oversold=30,     # 超卖阈值
    overbought=70    # 超买阈值
)

# 策略逻辑：
# - RSI从超卖区向上穿越 → 买入
# - RSI从超买区向下穿越 → 卖出

results = engine.run_backtest(data, strategy)
```

#### MACD策略

```python
from src.ai_inv.backtester import MACDStrategy

# 创建MACD策略
strategy = MACDStrategy(
    fast_period=12,    # 快线周期
    slow_period=26,    # 慢线周期
    signal_period=9    # 信号线周期
)

# 策略逻辑：
# - MACD柱状图由负转正 → 金叉 → 买入
# - MACD柱状图由正转负 → 死叉 → 卖出

results = engine.run_backtest(data, strategy)
```

#### 组合策略

```python
from src.ai_inv.backtester import CombinedStrategy

# 创建组合策略（多策略投票）
strategies = [
    MAStrategy(5, 20),
    RSIStrategy(14, 30, 70),
    MACDStrategy(12, 26, 9)
]

combined = CombinedStrategy(strategies)

# 投票机制：
# - 多数策略建议买入 → 执行买入
# - 多数策略建议卖出 → 执行卖出
# - 否则 → 观望

results = engine.run_backtest(data, combined)
```

### 3. 自定义策略

```python
from src.ai_inv.backtester import Strategy

class CustomStrategy(Strategy):
    """自定义策略"""
    
    def __init__(self, params):
        super().__init__()
        self.name = "自定义策略"
        self.params = params
    
    def generate_signal(self, data):
        """生成交易信号"""
        if len(data) < 20:
            return {'action': 'hold'}
        
        latest = data.iloc[-1]
        
        # 您的策略逻辑
        if latest['Close'] > latest['SMA_20'] and latest['RSI_14'] < 70:
            return {
                'action': 'buy',
                'symbol': 'DEFAULT',
                'quantity': 100
            }
        elif latest['Close'] < latest['SMA_20'] and latest['RSI_14'] > 30:
            return {
                'action': 'sell',
                'symbol': 'DEFAULT',
                'quantity': 100
            }
        
        return {'action': 'hold'}

# 使用自定义策略
strategy = CustomStrategy(params={})
results = engine.run_backtest(data, strategy)
```

### 4. 策略对比

```python
# 定义多个策略
strategies = [
    ('MA(5,20)', MAStrategy(5, 20)),
    ('MA(10,30)', MAStrategy(10, 30)),
    ('RSI(14)', RSIStrategy(14)),
    ('MACD(12,26,9)', MACDStrategy(12, 26, 9)),
]

results = []
for name, strategy in strategies:
    engine = BacktestEngine(initial_capital=100000)
    result = engine.run_backtest(data, strategy)
    
    results.append({
        '策略': name,
        '总收益率': result['summary']['total_return'],
        '年化收益率': result['summary']['annual_return'],
        '夏普比率': result['summary']['sharpe_ratio']
    })

# 转换为DataFrame
import pandas as pd
df = pd.DataFrame(results)
print(df)
```

### 5. 参数优化

```python
# 测试不同的参数组合
short_periods = [5, 10, 15]
long_periods = [20, 30, 40]

results = []

for short in short_periods:
    for long in long_periods:
        if short >= long:
            continue
        
        engine = BacktestEngine(initial_capital=100000)
        strategy = MAStrategy(short_period=short, long_period=long)
        result = engine.run_backtest(data, strategy)
        
        results.append({
            '短期均线': short,
            '长期均线': long,
            '收益率': result['summary']['total_return'],
            '夏普比率': result['summary']['sharpe_ratio']
        })

# 找出最优参数
df = pd.DataFrame(results)
best = df.loc[df['夏普比率'].idxmax()]
print(f"最优参数: MA({best['短期均线']}, {best['长期均线']})")
```

### 6. 风险管理

```python
from src.ai_inv.portfolio_optimizer import RiskManager

# 创建风险管理器
risk_manager = RiskManager(
    max_position_size=0.2,   # 最大单只股票仓位20%
    max_portfolio_risk=0.25  # 最大组合风险25%
)

# 计算仓位大小
position_size = risk_manager.calculate_position_size(
    capital=100000,
    risk_per_trade=0.02,  # 每笔交易风险2%
    stop_loss_pct=0.05    # 止损5%
)

print(f"建议仓位: HK${position_size:,.0f}")

# 检查组合风险
risk_check = risk_manager.check_risk(
    portfolio_value=100000,
    positions={'6158.HK': 10000, '7200.HK': 20000},
    current_prices={'6158.HK': 0.50, '7200.HK': 2.00}
)

if risk_check['has_warnings']:
    for warning in risk_check['warnings']:
        print(f"警告: {warning['message']}")

# 生成止损价格
stop_loss = risk_manager.generate_stop_loss(
    entry_price=100.0,
    method='fixed',
    params={'loss_pct': 0.05}
)

print(f"止损价: HK${stop_loss:.2f}")
```

### 7. 投资组合优化

```python
from src.ai_inv.portfolio_optimizer import PortfolioOptimizer

# 准备收益率数据
returns_df = get_returns_data()  # 您的收益率数据

# 创建优化器
optimizer = PortfolioOptimizer(risk_free_rate=0.02)

# 使用不同方法优化
result_sharpe = optimizer.optimize_portfolio(returns_df, method='sharpe')
result_min_var = optimizer.optimize_portfolio(returns_df, method='min_variance')
result_equal = optimizer.optimize_portfolio(returns_df, method='equal_weight')

# 查看结果
print(f"夏普比率优化:")
print(f"  预期年化收益: {result_sharpe['expected_return']:.2%}")
print(f"  年化波动率: {result_sharpe['volatility']:.2%}")
print(f"  夏普比率: {result_sharpe['sharpe_ratio']:.2f}")

# 显示权重分配
for symbol, weight in result_sharpe['weights'].items():
    print(f"  {symbol}: {weight:.2%}")
```

### 8. 生成回测报告

```python
from src.ai_inv.backtester import BacktestReport

# 运行回测
results = engine.run_backtest(data, strategy)

# 生成文本报告
report = BacktestReport.generate_report(
    results=results,
    strategy_name=strategy.name
)

print(report)

# 导出为Excel
BacktestReport.export_results(
    results=results,
    filepath='backtest_results.xlsx',
    format='excel'
)
```

## 📊 性能指标说明

### 收益指标

| 指标 | 说明 | 计算方法 |
|------|------|----------|
| 总收益率 | 整体收益 | (最终价值 - 初始价值) / 初始价值 |
| 年化收益率 | 年化后的收益 | (1 + 总收益率)^(365/天数) - 1 |

### 风险指标

| 指标 | 说明 | 理想值 |
|------|------|--------|
| 波动率 | 价格波动程度 | 越低越好 |
| 最大回撤 | 最大跌幅 | 越小越好 |
| 夏普比率 | 风险调整后收益 | > 1.5 优秀 |
| 索提诺比率 | 下行风险调整收益 | > 1.0 良好 |

### 其他指标

| 指标 | 说明 | 理想值 |
|------|------|--------|
| Calmar比率 | 收益/回撤比 | > 1.0 |
| 偏度 | 收益分布偏态 | 正值为好 |
| 峰度 | 收益分布峰度 | 适中 |

## 💡 最佳实践

### 1. 数据准备

```python
# 确保数据包含OHLCV列
required_columns = ['Open', 'High', 'Low', 'Close', 'Volume']

# 检查数据完整性
assert all(col in data.columns for col in required_columns)

# 处理缺失值
data = data.dropna()
```

### 2. 参数选择

```python
# 避免过拟合
# - 使用较长的历史数据
# - 使用合理的参数范围
# - 避免过多参数

# 示例：合理的参数范围
# MA: 5-200
# RSI: 10-30
# MACD: 5-50
```

### 3. 回测验证

```python
# 使用样本外数据验证
# - 训练集：前70%
# - 测试集：后30%

split = int(len(data) * 0.7)
train_data = data[:split]
test_data = data[split:]

# 在训练集上优化参数
# 在测试集上验证策略
```

### 4. 风险控制

```python
# 设置合理的止损
# - 固定百分比止损：5-10%
# - ATR止损：2-3倍ATR
# - 移动止损：追踪高点

# 控制仓位
# - 单只股票：< 20%
# - 总仓位：< 80%
```

## 🔧 高级功能

### 1. 蒙特卡洛模拟

```python
# 使用蒙特卡洛模拟评估策略稳定性
results = optimizer.monte_carlo_simulation(
    returns_df,
    num_simulations=1000,
    num_portfolios=100
)

# 分析结果
print(f"平均收益: {results['return'].mean():.2%}")
print(f"平均波动率: {results['volatility'].mean():.2%}")
print(f"平均夏普比率: {results['sharpe_ratio'].mean():.2f}")
```

### 2. 有效前沿

```python
# 计算有效前沿
frontier = optimizer.calculate_efficient_frontier(returns_df, num_portfolios=100)

# 找到最优组合
max_sharpe = frontier.loc[frontier['sharpe_ratio'].idxmax()]
print(f"最优组合夏普比率: {max_sharpe['sharpe_ratio']:.2f}")
```

### 3. 多资产回测

```python
# 回测多资产组合
symbols = ['6158.HK', '7200.HK', '^HSI']

# 获取多资产数据
multi_data = {}
for symbol in symbols:
    multi_data[symbol] = get_historical_data(symbol)

# 对齐数据
aligned_data = pd.DataFrame({
    symbol: df['Close']
    for symbol, df in multi_data.items()
}).dropna()

# 计算收益率
returns = aligned_data.pct_change().dropna()

# 优化组合
result = optimizer.optimize_portfolio(returns, method='sharpe')
```

## ⚠️ 注意事项

### 1. 回测陷阱

- **过拟合** - 过度优化导致实盘表现差
- **未来函数** - 使用了未来数据
- **交易成本** - 忽视手续费和滑点
- **市场变化** - 历史不代表未来

### 2. 实盘差异

- **流动性** - 实盘可能无法成交
- **冲击成本** - 大单交易影响价格
- **心理因素** - 回测不考虑情绪
- **市场环境** - 市场结构可能变化

### 3. 改进建议

- 使用样本外验证
- 考虑交易成本
- 模拟真实交易环境
- 定期重新评估策略

## 🔍 故障排除

### 问题1: 回测结果异常

**可能原因**:
- 数据质量问题
- 策略逻辑错误
- 参数设置不当

**解决方案**:
1. 检查数据完整性
2. 验证策略逻辑
3. 调整参数范围

### 问题2: 夏普比率过高

**可能原因**:
- 过拟合
- 忽视风险
- 计算错误

**解决方案**:
1. 使用更长的历史数据
2. 增加交易成本
3. 样本外验证

### 问题3: 交易次数过多

**可能原因**:
- 参数设置过小
- 策略过于敏感

**解决方案**:
1. 增大参数周期
2. 添加过滤条件
3. 降低交易频率

## 📚 相关文档

- [README.md](README.md) - 项目总览
- [DATA_MODULE_GUIDE.md](DATA_MODULE_GUIDE.md) - 数据模块指南
- [TECHNICAL_ANALYSIS_GUIDE.md](TECHNICAL_ANALYSIS_GUIDE.md) - 技术分析指南
- [AI_INTEGRATION_GUIDE.md](AI_INTEGRATION_GUIDE.md) - AI集成指南

## 🆘 获取帮助

如果遇到问题：

1. 查看示例代码 `examples/backtest_example.py`
2. 检查日志输出
3. 查阅本指南的故障排除部分
4. 参考量化投资文献

## 📈 更新日志

### v1.0.0 (2026-03-13)

- ✅ 实现基础回测引擎
- ✅ 实现多种交易策略（MA、RSI、MACD）
- ✅ 实现组合策略
- ✅ 实现性能评估指标
- ✅ 实现风险管理功能
- ✅ 实现投资组合优化
- ✅ 实现参数优化功能

---

**回测引擎** - 让策略验证更科学、更可靠！
