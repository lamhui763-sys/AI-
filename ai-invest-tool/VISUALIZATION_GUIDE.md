# 可视化界面模块使用指南

## 📖 目录

1. [模块概述](#模块概述)
2. [快速开始](#快速开始)
3. [Excel可视化](#excel可视化)
4. [Web界面](#web界面)
5. [使用示例](#使用示例)
6. [图表类型](#图表类型)
7. [高级功能](#高级功能)
8. [最佳实践](#最佳实践)
9. [故障排除](#故障排除)

---

## 模块概述

### 功能特性

AI投资工具提供两种可视化方式：

#### 1. **Excel可视化**
- ✅ 自动生成专业的Excel报表
- ✅ 多工作表组织
- ✅ 自动格式化
- ✅ 图表支持
- ✅ 数据导出

#### 2. **Web界面**
- ✅ 交互式Web仪表板
- ✅ 实时数据更新
- ✅ 丰富的图表
- ✅ 响应式设计
- ✅ Excel导出集成

### 支持的报告类型

| 报告类型 | 功能 | 工作表 |
|---------|------|-------|
| 股票分析报告 | 单股票完整分析 | 价格数据、技术指标、交易信号、AI分析、摘要 |
| 回测报告 | 策略回测结果 | 回测摘要、交易记录、资金曲线、性能指标 |
| 投资组合报告 | 投资组合分析 | 组合概览、持仓详情、收益分析、风险分析 |

---

## 快速开始

### 安装依赖

```bash
# Excel可视化依赖
pip install openpyxl

# Web界面依赖
pip install streamlit plotly

# 安装所有依赖
pip install openpyxl streamlit plotly
```

### 基本使用

#### Excel报表

```python
from src.ai_inv.excel_visualizer import ExcelVisualizer
from src.ai_inv.technical_analyzer import TechnicalAnalyzer

# 创建可视化器
visualizer = ExcelVisualizer(output_dir='output/excel')

# 创建分析器
analyzer = TechnicalAnalyzer()

# 分析股票
data = analyzer.analyze_stock('^HSI', period='1y')

# 生成报告
filepath = visualizer.generate_stock_report(
    symbol='^HSI',
    price_data=data['data'],
    indicators=data['indicators']
)

print(f"报告已生成: {filepath}")
```

#### Web界面

```bash
# 启动Web界面
cd ai-invest-tool
streamlit run src/ai_inv/web_dashboard.py

# 浏览器访问
http://localhost:8501
```

---

## Excel可视化

### 1. 股票分析报告

#### 基本用法

```python
from src.ai_inv.excel_visualizer import ExcelVisualizer
from src.ai_inv.data_fetcher import DataFetcher
from src.ai_inv.indicators import TechnicalIndicators

# 创建可视化器
visualizer = ExcelVisualizer(output_dir='output/excel')

# 获取数据
fetcher = DataFetcher()
data = fetcher.get_historical_data('^HSI', period='1y')

# 计算指标
indicators = TechnicalIndicators().calculate_all_indicators(data)

# 生成报告
filepath = visualizer.generate_stock_report(
    symbol='^HSI',
    price_data=data,
    indicators=indicators,
    filename='hsi_report.xlsx'  # 可选
)
```

#### 报告内容

**工作表1: 价格数据**
- 日期、开盘价、最高价、最低价、收盘价、成交量
- 自动列宽调整
- 标题格式化

**工作表2: 技术指标**
- 所有技术指标
- 布林带（上轨、中轨、下轨）
- RSI、MACD、MA等

**工作表3: 交易信号**
- 日期、信号类型、强度
- 信号说明

**工作表4: AI分析**（可选）
- AI建议
- 置信度
- 市场情感

**工作表5: 摘要**
- 基本信息
- 技术指标摘要
- AI分析摘要

### 2. 回测报告

```python
from src.ai_inv.backtester import BacktestEngine, MAStrategy
from src.ai_inv.excel_visualizer import ExcelVisualizer

# 创建回测引擎
engine = BacktestEngine(
    initial_capital=100000,
    commission=0.001
)

# 创建策略
strategy = MAStrategy(short_period=5, long_period=20)

# 运行回测
results = engine.run_backtest(data, strategy)

# 生成报告
visualizer = ExcelVisualizer()
filepath = visualizer.generate_backtest_report(
    results=results,
    strategy_name='MA_5_20'
)
```

#### 回测报告内容

**工作表1: 回测摘要**
- 策略名称、回测期间
- 收益指标（总收益、年化收益）
- 风险指标（最大回撤、夏普比率）
- 交易统计（胜率、盈亏比）

**工作表2: 交易记录**
- 买入/卖出日期
- 价格、股数
- 盈亏金额和百分比

**工作表3: 资金曲线**
- 每日资金变化

**工作表4: 性能指标**
- 详细性能指标
- 收益、风险、风险调整收益

### 3. 投资组合报告

```python
# 创建投资组合数据
portfolio_data = {
    'total_value': 1000000,
    'total_pnl': 50000,
    'total_return': 5.0,
    'num_holdings': 5,
    'date': '2024-01-15',
    'holdings': holdings_df,  # 持仓DataFrame
    'returns': returns_df,    # 收益DataFrame
    'risk_analysis': risk_dict  # 风险分析字典
}

# 生成报告
visualizer = ExcelVisualizer()
filepath = visualizer.generate_portfolio_report(
    portfolio_data=portfolio_data
)
```

---

## Web界面

### 1. 启动Web界面

```bash
# 方法1: 使用streamlit命令
streamlit run src/ai_inv/web_dashboard.py

# 方法2: 指定端口
streamlit run src/ai_inv/web_dashboard.py --server.port 8501

# 方法3: 自动刷新
streamlit run src/ai_inv/web_dashboard.py --server.runOnSave true
```

### 2. 页面功能

#### 股票分析页面
- 输入股票代码
- 选择时间周期
- 查看价格图表
- 技术指标可视化
- 交易信号显示
- 导出Excel

#### 技术分析页面
- 选择技术指标
- 自定义指标参数
- 交互式图表
- 实时更新
- 导出功能

#### AI分析页面
- 配置OpenAI API
- 基础AI分析
- 情感分析
- 智能顾问
- 投资计划生成

#### 回测引擎页面
- 策略选择
- 参数配置
- 回测执行
- 结果可视化
- 交易记录
- 性能指标

#### 投资组合页面
- 添加持仓
- 实时更新
- 组合统计
- 持仓分布饼图
- 盈亏分析

#### 新闻分析页面
- 输入新闻文本
- 情感分析
- 关键词提取
- 情感评分

### 3. Web界面特性

#### 交互式图表
- 缩放和平移
- 悬停显示详情
- 多图表联动
- 自定义样式

#### 响应式设计
- 适配不同屏幕
- 移动端支持
- 自动调整布局

#### 数据导出
- 一键导出Excel
- PDF打印支持
- CSV下载

---

## 使用示例

### 示例1: 基本Excel报告

```python
from src.ai_inv.excel_visualizer import ExcelVisualizer
from src.ai_inv.technical_analyzer import TechnicalAnalyzer

visualizer = ExcelVisualizer()
analyzer = TechnicalAnalyzer()

# 分析恒生指数
data = analyzer.analyze_stock('^HSI', period='1y')

# 生成报告
filepath = visualizer.generate_stock_report(
    symbol='^HSI',
    price_data=data['data'],
    indicators=data['indicators']
)
```

### 示例2: 批量生成报告

```python
symbols = ['^HSI', '6158.HK', '7200.HK']

for symbol in symbols:
    data = analyzer.analyze_stock(symbol, period='6mo')
    
    filepath = visualizer.generate_stock_report(
        symbol=symbol,
        price_data=data['data'],
        indicators=data['indicators']
    )
    
    print(f"✅ {symbol} 报告已生成")
```

### 示例3: 包含AI分析的报告

```python
from src.ai_inv.ai_analyzer import AIAnalyzer

# AI分析
ai_analyzer = AIAnalyzer()
ai_result = ai_analyzer.analyze_stock_with_ai(
    symbol='^HSI',
    technical_data=data['summary']
)

# 生成包含AI分析的报告
filepath = visualizer.generate_stock_report(
    symbol='^HSI',
    price_data=data['data'],
    indicators=data['indicators'],
    ai_analysis=ai_result  # 添加AI分析
)
```

### 示例4: 自定义输出目录

```python
# 指定输出目录
visualizer = ExcelVisualizer(output_dir='my_reports')

# 生成报告
filepath = visualizer.generate_stock_report(
    symbol='^HSI',
    price_data=data,
    indicators=indicators
)
```

### 示例5: Web界面使用

```bash
# 启动Web界面
streamlit run src/ai_inv/web_dashboard.py

# 访问 http://localhost:8501
# 选择页面和功能
# 输入参数并分析
# 导出结果
```

---

## 图表类型

### Excel图表

ExcelVisualizer主要生成数据表格，可以手动创建图表：

- **折线图** - 价格走势、指标变化
- **柱状图** - 成交量、盈亏分布
- **饼图** - 持仓分布
- **散点图** - 收益率vs风险

### Web图表

Web界面使用Plotly创建交互式图表：

#### 价格图表
```python
def plot_price_chart(data, indicators):
    fig = go.Figure()
    
    # K线图
    fig.add_trace(go.Candlestick(
        x=data.index,
        open=data['Open'],
        high=data['High'],
        low=data['Low'],
        close=data['Close']
    ))
    
    # 均线
    fig.add_trace(go.Scatter(
        x=data.index,
        y=indicators['SMA']['SMA_20'],
        mode='lines'
    ))
    
    return fig
```

#### RSI图表
```python
def plot_rsi_chart(indicators):
    fig = go.Figure()
    
    # RSI曲线
    fig.add_trace(go.Scatter(
        x=indicators['RSI'].index,
        y=indicators['RSI']
    ))
    
    # 超买超卖线
    fig.add_hline(y=70, line_dash="dash")
    fig.add_hline(y=30, line_dash="dash")
    
    return fig
```

#### MACD图表
```python
def plot_macd_chart(indicators):
    macd = indicators['MACD']
    
    fig = go.Figure()
    
    # MACD线
    fig.add_trace(go.Scatter(
        x=macd['macd'].index,
        y=macd['macd'],
        name='MACD'
    ))
    
    # 信号线
    fig.add_trace(go.Scatter(
        x=macd['signal'].index,
        y=macd['signal'],
        name='Signal'
    ))
    
    # 柱状图
    fig.add_trace(go.Bar(
        x=macd['histogram'].index,
        y=macd['histogram'],
        name='Histogram'
    ))
    
    return fig
```

---

## 高级功能

### 1. 自定义Excel格式

```python
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter

# 打开已生成的Excel文件
from openpyxl import load_workbook

wb = load_workbook('output/excel/hsi_report.xlsx')
ws = wb.active

# 自定义样式
ws['A1'].font = Font(bold=True, size=14, color="FF0000")
ws['A1'].fill = PatternFill(start_color="4472C4", fill_type="solid")
ws['A1'].alignment = Alignment(horizontal='center')

# 保存
wb.save('output/excel/hsi_report_custom.xlsx')
```

### 2. 添加图表到Excel

```python
from openpyxl.chart import LineChart, Reference

# 创建图表
chart = LineChart()
chart.title = "价格走势"
chart.style = 10

# 设置数据
data = Reference(ws, min_col=2, min_row=2, max_row=100, max_col=6)
categories = Reference(ws, min_col=1, min_row=2, max_row=100)

chart.add_data(data, titles_from_data=True)
chart.set_categories(categories)

# 添加到工作表
ws.add_chart(chart, "H2")

wb.save('output/excel/hsi_report_with_chart.xlsx')
```

### 3. Web界面自定义

```python
# 自定义页面配置
st.set_page_config(
    page_title="我的投资工具",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义样式
st.markdown("""
<style>
.big-font {
    font-size:20px !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="big-font">大字体文本</p>', unsafe_allow_html=True)
```

### 4. 数据缓存

```python
@st.cache_data
def load_data(symbol, period):
    """缓存数据加载"""
    fetcher = DataFetcher()
    return fetcher.get_historical_data(symbol, period)

# 使用缓存数据
data = load_data('^HSI', '1y')
```

---

## 最佳实践

### 1. Excel报告

#### ✅ 推荐
- 批量生成多只股票报告
- 使用有意义的文件名
- 定期清理旧报告
- 添加日期戳

```python
filename = f"{symbol}_report_{datetime.now().strftime('%Y%m%d')}.xlsx"
```

#### ❌ 避免
- 生成过大的Excel文件
- 包含过多数据行
- 忽略错误处理

### 2. Web界面

#### ✅ 推荐
- 使用缓存减少加载时间
- 分页显示大数据
- 提供加载状态提示
- 响应式设计

```python
with st.spinner("正在加载..."):
    data = load_data(symbol)
```

#### ❌ 避免
- 同步长时间运行的任务
- 一次性加载所有数据
- 不处理异常情况

### 3. 数据可视化

#### ✅ 推荐
- 使用适合的图表类型
- 添加图例和标签
- 保持简洁清晰
- 使用颜色区分

#### ❌ 避免
- 过于复杂的图表
- 信息过载
- 缺少上下文

### 4. 性能优化

#### Excel优化
```python
# 限制数据量
data = data.tail(500)  # 只保留最近500条

# 选择必要列
columns = ['Open', 'High', 'Low', 'Close', 'Volume']
data = data[columns]
```

#### Web优化
```python
# 使用缓存
@st.cache_data(ttl=3600)  # 缓存1小时
def expensive_function():
    pass

# 分页显示
page_size = 50
total_pages = len(data) // page_size
page = st.number_input("页码", 1, total_pages)
```

---

## 故障排除

### 1. Excel相关问题

#### 问题: openpyxl未安装
```
ModuleNotFoundError: No module named 'openpyxl'
```

**解决方案:**
```bash
pip install openpyxl
```

#### 问题: 文件被占用
```
PermissionError: [Errno 13] Permission denied
```

**解决方案:**
- 关闭Excel文件
- 使用新的文件名
- 检查文件权限

#### 问题: 内存不足
```
MemoryError: Unable to allocate array
```

**解决方案:**
- 减少数据量
- 分批处理
- 使用更简单的格式

### 2. Web界面相关问题

#### 问题: streamlit未安装
```
ModuleNotFoundError: No module named 'streamlit'
```

**解决方案:**
```bash
pip install streamlit plotly
```

#### 问题: 端口被占用
```
Port 8501 is already in use
```

**解决方案:**
```bash
# 使用其他端口
streamlit run app.py --server.port 8502
```

#### 问题: 数据加载慢
```
加载时间过长
```

**解决方案:**
```python
# 使用缓存
@st.cache_data
def load_data():
    pass

# 减少数据量
data = data.tail(1000)

# 显示进度
with st.spinner("加载中..."):
    data = load_data()
```

### 3. 图表相关问题

#### 问题: 图表不显示
```
图表区域空白
```

**解决方案:**
- 检查数据格式
- 查看控制台错误
- 确认图表库版本

#### 问题: 图表样式错误
```
图表显示异常
```

**解决方案:**
- 检查Plotly版本
- 更新图表库
- 查看图表文档

---

## 总结

### Excel可视化优势
✅ 专业报表
✅ 离线可用
✅ 易于分享
✅ 广泛兼容

### Web界面优势
✅ 交互式
✅ 实时更新
✅ 丰富图表
✅ 跨平台

### 使用建议
1. **Excel**: 用于正式报告、离线分析、数据存档
2. **Web**: 用于实时监控、交互分析、快速探索
3. **结合使用**: Web分析 + Excel导出 = 最佳体验

---

## 参考资料

- [Streamlit文档](https://docs.streamlit.io/)
- [Plotly文档](https://plotly.com/python/)
- [openpyxl文档](https://openpyxl.readthedocs.io/)
- [项目主页](../../README.md)
