# 技术分析模块使用指南

## 📊 模块概述

技术分析模块是AI投资工具的核心组成部分，提供了专业的股票技术分析功能，包括：

### 🎯 核心功能

1. **技术指标计算** - 20+种专业技术指标
2. **交易信号生成** - 基于多指标的综合信号
3. **趋势分析** - 短中长期趋势判断
4. **机会发现** - 自动寻找买入/卖出机会
5. **股票对比** - 多股票技术指标横向对比
6. **报告生成** - 自动生成分析报告
7. **数据导出** - 支持Excel/CSV格式

## 🏗️ 模块架构

```
技术分析模块
├── indicators.py          # 技术指标计算
│   ├── 趋势指标
│   ├── 动量指标
│   ├── 成交量指标
│   └── 波动率指标
│
├── technical_analyzer.py  # 技术分析器（统一接口）
│   ├── 数据获取
│   ├── 指标计算
│   ├── 信号生成
│   └── 报告导出
│
└── examples/
    └── technical_analysis_example.py  # 使用示例
```

## 📈 支持的技术指标

### 1. 趋势指标

| 指标 | 说明 | 参数 |
|------|------|------|
| SMA | 简单移动平均线 | 周期 (5, 10, 20, 50, 200) |
| EMA | 指数移动平均线 | 周期 (12, 26) |
| 布林带 | 价格通道 | 周期20, 标准差2 |
| 肯特纳通道 | 波动性通道 | EMA周期20, ATR周期14 |

### 2. 动量指标

| 指标 | 说明 | 参数 | 范围 |
|------|------|------|------|
| RSI | 相对强弱指标 | 周期14 | 0-100 |
| MACD | 平滑异同移动平均线 | 快线12, 慢线26, 信号9 | - |
| 随机震荡 | %K和%D | %K周期14, %D周期3 | 0-100 |
| 威廉指标 | 超买超卖 | 周期14 | -100到0 |

### 3. 成交量指标

| 指标 | 说明 | 参数 |
|------|------|------|
| OBV | 能量潮指标 | - |
| 成交量MA | 成交量移动平均 | 周期20 |

### 4. 波动率指标

| 指标 | 说明 | 参数 |
|------|------|------|
| ATR | 平均真实波幅 | 周期14 |
| 肯特纳通道 | 波动性通道 | ATR倍数2.0 |

## 🚀 快速开始

### 安装依赖

```bash
cd ai-invest-tool
pip install -r requirements.txt
```

### 基本使用

```python
from src.ai_inv.technical_analyzer import TechnicalAnalyzer

# 创建分析器
analyzer = TechnicalAnalyzer()

# 分析单只股票
data = analyzer.analyze_stock('^HSI', period='1y')

# 获取交易信号
signal = analyzer.get_trading_signal('^HSI')

# 生成报告
report = analyzer.generate_report('^HSI')
print(report)
```

## 📖 详细使用指南

### 1. 基本技术分析

```python
from src.ai_inv.technical_analyzer import TechnicalAnalyzer

analyzer = TechnicalAnalyzer()

# 分析股票
data = analyzer.analyze_stock('6158.HK', period='1y')

# 查看最新数据
latest = data.iloc[-1]
print(f"收盘价: {latest['Close']:.2f}")
print(f"RSI: {latest['RSI_14']:.2f}")
print(f"信号: {latest['Signal']}")
```

### 2. 多股票分析

```python
# 分析关注列表
symbols = ['^HSI', '6158.HK', '7200.HK']
results = analyzer.analyze_watchlist(symbols, period='6m')

for symbol, data in results.items():
    latest = data.iloc[-1]
    print(f"{symbol}: {latest['Signal']} (强度: {latest['Signal_Strength']})")
```

### 3. 获取交易信号

```python
# 获取技术信号摘要
signal = analyzer.get_trading_signal('^HSI')

print("价格信息:", signal['价格'])
print("趋势指标:", signal['趋势指标'])
print("动量指标:", signal['动量指标'])
print("交易信号:", signal['交易信号'])
```

### 4. 比较多只股票

```python
# 横向对比
symbols = ['^HSI', '6158.HK', '7200.HK']
comparison = analyzer.compare_stocks(symbols)

print(comparison)
```

### 5. 寻找交易机会

```python
# 寻找买入机会
opportunities = analyzer.find_opportunities(
    symbols=symbols,
    signal_type='BUY',
    min_strength=2
)

for opp in opportunities:
    print(f"{opp['股票代码']}: {opp['信号']} (强度: {opp['强度']})")
```

### 6. 趋势分析

```python
# 分析趋势
trend = analyzer.get_trend_analysis('^HSI')

print(f"短期趋势: {trend['短期趋势']}")
print(f"中期趋势: {trend['中期趋势']}")
print(f"长期趋势: {trend['长期趋势']}")
```

### 7. 导出分析结果

```python
# 导出Excel
analyzer.export_analysis(
    symbol='^HSI',
    filepath='hsi_analysis.xlsx',
    period='1y',
    format='excel'
)

# 导出CSV
analyzer.export_analysis(
    symbol='^HSI',
    filepath='hsi_analysis.csv',
    period='1y',
    format='csv'
)
```

### 8. 生成分析报告

```python
# 自动生成报告
report = analyzer.generate_report('^HSI', period='1y')
print(report)
```

