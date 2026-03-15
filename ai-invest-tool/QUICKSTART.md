# 快速开始指南

欢迎来到AI投资工具！本指南将帮助您在5分钟内快速上手。

## 📋 前提条件

- Python 3.9+
- 网络连接
- 基本的Python知识

## 🚀 5分钟快速开始

### 第一步：安装（2分钟）

```bash
# 1. 克隆项目
git clone <repository-url>
cd ai-invest-tool

# 2. 创建虚拟环境（推荐）
python -m venv venv

# Windows激活
venv\Scripts\activate

# macOS/Linux激活
source venv/bin/activate

# 3. 安装依赖
pip install -r requirements.txt
```

### 第二步：配置（1分钟）

```bash
# 可选：配置OpenAI API Key（用于AI分析）
export OPENAI_API_KEY="your-api-key-here"
```

### 第三步：运行（2分钟）

#### 方式1：Web界面（推荐）

```bash
# 启动Web界面
streamlit run src/ai_inv/web_dashboard.py

# 浏览器访问
http://localhost:8501
```

#### 方式2：Python代码

```python
# 创建文件 test.py
from src.ai_inv.technical_analyzer import TechnicalAnalyzer

# 创建分析器
analyzer = TechnicalAnalyzer()

# 分析恒生指数
result = analyzer.analyze_stock('^HSI', period='1y')

# 获取交易信号
signal = analyzer.get_trading_signal('^HSI')

# 显示结果
print(f"股票: ^HSI")
print(f"交易信号: {signal['交易信号']}")
print(f"信号强度: {signal['强度']}")
```

运行：
```bash
python test.py
```

## 💡 基础示例

### 示例1：分析单只股票

```python
from src.ai_inv.technical_analyzer import TechnicalAnalyzer

analyzer = TechnicalAnalyzer()

# 分析股票
data = analyzer.analyze_stock('6158.HK', period='3mo')

# 查看结果
print(f"收盘价: {data['data']['Close'].iloc[-1]}")
print(f"RSI: {data['indicators']['RSI'].iloc[-1]:.2f}")

# 获取交易信号
signal = analyzer.get_trading_signal('6158.HK')
print(f"建议: {signal['交易信号']}")
```

### 示例2：批量分析多只股票

```python
from src.ai_inv.technical_analyzer import TechnicalAnalyzer

analyzer = TechnicalAnalyzer()

# 股票列表
symbols = ['^HSI', '6158.HK', '7200.HK']

# 批量分析
results = analyzer.analyze_multiple_stocks(symbols)

# 显示结果
for result in results:
    print(f"{result['股票代码']}: {result['交易信号']} (强度: {result['强度']})")
```

### 示例3：生成Excel报告

```python
from src.ai_inv.technical_analyzer import TechnicalAnalyzer
from src.ai_inv.excel_visualizer import ExcelVisualizer

# 分析股票
analyzer = TechnicalAnalyzer()
data = analyzer.analyze_stock('^HSI', period='1y')

# 生成Excel报告
visualizer = ExcelVisualizer()
filepath = visualizer.generate_stock_report(
    symbol='^HSI',
    price_data=data['data'],
    indicators=data['indicators']
)

print(f"报告已生成: {filepath}")
```

### 示例4：策略回测

```python
from src.ai_inv.backtester import BacktestEngine, MAStrategy
from src.ai_inv.data_fetcher import DataFetcher

# 获取数据
fetcher = DataFetcher()
data = fetcher.get_historical_data('^HSI', period='2y')

# 创建回测引擎
engine = BacktestEngine(initial_capital=100000)

# 创建策略
strategy = MAStrategy(short_period=5, long_period=20)

# 运行回测
results = engine.run_backtest(data, strategy)

# 查看结果
summary = results['summary']
print(f"总收益率: {summary['total_return']:.2f}%")
print(f"夏普比率: {summary['sharpe_ratio']:.2f}")
print(f"胜率: {summary['win_rate']:.2f}%")
```

## 📊 Web界面使用指南

### 启动Web界面

```bash
streamlit run src/ai_inv/web_dashboard.py
```

### 主要功能页面

1. **股票分析** - 输入股票代码，查看实时分析
2. **技术分析** - 选择技术指标，查看图表
3. **AI分析** - 配置API Key，进行智能分析
4. **回测引擎** - 选择策略，运行回测
5. **投资组合** - 管理持仓，查看分析
6. **新闻分析** - 分析新闻情感

### 基本操作

1. 在左侧边栏选择功能页面
2. 输入参数（股票代码、时间周期等）
3. 点击"开始分析"按钮
4. 查看结果和图表
5. 导出Excel报告（可选）

## 🎯 常见使用场景

### 场景1：每日股票分析

