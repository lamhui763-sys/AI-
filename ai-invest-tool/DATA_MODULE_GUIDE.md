# Data Module Documentation
## 数据模块文档

**版本**: 1.0.0
**最后更新**: 2026-03-12
**作者**: WorkBuddy AI

---

## 📋 目录

1. [模块概述](#模块概述)
2. [架构设计](#架构设计)
3. [核心功能](#核心功能)
4. [使用指南](#使用指南)
5. [API参考](#api参考)
6. [最佳实践](#最佳实践)
7. [故障排除](#故障排除)

---

## 模块概述

数据模块负责AI投资工具的所有数据相关功能，包括数据获取、处理、存储和管理。

### 核心组件

| 组件 | 文件 | 职责 |
|------|------|------|
| **DataFetcher** | data_fetcher.py | 从Yahoo Finance、Alpha Vantage等数据源获取数据 |
| **DataProcessor** | data_processor.py | 数据清洗、转换、存储和导出 |
| **DataManager** | data_manager.py | 统一接口，管理数据获取和处理流程 |

### 主要特性

- ✅ **多数据源支持**: Yahoo Finance、Alpha Vantage
- ✅ **智能缓存**: 30分钟缓存，减少API调用
- ✅ **数据清洗**: 自动处理缺失值、异常值
- ✅ **技术特征**: 自动添加收益率、波动率等技术指标
- ✅ **SQLite存储**: 本地数据库存储，支持历史数据
- ✅ **数据质量检查**: 完整性、一致性、新鲜度评估
- ✅ **Excel集成**: 支持导出到Excel格式

---

## 架构设计

### 数据流

```
数据源 (Yahoo, Alpha Vantage)
    ↓
DataFetcher (获取原始数据)
    ↓
DataProcessor (清洗和转换)
    ├── 数据清洗
    ├── 特征工程
    └── 质量检查
    ↓
DataManager (统一接口)
    ├── 缓存管理
    ├── 数据库存储
    └── API提供服务
```

### 数据模型

#### Stock Data (股票数据)

```sql
CREATE TABLE stock_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    symbol TEXT NOT NULL,
    date TEXT NOT NULL,
    open REAL,
    high REAL,
    low REAL,
    close REAL,
    volume INTEGER,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(symbol, date)
);
```

#### Stock Info (股票信息)

```sql
CREATE TABLE stock_info (
    symbol TEXT PRIMARY KEY,
    name TEXT,
    sector TEXT,
    industry TEXT,
    market_cap REAL,
    pe_ratio REAL,
    dividend_yield REAL,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
);
```

#### Analysis Results (分析结果)

```sql
CREATE TABLE analysis_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    symbol TEXT NOT NULL,
    analysis_type TEXT NOT NULL,
    analysis_date TEXT NOT NULL,
    result_data TEXT NOT NULL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
```

---

## 核心功能

### 1. 数据获取 (DataFetcher)

#### 支持的数据源

| 数据源 | 状态 | 优势 | 限制 |
|--------|------|------|------|
| **Yahoo Finance** | ✅ 免费，实时 | 请求限制较低 |
| **Alpha Vantage** | ✅ 高质量，丰富数据 | 免费版有限制 |

#### 功能特性

```python
# 获取实时数据
fetcher = DataFetcher(config)
data = fetcher.fetch_stock_data('6158.HK', period='1y', interval='1d')

# 获取历史数据
historical_data = fetcher.fetch_historical_data('6158.HK', '2023-01-01', '2024-01-01')

# 获取当前价格
current_price = fetcher.get_current_price('6158.HK')

# 获取股票信息
stock_info = fetcher.get_stock_info('6158.HK')
```

### 2. 数据处理 (DataProcessor)

#### 数据清洗

- ✅ 缺失值处理（前向填充、后向填充）
- ✅ 异常值检测和修正
- ✅ 价格一致性检查（High ≥ Low）
- ✅ 重复数据处理
- ✅ 排序和索引优化

#### 特征工程

```python
# 基础收益率
df['returns'] = df['Close'].pct_change()
df['log_returns'] = np.log(df['Close'] / df['Close'].shift(1))

# 波动率
df['volatility'] = df['returns'].rolling(window=20).std()

# 技术指标
df['SMA_5'] = df['Close'].rolling(window=5).mean()
df['EMA_12'] = df['Close'].ewm(span=12).mean()

# 时间特征
df['day_of_week'] = df.index.dayofweek
df['month'] = df.index.month
```

### 3. 数据管理 (DataManager)

#### 统一接口

```python
# 初始化
manager = DataManager(config)

# 获取股票数据（自动清洗、缓存、存储）
data = manager.get_stock_data('6158.HK', period='1y', interval='1d')

# 获取多只股票
results = manager.get_multiple_stocks(['6158.HK', '7200.HK'])

# 获取数据摘要
summary = manager.get_data_summary('6158.HK')

# 导出数据
file_path = manager.export_data('6158.HK', format='excel')
```

---

## 使用指南

### 快速开始

#### 1. 基本使用

```python
from ai_inv.data_manager import DataManager

# 配置
config = {
    'yahoo_finance': {'enabled': True, 'timeout': 30},
    'hk_stocks': {
        'watchlist': ['6158.HK', '7200.HK'],
        'default_period': '1y',
        'default_interval': '1d'
    },
    'database': {'path': './data/investment.db'}
}

# 初始化
manager = DataManager(config)

# 获取数据
data = manager.get_stock_data('6158.HK')
print(f"获取到 {len(data)} 条数据")
print(f"当前价格: {data['Close'].iloc[-1]:.2f}")
```

#### 2. 批量获取

```python
# 获取关注列表
results = manager.get_watchlist_data()

# 遍历结果
for symbol, data in results.items():
    print(f"{symbol}: {data['Close'].iloc[-1]:.2f}")
```

#### 3. 数据导出

```python
# 导出到Excel
excel_file = manager.export_data('6158.HK', format='excel')

# 导出到CSV
csv_file = manager.export_data('6158.HK', format='csv')
```

### 高级用法

#### 1. 自定义数据源

```python
# 使用Alpha Vantage
config['alpha_vantage'] = {
    'api_key': 'your-api-key',
    'output_size': 'full'
}

manager = DataManager(config)
```

#### 2. 缓存控制

```python
# 使用缓存
data = manager.get_stock_data('6158.HK', use_cache=True)

# 强制刷新
data = manager.get_stock_data('6158.HK', force_refresh=True)

# 清除缓存
manager.refresh_cache('6158.HK')
```

#### 3. 数据维护

```python
# 执行维护（备份和清理）
manager.maintenance()

# 清理旧数据
deleted = manager.processor.clean_old_data(days_to_keep=365)
print(f"删除了 {deleted} 条旧记录")
```

---

## API参考

### DataManager API

#### `get_stock_data(symbol, period='1y', interval='1d', use_cache=True, force_refresh=False)`

获取股票数据（统一接口）

**参数**:
- `symbol` (str): 股票代码
- `period` (str): 时间周期 ('1y', '2y', '5y', 'max')
- `interval` (str): 数据间隔 ('1d', '1wk', '1mo')
- `use_cache` (bool): 是否使用缓存
- `force_refresh` (bool): 强制刷新

**返回**:
- `pd.DataFrame`: 股票数据（已清洗和转换）
- `None`: 获取失败

**示例**:
```python
data = manager.get_stock_data('6158.HK', period='1y', interval='1d')
```

#### `get_historical_data(symbol, start_date, end_date=None)`

获取历史数据

**参数**:
- `symbol` (str): 股票代码
- `start_date` (str): 开始日期 (YYYY-MM-DD)
- `end_date` (str): 结束日期 (YYYY-MM-DD)

**返回**:
- `pd.DataFrame`: 历史数据

**示例**:
```python
data = manager.get_historical_data('6158.HK', '2023-01-01', '2024-01-01')
```

#### `get_data_summary(symbol)`

获取数据摘要

**参数**:
- `symbol` (str): 股票代码

**返回**:
- `dict`: 数据摘要信息

**示例**:
```python
summary = manager.get_data_summary('6158.HK')
print(summary['data_quality']['completeness'])
```

---

## 最佳实践

### 1. 性能优化

```python
# ✅ 使用缓存
data = manager.get_stock_data('6158.HK', use_cache=True)

# ✅ 批量获取
results = manager.get_multiple_stocks(symbols)

# ❌ 避免频繁请求
# for symbol in symbols:
#     data = manager.get_stock_data(symbol)  # 每次都请求网络
```

### 2. 错误处理

```python
# ✅ 正确的错误处理
try:
    data = manager.get_stock_data('6158.HK')
    if data is not None:
        # 处理数据
        pass
    else:
        # 处理无数据情况
        pass
except Exception as e:
    # 记录错误
    logger.error(f"Error: {str(e)}")
```

### 3. 数据质量

```python
# ✅ 检查数据质量
summary = manager.get_data_summary('6158.HK')
quality = summary['data_quality']

if quality['completeness'] < 90:
    print("警告: 数据完整性不足")

if quality['freshness']['status'] != 'fresh':
    print("警告: 数据不够新鲜")
```

---

## 故障排除

### 常见问题

#### Q1: 无法获取数据

**症状**: `get_stock_data()` 返回 None

**解决方案**:
1. 检查网络连接
2. 验证股票代码是否正确
3. 检查Yahoo Finance服务状态
4. 尝试不同的数据源

#### Q2: 数据不准确

**症状**: 价格数据与实际不符

**解决方案**:
1. 检查时区设置
2. 验证数据源
3. 清除缓存重新获取
4. 检查数据一致性

#### Q3: 性能慢

**症状**: 数据获取速度慢

**解决方案**:
1. 启用缓存
2. 批量获取数据
3. 调整缓存过期时间
4. 使用本地数据库

---

## 下一步

数据模块开发完成后，接下来将开发：

- [ ] 技术分析模块
- [ ] AI分析模块
- [ ] 回测引擎
- [ ] 可视化界面

---

**文档版本**: 1.0.0
**最后更新**: 2026-03-12
**维护者**: WorkBuddy AI
