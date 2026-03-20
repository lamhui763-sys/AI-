# AI集成模块使用指南

## 🤖 模块概述

AI集成模块是AI投资工具的智能核心，整合了多种AI技术来提供智能投资分析：

### 🎯 核心功能

1. **OpenAI集成** - 使用ChatGPT等GPT模型进行智能分析
2. **本地LLM支持** - 支持本地大语言模型（可选）
3. **混合AI分析** - 结合多个AI工具的共识分析
4. **情感分析** - 分析新闻、社交媒体的市场情感
5. **智能投资顾问** - 综合技术分析、AI分析和情感分析
6. **投资建议生成** - 基于AI的个性化投资建议
7. **交易计划制定** - 自动生成详细的交易计划

## 🏗️ 模块架构

```
AI集成模块
├── ai_analyzer.py           # AI分析器
│   ├── OpenAI集成
│   ├── 本地LLM支持
│   └── 混合AI分析
│
├── sentiment_analyzer.py    # 情感分析器
│   ├── 文本情感分析
│   ├── 新闻情感分析
│   └── 情感趋势分析
│
├── smart_advisor.py         # 智能投资顾问
│   ├── 综合分析
│   ├── 投资计划
│   └── 投资组合建议
│
└── examples/
    └── ai_analysis_example.py  # 使用示例
```

## 🔑 配置说明

### 1. OpenAI API配置

在 `config.yaml` 中添加：

```yaml
ai:
  openai_api_key: "your-api-key-here"
  openai_model: "gpt-4"  # 或 "gpt-3.5-turbo"
  temperature: 0.7
  max_tokens: 1500
```

或通过环境变量：

```bash
export OPENAI_API_KEY="your-api-key-here"
```

### 2. 获取OpenAI API密钥