报告包含：
- 价格信息（收盘价、涨跌幅）
- 趋势指标（均线、布林带）
- 动量指标（RSI、MACD）
- 交易信号和强度
- 技术建议
- 风险提示

## 🎯 交易信号说明

### 信号类型

| 信号 | 说明 | 强度 | 建议 |
|------|------|------|------|
| STRONG BUY | 强力买入 | 4-5 | 多项指标显示强烈买入信号 |
| BUY | 买入 | 2-3 | 技术指标偏多 |
| HOLD | 观望 | 0-1 | 技术指标中性 |
| SELL | 卖出 | 2-3 | 技术指标偏空 |
| STRONG SELL | 强力卖出 | 4-5 | 多项指标显示强烈卖出信号 |

### 信号生成逻辑

交易信号基于以下指标综合判断：

1. **RSI信号**
   - RSI < 30: 超卖，买入信号
   - RSI > 70: 超买，卖出信号

2. **MACD信号**
   - MACD柱状图由负转正: 金叉，买入
   - MACD柱状图由正转负: 死叉，卖出

3. **均线信号**
   - 短期均线上穿长期均线: 金叉，买入
   - 短期均线下穿长期均线: 死叉，卖出

4. **布林带信号**
   - 价格触及下轨: 买入
   - 价格触及上轨: 卖出

5. **成交量确认**
   - 大成交量伴随信号: 加强信号强度

## 🔧 高级功能

### 1. 计算特定指标

```python
from src.ai_inv.indicators import TechnicalIndicators

ti = TechnicalIndicators()

# 只计算RSI
data = ti.rsi(data, period=14)

# 只计算MACD
data = ti.macd(data, fast_period=12, slow_period=26, signal_period=9)
```

### 2. 自定义指标参数

```python
# 自定义布林带
data = ti.bollinger_bands(data, period=10, std_dev=1.5)

# 自定义RSI
data = ti.rsi(data, period=21)
```

### 3. 批量分析

```python
# 批量分析100只股票
symbols = [f"{code:04d}.HK" for code in range(1, 101)]
results = analyzer.analyze_watchlist(symbols)
```

## 📊 数据导出格式

### Excel导出

导出的Excel文件包含以下列：

**基础数据**：
- Date, Open, High, Low, Close, Volume

**趋势指标**：
- SMA_5, SMA_10, SMA_20, SMA_50, SMA_200
- EMA_12, EMA_26
- BB_Upper, BB_Middle, BB_Lower, BB_Width

**动量指标**：
- RSI_14
- MACD, MACD_Signal, MACD_Histogram
- Stoch_K, Stoch_D
- Williams_R

**成交量指标**：
- OBV, OBV_MA
- Volume_MA_20

**波动率指标**：
- ATR
- KC_Upper, KC_Middle, KC_Lower

**交易信号**：
- Signal, Signal_Strength

## 💡 最佳实践

### 1. 数据周期选择

| 周期 | 适用场景 |
|------|----------|
| 1m | 日内交易 |
| 5m | 短线交易 |
| 1h | 日内趋势 |
| 1d | 短中线交易 |
| 1w | 中长线投资 |
| 1M | 长线投资 |

### 2. 指标组合建议

**短线交易**：
- RSI(14) + MACD + 布林带

**中线交易**：
- SMA(5,20) + MACD + 成交量

**长线投资**：
- SMA(20,50,200) + 趋势分析

### 3. 信号确认

- 单一指标信号需谨慎
- 多指标共振信号更可靠
- 成交量配合加强信号可信度

### 4. 风险控制

- 设置止损位
- 分批建仓
- 控制仓位比例

## ⚠️ 注意事项

### 1. 数据限制

- 免费数据源有请求限制
- 建议使用缓存机制
- 避免频繁API调用

### 2. 指标局限

- 技术指标仅供参考
- 不能保证100%准确
- 需结合基本面分析

### 3. 市场风险

- 市场存在不确定性
- 过度依赖技术指标有风险
- 需要风险管理策略

## 🔍 故障排除

### 问题1: 无法获取数据

**解决方案**：
1. 检查网络连接
2. 确认股票代码格式正确
3. 检查数据源API是否正常

### 问题2: 指标计算错误

**解决方案**：
1. 确认数据包含必要的列（OHLCV）
2. 检查数据是否为空
3. 验证参数是否在合理范围内

### 问题3: 信号不准确

**解决方案**：
1. 增加分析数据量
2. 调整指标参数
3. 结合多个指标判断
4. 添加成交量确认

## 📚 相关文档

- [README.md](README.md) - 项目总览
- [DATA_MODULE_GUIDE.md](DATA_MODULE_GUIDE.md) - 数据模块指南
- [BACKTEST_ENGINE_GUIDE.md](BACKTEST_ENGINE_GUIDE.md) - 回测引擎指南（待完成）

## 🆘 获取帮助

如果遇到问题：

1. 查看示例代码 `examples/technical_analysis_example.py`
2. 检查日志输出
3. 查阅本指南的故障排除部分
4. 参考技术指标文档

## 📈 更新日志

### v1.0.0 (2026-03-13)

- ✅ 实现基础技术指标（SMA, EMA, 布林带, RSI, MACD等）
- ✅ 实现交易信号生成
- ✅ 实现趋势分析
- ✅ 实现多股票对比
- ✅ 实现机会发现
- ✅ 实现报告生成
- ✅ 实现数据导出

---

**技术分析模块** - 让投资分析更专业、更高效！
