# 🚀 如何使用AI投资工具

## 📱 方法1: 一键启动（推荐）

### Windows用户

**双击运行** `start.bat` 文件即可！

1. 找到 `start.bat` 文件
2. 双击运行
3. 等待自动安装依赖
4. 浏览器会自动打开

### macOS/Linux用户

**在终端运行**:
```bash
chmod +x start.sh
./start.sh
```

### 任意系统（推荐）

**运行Python脚本**:
```bash
python run.py
```

这个脚本会：
- ✅ 自动检查Python版本
- ✅ 自动安装所有依赖
- ✅ 自动启动Web界面
- ✅ 自动打开浏览器

---

## 🌐 方法2: 命令行启动

### 步骤1: 安装依赖

```bash
pip install streamlit plotly openpyxl pandas numpy yfinance openai
```

### 步骤2: 启动Web界面

```bash
streamlit run src/ai_inv/web_dashboard.py
```

### 步骤3: 访问

浏览器会自动打开，或者手动访问:
```
http://localhost:8501
```

---

## 💻 方法3: Python代码

### 创建测试文件 `test.py`

```python
from src.ai_inv.technical_analyzer import TechnicalAnalyzer

# 创建分析器
analyzer = TechnicalAnalyzer()

# 分析恒生指数
result = analyzer.analyze_stock('^HSI', period='1y')

# 获取交易信号
signal = analyzer.get_trading_signal('^HSI')

# 显示结果
print("=" * 60)
print("AI投资工具 - 股票分析")
print("=" * 60)
print()
print(f"股票代码: ^HSI (恒生指数)")
print(f"最新价格: HK${result['data']['Close'].iloc[-1]:.2f}")
print(f"交易信号: {signal['交易信号']}")
print(f"信号强度: {signal['强度']}")
print()
print("=" * 60)
```

运行:
```bash
python test.py
```

---

## 🎯 Web界面功能

启动后，您会看到一个漂亮的Web界面，包含以下功能：

### 1. 📊 股票分析
- 输入股票代码（如 `^HSI`, `6158.HK`）
- 选择时间周期（1个月到5年）
- 点击"开始分析"
- 查看价格图表、技术指标、交易信号

### 2. 🔬 技术分析
- 选择要显示的技术指标
- 自定义指标参数
- 查看实时交互式图表
- 导出Excel报告

### 3. 🤖 AI分析
- 配置OpenAI API Key（可选）
- 进行AI驱动的股票分析
- 查看情感分析
- 获取智能投资建议

### 4. ⏱️ 回测引擎
- 选择交易策略
- 配置回测参数
- 运行策略回测
- 查看资金曲线和性能指标

### 5. 💼 投资组合
- 添加您的持仓
- 实时更新价格
- 查看组合统计
- 分析盈亏情况

### 6. 📰 新闻分析
- 输入新闻文本
- 分析情感倾向
- 查看关键词
- 获取情感评分

---

## 💡 快速示例

### 示例1: 分析恒生指数

1. 启动Web界面
2. 在"股票分析"页面
3. 输入: `^HSI`
4. 选择: 1年
5. 点击: 开始分析
6. 查看结果和图表

### 示例2: 查看技术指标

1. 切换到"技术分析"页面
2. 输入股票代码: `6158.HK`
3. 勾选: RSI、MACD、布林带
4. 点击: 生成分析
5. 查看交互式图表

### 示例3: 回测策略

1. 切换到"回测引擎"页面
2. 选择策略: 移动平均交叉
3. 设置参数: 短期5，长期20
4. 点击: 开始回测
5. 查看回测结果和性能指标

---

## 📤 导出报告

### Excel报告

在任何分析页面，点击"导出为Excel"按钮，即可生成专业的Excel报告。

报告包含:
- 价格数据
- 技术指标
- 交易信号
- AI分析（如果有）
- 摘要信息

---

## ⚙️ 配置

### OpenAI API（可选）

如果想要使用AI分析功能：

1. 访问 https://platform.openai.com/api-keys
2. 注册并获取API Key
3. 在Web界面的"AI分析"页面输入Key

或者设置环境变量:
```bash
# Windows
set OPENAI_API_KEY=your-key-here

# macOS/Linux
export OPENAI_API_KEY="your-key-here"
```

---

## 📚 更多示例

运行完整示例:
```bash
python examples/complete_workflow.py
```

这个示例会:
1. 获取多只股票数据
2. 进行技术分析
3. AI智能分析
4. 策略回测
5. 投资组合优化
6. 生成Excel报告

---

## ❓ 常见问题

### Q: 启动失败怎么办？

A: 尝试以下方法:
1. 确认Python已安装（需要3.9+）
2. 手动安装依赖: `pip install streamlit plotly openpyxl`
3. 检查防火墙设置

### Q: 无法获取股票数据？

A: 检查:
1. 网络连接是否正常
2. 股票代码格式是否正确（港股用.HK后缀）
3. Yahoo Finance服务是否可用

### Q: AI分析功能不可用？

A: 需要配置OpenAI API Key，详见上面的"配置"部分

---

## 🎉 开始使用

### 推荐的启动方式:

**Windows**:
```bash
# 双击运行
start.bat
```

**Python脚本**:
```bash
python run.py
```

**命令行**:
```bash
streamlit run src/ai_inv/web_dashboard.py
```

启动后，浏览器会自动打开 http://localhost:8501

---

## 📞 获取帮助

- 📖 查看完整文档: [README.md](README.md)
- 🚀 快速开始: [QUICKSTART.md](QUICKSTART.md)
- 💻 查看示例: `examples/` 目录

---

祝您使用愉快！🎊