1. 访问 [OpenAI官网](https://platform.openai.com/)
2. 注册账号并登录
3. 进入 API Keys 页面
4. 创建新的API密钥
5. 复制密钥并保存到配置文件

## 📖 详细使用指南

### 1. AI股票分析

```python
from src.ai_inv.ai_analyzer import AIAnalyzer

# 创建AI分析器
analyzer = AIAnalyzer()

# 准备技术数据
technical_data = {
    '价格': {
        '收盘价': 28000.0,
        '涨跌幅': '+1.5%'
    },
    '趋势指标': {
        '20日均线': '27500.0',
        '50日均线': '27000.0'
    },
    '动量指标': {
        'RSI': '65.5',
        'RSI状态': '正常'
    },
    '交易信号': 'BUY',
    '信号强度': 3
}

# AI分析
result = analyzer.analyze_stock_with_ai('^HSI', technical_data)

print(f"建议: {result.get('操作建议', 'N/A')}")
print(f"理由: {result.get('投资理由', 'N/A')}")
```

### 2. 获取投资建议

```python
# 获取投资建议
advice = analyzer.get_investment_advice(
    symbol='6158.HK',
    technical_data=technical_data
)

print(f"是否建议投资: {advice.get('是否建议投资', 'N/A')}")
print(f"建议仓位: {advice.get('建议仓位比例', 'N/A')}")
print(f"买入时机: {advice.get('买入时机', 'N/A')}")
```

### 3. 情感分析

```python
from src.ai_inv.sentiment_analyzer import SentimentAnalyzer

# 创建情感分析器
analyzer = SentimentAnalyzer()

# 分析文本
text = "恒生指數今日上漲2%，市場情緒樂觀"
result = analyzer.analyze_text(text)

print(f"情感: {result['sentiment']}")  # positive/negative/neutral
print(f"分数: {result['score']:.2f}")  # -1.0 到 1.0
print(f"强度: {result['strength']}")  # strong/moderate/weak
print(f"正面词: {result['positive_words']}")
print(f"负面词: {result['negative_words']}")
```

### 4. 新闻情感分析

```python
from src.ai_inv.sentiment_analyzer import NewsSentimentAnalyzer

# 创建新闻情感分析器
analyzer = NewsSentimentAnalyzer()

# 模拟新闻列表
news_list = [
    {
        'title': '恆生指數突破30000點',
        'summary': '受惠於市場樂觀情緒，恆生指數今日上升300點',
        'time': '2026-03-13 10:30:00',
        'source': '財經日報'
    },
    {
        'title': '科技股表現突出',
        'summary': '多隻大型科技股上漲超過5%',
        'time': '2026-03-13 11:00:00',
        'source': '經濟日報'
    }
]

# 批量分析
result = analyzer.batch_analyze_news(news_list)

print(f"整体情感: {result['overall_sentiment']}")
print(f"平均分数: {result['average_score']:.2f}")
print(f"正面: {result['positive_count']} 条")
print(f"负面: {result['negative_count']} 条")

# 获取文本摘要
summary = analyzer.get_sentiment_summary(news_list)
print(summary)
```

### 5. 智能顾问综合分析

```python
from src.ai_inv.smart_advisor import SmartAdvisor

# 创建智能顾问
advisor = SmartAdvisor()

# 获取综合分析（技术 + AI + 情感）
analysis = advisor.get_comprehensive_analysis(
    symbol='^HSI',
    period='1y',
    include_news=True
)

# 显示建议
rec = analysis['recommendation']
print(f"操作: {rec['action']}")  # strong_buy/buy/hold/sell/strong_sell
print(f"理由: {rec['reason']}")
print(f"风险: {rec['risk_level']}")
print(f"置信度: {rec['confidence']}")
print(f"总分: {rec['total_score']}/10")

print(f"\n评分分解:")
print(f"  技术面: {rec['technical_score']}/10")
print(f"  AI分析: {rec['ai_score']}/10")
print(f"  情感分析: {rec['sentiment_score']}/10")
```

### 6. 生成投资计划

```python
# 生成个性化投资计划
plan = advisor.get_investment_plan(
    symbol='^HSI',
    capital=100000,  # 10万港元
    risk_tolerance='medium',  # low/medium/high
    investment_goal='growth'  # growth/income/balance
)

print(f"本金: HK${plan['capital']:,.0f}")
print(f"风险承受能力: {plan['risk_tolerance']}")

print(f"\n入场策略:")
entry = plan['entry_strategy']
print(f"  策略: {entry['strategy']}")
print(f"  首次入场价: HK${entry['first_entry']:.2f}")
print(f"  批次数: {entry['batch_count']}")

print(f"\n止损止盈:")
print(f"  止损位: HK${plan['stop_loss']:.2f}")
print(f"  止盈位: HK${plan['take_profit']:.2f}")

print(f"\n仓位管理:")
print(f"  建议仓位: HK${plan['position_size']:,.0f}")

print(f"\n时间周期: {plan['time_horizon']}")
```

### 7. 比较多只股票

```python
# 比较多只股票
symbols = ['^HSI', '6158.HK', '7200.HK']

comparison = advisor.compare_multiple_stocks(symbols)

# 显示排名
print("排名:")
for i, stock in enumerate(comparison['rankings'], 1):
    print(f"{i}. {stock['symbol']} - 评分: {stock['score']:.1f}/10")

print(f"\n建议: {comparison['recommendations']['recommendation']}")
```

### 8. 生成详细报告

```python
# 生成专业投资分析报告
report = advisor.generate_detailed_report('^HSI')

# 保存报告
with open('hsi_ai_report.txt', 'w', encoding='utf-8') as f:
    f.write(report)

print(report)
```

## 🎯 智能投资建议系统

### 建议类型

| 建议 | 含义 | 总分范围 | 风险等级 |
|------|------|---------|---------|
| STRONG BUY | 强力买入 | 7.5-10.0 | 低/中低 |
| BUY | 买入 | 6.0-7.5 | 中低/中 |
| HOLD | 观望 | 4.0-6.0 | 中 |
| SELL | 卖出 | 2.5-4.0 | 中高/高 |
| STRONG SELL | 强力卖出 | 0.0-2.5 | 高 |

### 综合评分计算

```
总分 = 技术面评分 × 0.4 + AI分析评分 × 0.4 + 情感分析评分 × 0.2

- 技术面评分: 基于交易信号、RSI、MACD等技术指标
- AI分析评分: 基于GPT模型的分析结果
- 情感分析评分: 基于新闻和市场情感的正面/负面程度
```

## 💡 最佳实践

### 1. API密钥管理

```python
# 方法1: 使用配置文件
config = {
    'openai_api_key': 'sk-xxx...'
}
analyzer = AIAnalyzer(config)

# 方法2: 使用环境变量
import os
os.environ['OPENAI_API_KEY'] = 'sk-xxx...'
analyzer = AIAnalyzer()

# 方法3: 使用配置文件
# 在config.yaml中设置
```

### 2. 错误处理

```python
try:
    result = analyzer.analyze_stock_with_ai(symbol, technical_data)
except Exception as e:
    print(f"AI分析失败: {e}")
    # 使用备用方案或技术分析结果
```

### 3. API调用优化

```python
# 使用缓存避免重复调用
from functools import lru_cache

@lru_cache(maxsize=100)
def cached_analysis(symbol, data_hash):
    return analyzer.analyze_stock_with_ai(symbol, data)
```

### 4. 批量处理

```python
# 批量分析多只股票
symbols = ['6158.HK', '7200.HK', '^HSI']
results = []

for symbol in symbols:
    try:
        result = advisor.get_comprehensive_analysis(symbol)
        results.append(result)
    except Exception as e:
        print(f"分析 {symbol} 失败: {e}")
```

## 🔧 高级功能

### 1. 混合AI分析

```python
from src.ai_inv.ai_analyzer import HybridAIAnalyzer

# 创建混合分析器
hybrid = HybridAIAnalyzer(config)

# 使用多个AI工具进行共识分析
result = hybrid.analyze_with_consensus(symbol, technical_data)

print(f"OpenAI分析: {result['individual_results']['openai']}")
print(f"共识建议: {result['consensus']}")
```

### 2. 自定义情感词典

```python
# 扩展情感词典
analyzer = SentimentAnalyzer()

# 添加自定义正面词
analyzer.positive_words.update({
    '新概念', '颠覆性', '革命性', '突破性'
})

# 添加自定义负面词
analyzer.negative_words.update({
    '衰退', '萧条', '危机', '暴跌'
})
```

### 3. 情感趋势分析

```python
# 分析历史情感变化
sentiment_history = [
    {'score': 0.5, 'time': '2026-03-10'},
    {'score': 0.3, 'time': '2026-03-11'},
    {'score': 0.7, 'time': '2026-03-12'},
    {'score': 0.8, 'time': '2026-03-13'}
]

trend = analyzer.analyze_sentiment_trend(sentiment_history)

print(f"趋势: {trend['trend']}")  # improving/declining/stable
print(f"说明: {trend['message']}")
```

### 4. 投资组合分析

```python
# 分析投资组合
portfolio = {
    'total_value': 500000,
    'holdings': {
        '6158.HK': {'quantity': 10000, 'avg_price': 0.50},
        '7200.HK': {'quantity': 5000, 'avg_price': 2.00},
        '^HSI': {'quantity': 100, 'avg_price': 28000.0}
    }
}

advice = advisor.get_portfolio_advice(portfolio)

print(f"投资组合总值: HK${advice['portfolio_value']:,.0f}")
print(f"买入建议: {len(advice['portfolio_advice']['buy_recommendations'])} 只")
print(f"卖出建议: {len(advice['portfolio_advice']['sell_recommendations'])} 只")
```

## ⚠️ 注意事项

### 1. API限制

- OpenAI API有调用频率限制
- 建议使用缓存减少调用
- 注意API费用控制

### 2. 数据隐私

- 不要将敏感信息发送给AI
- 注意数据传输安全
- 遵守隐私法规

### 3. 结果可靠性

- AI分析仅供参考
- 需要结合其他分析方法
- 验证重要决策

### 4. 本地化支持

- 默认支持繁体中文
- 可以自定义语言设置
- 情感词典针对港股优化

## 🔍 故障排除

### 问题1: API密钥未配置

**错误信息**:
```
未提供OpenAI API密钥
```

**解决方案**:
```python
# 检查配置
import os
print(os.getenv('OPENAI_API_KEY'))

# 或设置环境变量
os.environ['OPENAI_API_KEY'] = 'your-key'
```

### 问题2: API调用失败

**错误信息**:
```
调用OpenAI API失败: ...
```

**解决方案**:
1. 检查网络连接
2. 验证API密钥有效性
3. 检查账户余额
4. 查看API状态页面

### 问题3: 情感分析不准确

**解决方案**:
1. 扩展情感词典
2. 调整阈值参数
3. 使用混合AI分析
4. 结合人工验证

### 问题4: 响应时间过长

**解决方案**:
1. 使用缓存机制
2. 减少token数量
3. 使用更快的模型（如gpt-3.5-turbo）
4. 批量处理优化

## 📊 性能优化建议

### 1. 缓存策略

```python
import json
from datetime import datetime, timedelta

def get_cached_analysis(symbol, cache_hours=24):
    cache_file = f"cache/{symbol}.json"
    
    try:
        with open(cache_file, 'r') as f:
            cached = json.load(f)
        
        # 检查是否过期
        cache_time = datetime.fromisoformat(cached['time'])
        if datetime.now() - cache_time < timedelta(hours=cache_hours):
            return cached['data']
    except:
        pass
    
    # 生成新分析
    analysis = advisor.get_comprehensive_analysis(symbol)
    
    # 保存缓存
    with open(cache_file, 'w') as f:
        json.dump({
            'time': datetime.now().isoformat(),
            'data': analysis
        }, f)
    
    return analysis
```

### 2. 异步处理

```python
import asyncio

async def analyze_multiple(symbols):
    tasks = [advisor.get_comprehensive_analysis(s) for s in symbols]
    results = await asyncio.gather(*tasks)
    return results
```

## 📚 相关文档

- [README.md](README.md) - 项目总览
- [DATA_MODULE_GUIDE.md](DATA_MODULE_GUIDE.md) - 数据模块指南
- [TECHNICAL_ANALYSIS_GUIDE.md](TECHNICAL_ANALYSIS_GUIDE.md) - 技术分析指南
- [BACKTEST_ENGINE_GUIDE.md](BACKTEST_ENGINE_GUIDE.md) - 回测引擎指南（待完成）

## 🆘 获取帮助

如果遇到问题：

1. 查看示例代码 `examples/ai_analysis_example.py`
2. 检查日志输出
3. 查阅本指南的故障排除部分
4. 参考OpenAI API文档

## 💰 成本控制

### API费用估算

OpenAI API按token计费：

- GPT-4: ~$0.03/1K tokens (输入) + $0.06/1K tokens (输出)
- GPT-3.5-turbo: ~$0.0015/1K tokens (输入) + $0.002/1K tokens (输出)

**典型分析成本**:
- 单次股票分析: ~$0.02-0.05
- 每日10次分析: ~$0.20-0.50
- 每月300次分析: ~$6.00-15.00

### 成本优化建议

1. 使用gpt-3.5-turbo降低成本
2. 启用缓存减少调用
3. 控制token数量
4. 批量分析提高效率

## 📈 更新日志

### v1.0.0 (2026-03-13)

- ✅ 实现OpenAI集成
- ✅ 实现情感分析
- ✅ 实现智能投资顾问
- ✅ 实现投资计划生成
- ✅ 实现投资组合分析
- ✅ 实现混合AI分析

---

**AI集成模块** - 让投资分析更智能、更精准！
