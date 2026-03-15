# AI投资工具 (AI Investment Tool)

> 一个专业的港股投资分析工具，集成技术分析、AI智能分析和策略回测功能

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![Streamlit](https://img.shields.io/badge/Streamlit-Web-orange)](https://streamlit.io/)

## 📖 目录

- [项目简介](#项目简介)
- [功能特性](#功能特性)
- [快速开始](#快速开始)
- [安装指南](#安装指南)
- [使用文档](#使用文档)
- [示例代码](#示例代码)
- [Web界面](#web界面)
- [API文档](#api文档)
- [常见问题](#常见问题)
- [贡献指南](#贡献指南)
- [许可证](#许可证)

---

## 项目简介

AI投资工具是一个专为港股投资设计的综合分析工具，结合了传统技术分析、现代AI技术和量化回测功能。

### 主要目标

- 📊 **技术分析** - 提供专业的技术指标和交易信号
- 🤖 **AI驱动** - 集成ChatGPT等AI工具进行智能分析
- ⏱️ **策略回测** - 验证交易策略的有效性
- 📈 **可视化** - Excel报表和Web界面双重视图
- 💼 **港股优化** - 专门针对港股市场优化

### 适用人群

- 港股投资者
- 量化交易爱好者
- 金融分析师
- 投资研究者
- 学习Python金融分析的开发者

---

## 功能特性

### 🎯 核心功能

#### 1. 数据获取
- ✅ 多数据源支持（Yahoo Finance、Alpha Vantage）
- ✅ 实时和历史数据
- ✅ 港股代码支持
- ✅ 自动数据清洗

#### 2. 技术分析
- ✅ 20+ 技术指标（SMA、EMA、RSI、MACD、布林带等）
- ✅ 自动交易信号生成
- ✅ 趋势分析
- ✅ 支撑阻力位分析

#### 3. AI分析
- ✅ ChatGPT API集成
- ✅ 智能投资建议
- ✅ 新闻情感分析
- ✅ 综合评分系统

#### 4. 回测引擎
- ✅ 多种策略（MA、RSI、MACD、组合策略）
- ✅ 完整的性能指标
- ✅ 手续费和滑点模拟
- ✅ 参数优化

#### 5. 可视化
- ✅ Excel报表生成
- ✅ Web交互界面
- ✅ 丰富的图表类型
- ✅ 数据导出

### 📊 技术指标库

| 类别 | 指标 | 数量 |
|-----|------|------|
| 趋势指标 | SMA, EMA, 布林带, 肯特纳通道 | 4 |
| 动量指标 | RSI, MACD, 随机震荡, 威廉指标 | 4 |
| 成交量指标 | OBV, 成交量MA | 2 |
| 波动率指标 | ATR, 肯特纳通道 | 2 |

---

## 快速开始

### 30秒快速体验

```bash
# 1. 克隆项目
git clone <repository-url>
cd ai-invest-tool

# 2. 安装依赖
pip install -r requirements.txt

# 3. 启动Web界面
streamlit run src/ai_inv/web_dashboard.py

# 4. 浏览器访问
# http://localhost:8501
```

### Python代码快速上手

```python
from src.ai_inv.technical_analyzer import TechnicalAnalyzer
from src.ai_inv.excel_visualizer import ExcelVisualizer

# 创建分析器
analyzer = TechnicalAnalyzer()

# 分析股票
data = analyzer.analyze_stock('^HSI', period='1y')

# 获取交易信号
signal = analyzer.get_trading_signal('^HSI')
print(f"交易信号: {signal['交易信号']}")

# 生成Excel报告
visualizer = ExcelVisualizer()
filepath = visualizer.generate_stock_report(
    symbol='^HSI',
    price_data=data['data'],
    indicators=data['indicators']
)
print(f"报告已生成: {filepath}")
```

---

## 安装指南

### 系统要求

- Python 3.9 或更高版本
- Windows / macOS / Linux
- 至少 2GB 可用内存
- 网络连接（用于获取数据）

### 详细安装步骤

#### 1. 安装Python

```bash
# Windows: 访问 https://www.python.org/downloads/
# macOS: brew install python3
# Linux: sudo apt-get install python3
```

#### 2. 克隆项目

```bash
git clone <repository-url>
cd ai-invest-tool
```

#### 3. 创建虚拟环境（推荐）

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

#### 4. 安装依赖

```bash
# 安装所有依赖
pip install -r requirements.txt

# 或者分步安装
pip install pandas numpy yfinance
pip install openai
pip install streamlit plotly
pip install openpyxl
```

#### 5. 配置API密钥（可选）

```bash
# OpenAI API（用于AI分析）
export OPENAI_API_KEY="your-api-key-here"

# Alpha Vantage（备用数据源）
export ALPHA_VANTAGE_API_KEY="your-api-key-here"
```

#### 6. 验证安装

```bash
# 运行测试
python -m pytest tests/

# 启动Web界面
streamlit run src/ai_inv/web_dashboard.py
```

### 依赖说明

| 依赖包 | 用途 | 必须 |
|-------|------|------|
| pandas | 数据处理 | ✅ |
| numpy | 数值计算 | ✅ |
| yfinance | 数据获取 | ✅ |
| openai | AI分析 | ⚠️ |
| streamlit | Web界面 | ⚠️ |
| plotly | 图表库 | ⚠️ |
| openpyxl | Excel处理 | ⚠️ |

---

## 使用文档

### 文档导航

| 文档 | 说明 | 链接 |
|-----|------|------|
| 快速开始 | 5分钟上手指南 | [快速开始指南](QUICKSTART.md) |
| 技术分析 | 技术指标详细说明 | [技术分析指南](TECHNICAL_ANALYSIS_GUIDE.md) |
| AI集成 | AI功能使用说明 | [AI集成指南](AI_INTEGRATION_GUIDE.md) |
| 回测引擎 | 策略回测教程 | [回测引擎指南](BACKTEST_ENGINE_GUIDE.md) |
| 可视化 | Excel和Web界面 | [可视化指南](VISUALIZATION_GUIDE.md) |
| API文档 | 完整API参考 | [API文档](docs/API.md) |

### 常见使用场景

#### 场景1: 股票技术分析

```python
from src.ai_inv.technical_analyzer import TechnicalAnalyzer

analyzer = TechnicalAnalyzer()

# 单股票分析
result = analyzer.analyze_stock('6158.HK', period='3mo')

# 获取交易信号
signal = analyzer.get_trading_signal('6158.HK')
```

#### 场景2: AI智能分析

```python
from src.ai_inv.ai_analyzer import AIAnalyzer
from src.ai_inv.smart_advisor import SmartAdvisor

# AI分析
ai_analyzer = AIAnalyzer()
result = ai_analyzer.analyze_stock_with_ai('^HSI', technical_data)

# 智能顾问
advisor = SmartAdvisor()
analysis = advisor.get_comprehensive_analysis('^HSI')
```

#### 场景3: 策略回测

```python
from src.ai_inv.backtester import BacktestEngine, MAStrategy

# 创建回测引擎
engine = BacktestEngine(initial_capital=100000)

# 创建策略
strategy = MAStrategy(short_period=5, long_period=20)

# 运行回测
results = engine.run_backtest(data, strategy)
```

#### 场景4: 生成报告

```python
from src.ai_inv.excel_visualizer import ExcelVisualizer

visualizer = ExcelVisualizer()

# 股票报告
filepath = visualizer.generate_stock_report(
    symbol='^HSI',
    price_data=data,
    indicators=indicators
)

# 回测报告
filepath = visualizer.generate_backtest_report(
    results=results,
    strategy_name='MA_5_20'
)
```

---

## 示例代码

### 示例目录结构

```
examples/
├── data_fetching_example.py      # 数据获取示例
├── technical_analysis_example.py # 技术分析示例
├── ai_analysis_example.py        # AI分析示例
├── backtest_example.py          # 回测示例
└── visualization_example.py     # 可视化示例
```

### 运行示例

```bash
# 数据获取示例
python examples/data_fetching_example.py

# 技术分析示例
python examples/technical_analysis_example.py

# AI分析示例
python examples/ai_analysis_example.py

# 回测示例
python examples/backtest_example.py

# 可视化示例
python examples/visualization_example.py
```

### 完整工作流示例

```python
from src.ai_inv.data_fetcher import DataFetcher
from src.ai_inv.technical_analyzer import TechnicalAnalyzer
from src.ai_inv.ai_analyzer import AIAnalyzer
from src.ai_inv.backtester import BacktestEngine, MAStrategy
from src.ai_inv.excel_visualizer import ExcelVisualizer

# 1. 获取数据
fetcher = DataFetcher()
data = fetcher.get_historical_data('^HSI', period='1y')

# 2. 技术分析
analyzer = TechnicalAnalyzer()
indicators = analyzer.analyze_stock('^HSI', period='1y')
signal = analyzer.get_trading_signal('^HSI')

# 3. AI分析（需要API Key）
ai_analyzer = AIAnalyzer()
ai_result = ai_analyzer.analyze_stock_with_ai('^HSI', indicators['summary'])

# 4. 回测
engine = BacktestEngine(initial_capital=100000)
strategy = MAStrategy(5, 20)
backtest_results = engine.run_backtest(data, strategy)

# 5. 生成报告
visualizer = ExcelVisualizer()

# 股票分析报告
visualizer.generate_stock_report(
    symbol='^HSI',
    price_data=data,
    indicators=indicators['indicators'],
    ai_analysis=ai_result
)

# 回测报告
visualizer.generate_backtest_report(
    results=backtest_results,
    strategy_name='MA_5_20'
)

print("分析完成！报告已生成。")
```

---

## Web界面

### 启动Web界面

```bash
# 基本启动
streamlit run src/ai_inv/web_dashboard.py

# 指定端口
streamlit run src/ai_inv/web_dashboard.py --server.port 8501

# 自动刷新
streamlit run src/ai_inv/web_dashboard.py --server.runOnSave true
```

### 访问界面

启动后，在浏览器中访问：
- 本地：http://localhost:8501
- 局域网：http://<your-ip>:8501

### Web界面功能

| 功能 | 描述 |
|-----|------|
| 股票分析 | 实时股票数据和分析 |
| 技术分析 | 交互式技术指标图表 |
| AI分析 | ChatGPT驱动的智能分析 |
| 回测引擎 | 策略回测和结果展示 |
| 投资组合 | 持仓管理和分析 |
| 新闻分析 | 新闻情感分析 |

---

## API文档

### 核心模块

#### 1. DataFetcher

```python
from src.ai_inv.data_fetcher import DataFetcher

fetcher = DataFetcher()

# 获取历史数据
data = fetcher.get_historical_data(symbol='^HSI', period='1y')

# 获取实时数据
data = fetcher.get_realtime_data(symbol='^HSI')

# 批量获取
data_list = fetcher.get_batch_data(symbols=['^HSI', '6158.HK'])
```

#### 2. TechnicalAnalyzer

```python
from src.ai_inv.technical_analyzer import TechnicalAnalyzer

analyzer = TechnicalAnalyzer()

# 分析股票
result = analyzer.analyze_stock(symbol='^HSI', period='1y')

# 获取交易信号
signal = analyzer.get_trading_signal(symbol='^HSI')

# 多股票分析
results = analyzer.analyze_multiple_stocks(symbols=['^HSI', '6158.HK'])
```

#### 3. AIAnalyzer

```python
from src.ai_inv.ai_analyzer import AIAnalyzer

analyzer = AIAnalyzer()

# AI股票分析
result = analyzer.analyze_stock_with_ai(
    symbol='^HSI',
    technical_data=data
)

# 解释指标
explanation = analyzer.explain_indicator('RSI')
```

#### 4. BacktestEngine

```python
from src.ai_inv.backtester import BacktestEngine, MAStrategy

engine = BacktestEngine(
    initial_capital=100000,
    commission=0.001
)

strategy = MAStrategy(short_period=5, long_period=20)

# 运行回测
results = engine.run_backtest(data, strategy)

# 生成报告
engine.generate_report(results)
```

#### 5. ExcelVisualizer

```python
from src.ai_inv.excel_visualizer import ExcelVisualizer

visualizer = ExcelVisualizer(output_dir='output/excel')

# 生成股票报告
filepath = visualizer.generate_stock_report(
    symbol='^HSI',
    price_data=data,
    indicators=indicators
)

# 生成回测报告
filepath = visualizer.generate_backtest_report(
    results=results,
    strategy_name='MA_5_20'
)
```

### 完整API文档

详细的API文档请参考：[API文档](docs/API.md)

---

## 常见问题

### 安装问题

**Q: pip安装失败怎么办？**

A: 尝试以下方法：
```bash
# 使用国内镜像
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 升级pip
python -m pip install --upgrade pip

# 使用conda（如果使用Anaconda）
conda install pandas numpy
```

**Q: TA-Lib安装失败？**

A: TA-Lib需要先安装C库：
```bash
# macOS
brew install ta-lib

# Linux
sudo apt-get install libta-lib-dev

# Windows: 下载预编译的whl文件
```

### 使用问题

**Q: 无法获取股票数据？**

A: 检查以下几点：
1. 股票代码格式是否正确（港股使用.HK后缀）
2. 网络连接是否正常
3. Yahoo Finance服务是否可用

**Q: AI分析功能不可用？**

A: 需要配置OpenAI API Key：
```bash
export OPENAI_API_KEY="your-api-key-here"
```

**Q: 回测结果不理想？**

A: 回测建议：
1. 使用足够长的历史数据
2. 考虑交易成本（手续费、滑点）
3. 避免过度优化参数
4. 使用样本外验证

### 性能问题

**Q: 数据处理速度慢？**

A: 优化建议：
1. 使用数据缓存
2. 限制数据量
3. 使用更高效的数据结构
4. 并行处理

**Q: 内存占用过高？**

A: 解决方法：
1. 分批处理数据
2. 使用更少的数据周期
3. 及时清理无用数据
4. 使用数据压缩

---

## 贡献指南

欢迎贡献代码！请遵循以下步骤：

1. Fork 项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

### 代码规范

- 遵循 PEP 8 代码风格
- 添加必要的注释和文档字符串
- 编写单元测试
- 更新相关文档

### 提交规范

```
feat: 新功能
fix: 修复bug
docs: 文档更新
style: 代码格式调整
refactor: 重构
test: 测试相关
chore: 构建/工具相关
```

---

## 项目结构

```
ai-invest-tool/
├── src/
│   └── ai_inv/
│       ├── __init__.py
│       ├── data_fetcher.py          # 数据获取模块
│       ├── indicators.py            # 技术指标计算
│       ├── technical_analyzer.py    # 技术分析器
│       ├── ai_analyzer.py           # AI分析模块
│       ├── sentiment_analyzer.py    # 情感分析
│       ├── smart_advisor.py         # 智能顾问
│       ├── backtester.py            # 回测引擎
│       ├── portfolio_optimizer.py   # 投资组合优化
│       ├── excel_visualizer.py      # Excel可视化
│       └── web_dashboard.py         # Web仪表板
├── examples/                        # 示例代码
│   ├── data_fetching_example.py
│   ├── technical_analysis_example.py
│   ├── ai_analysis_example.py
│   ├── backtest_example.py
│   └── visualization_example.py
├── tests/                           # 单元测试
│   ├── test_data_fetcher.py
│   ├── test_technical_analysis.py
│   ├── test_ai_analysis.py
│   ├── test_backtest.py
│   └── test_visualization.py
├── docs/                            # 文档
│   └── API.md
├── output/                          # 输出目录
│   ├── excel/                       # Excel报告
│   └── reports/                     # 其他报告
├── config.yaml                      # 配置文件
├── requirements.txt                 # 依赖包
├── README.md                        # 项目说明
├── QUICKSTART.md                    # 快速开始
├── TECHNICAL_ANALYSIS_GUIDE.md     # 技术分析指南
├── AI_INTEGRATION_GUIDE.md         # AI集成指南
├── BACKTEST_ENGINE_GUIDE.md        # 回测引擎指南
└── VISUALIZATION_GUIDE.md          # 可视化指南
```

---

## 版本历史

### v1.0.0 (2024-01-15)
- ✅ 初始版本发布
- ✅ 完整的数据获取功能
- ✅ 20+ 技术指标
- ✅ AI分析集成
- ✅ 回测引擎
- ✅ Excel和Web可视化

---

## 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

---

## 联系方式

- 项目主页: [GitHub Repository]
- 问题反馈: [Issues]
- 邮箱: your-email@example.com

---

## 致谢

感谢以下开源项目：

- [yfinance](https://github.com/ranaroussi/yfinance) - 金融数据获取
- [pandas](https://pandas.pydata.org/) - 数据处理
- [streamlit](https://streamlit.io/) - Web框架
- [plotly](https://plotly.com/) - 数据可视化
- [openpyxl](https://openpyxl.readthedocs.io/) - Excel处理

---

## 免责声明

本工具仅供学习和研究使用，不构成投资建议。投资有风险，入市需谨慎。使用本工具进行投资所产生的任何损失，开发者不承担责任。

---

## Star History

如果这个项目对你有帮助，请给一个 ⭐ Star！

<div align="center">
  <a href="https://github.com/yourusername/ai-invest-tool">
    <img src="https://api.star-history.com/svg?repos=yourusername/ai-invest-tool&type=Date" alt="Star History Chart">
  </a>
</div>