```python
# 每天早上分析关注列表
from src.ai_inv.technical_analyzer import TechnicalAnalyzer

analyzer = TechnicalAnalyzer()
watchlist = ['^HSI', '6158.HK', '7200.HK']

for symbol in watchlist:
    signal = analyzer.get_trading_signal(symbol)
    if signal['强度'] >= 2:
        print(f"⚠️  {symbol}: {signal['交易信号']} (强度: {signal['强度']})")
```

### 场景2：寻找买入机会

```python
from src.ai_inv.technical_analyzer import TechnicalAnalyzer

analyzer = TechnicalAnalyzer()

# 寻找买入机会
opportunities = analyzer.find_opportunities(
    symbols=['^HSI', '6158.HK', '7200.HK'],
    signal_type='BUY',
    min_strength=2
)

print("买入机会:")
for opp in opportunities:
    print(f"  {opp['股票代码']}: {opp['信号']} (强度: {opp['强度']})")
```

### 场景3：生成周报

```python
from src.ai_inv.technical_analyzer import TechnicalAnalyzer
from src.ai_inv.excel_visualizer import ExcelVisualizer
from datetime import datetime

analyzer = TechnicalAnalyzer()
visualizer = ExcelVisualizer()

# 为每只股票生成报告
symbols = ['^HSI', '6158.HK', '7200.HK']
date_str = datetime.now().strftime('%Y%m%d')

for symbol in symbols:
    data = analyzer.analyze_stock(symbol, period='1w')
    
    filename = f"{symbol}_weekly_{date_str}.xlsx"
    visualizer.generate_stock_report(
        symbol=symbol,
        price_data=data['data'],
        indicators=data['indicators'],
        filename=filename
    )

print(f"周报已生成，共{len(symbols)}份")
```

## 🔧 配置说明

### 基本配置

编辑 `config.yaml` 文件：

```yaml
# 数据源配置
data:
  source: "yfinance"  # yfinance 或 alpha_vantage
  cache_enabled: true
  cache_dir: "cache"

# 技术分析配置
technical:
  default_period: "1y"
  indicators:
    rsi_period: 14
    macd_fast: 12
    macd_slow: 26
    macd_signal: 9

# AI分析配置
ai:
  model: "gpt-4"
  temperature: 0.7
  max_tokens: 500

# 回测配置
backtest:
  initial_capital: 100000
  commission: 0.001
  slippage: 0.0005

# 输出配置
output:
  excel_dir: "output/excel"
  report_dir: "output/reports"
```

### API Key配置

创建 `.env` 文件：

```bash
# OpenAI API
OPENAI_API_KEY=sk-your-openai-key-here

# Alpha Vantage API
ALPHA_VANTAGE_API_KEY=your-alpha-vantage-key-here
```

## 📖 下一步

现在您已经了解了基本使用方法，接下来可以：

1. **深入学习** - 阅读详细的使用指南
   - [技术分析指南](TECHNICAL_ANALYSIS_GUIDE.md)
   - [AI集成指南](AI_INTEGRATION_GUIDE.md)
   - [回测引擎指南](BACKTEST_ENGINE_GUIDE.md)
   - [可视化指南](VISUALIZATION_GUIDE.md)

2. **运行示例** - 查看更多示例代码
   ```bash
   python examples/technical_analysis_example.py
   python examples/ai_analysis_example.py
   python examples/backtest_example.py
   ```

3. **阅读API文档** - 了解所有可用的功能
   - [API文档](docs/API.md)

4. **自定义开发** - 根据您的需求定制
   - 创建自定义策略
   - 添加新的技术指标
   - 集成其他AI工具

## ❓ 获取帮助

### 常见问题

**Q: 如何获取OpenAI API Key？**

A: 访问 [OpenAI官网](https://platform.openai.com/api-keys) 注册并获取API Key。

**Q: 支持哪些股票市场？**

A: 主要支持港股（使用.HK后缀），也支持美股、A股等。

**Q: 可以离线使用吗？**

A: Excel可视化功能可以离线使用，但数据获取需要网络连接。

**Q: 如何优化回测性能？**

A: 使用更少的数据周期、限制交易次数、使用缓存。

### 获取支持

- 📧 邮箱: your-email@example.com
- 💬 GitHub Issues: [提交问题](https://github.com/yourusername/ai-invest-tool/issues)
- 📚 文档: [完整文档](README.md)

## ✅ 检查清单

开始使用前，请确保：

- [ ] 已安装Python 3.9+
- [ ] 已安装所有依赖包
- [ ] 已配置API Key（如需AI功能）
- [ ] 已测试基本功能
- [ ] 已阅读使用文档

---

祝您使用愉快！🎉

如有任何问题，请随时联系。
