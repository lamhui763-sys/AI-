# 贡献指南

感谢您对AI投资工具的兴趣！我们欢迎所有形式的贡献。

## 📋 目录

1. [如何贡献](#如何贡献)
2. [开发环境设置](#开发环境设置)
3. [代码规范](#代码规范)
4. [提交规范](#提交规范)
5. [测试](#测试)
6. [文档](#文档)
7. [问题报告](#问题报告)
8. [功能请求](#功能请求)

---

## 如何贡献

### 贡献方式

- 🐛 报告Bug
- 💡 提出新功能
- 📝 改进文档
- 🔧 修复代码
- 🎨 改进UI/UX
- 🌍 翻译文档

### 贡献流程

1. **Fork项目**
   ```bash
   # 点击GitHub上的Fork按钮
   ```

2. **克隆您的Fork**
   ```bash
   git clone https://github.com/your-username/ai-invest-tool.git
   cd ai-invest-tool
   ```

3. **创建分支**
   ```bash
   git checkout -b feature/your-feature-name
   ```

4. **进行更改**
   ```bash
   # 编写代码
   # 运行测试
   # 更新文档
   ```

5. **提交更改**
   ```bash
   git add .
   git commit -m "feat: add your feature description"
   ```

6. **推送到GitHub**
   ```bash
   git push origin feature/your-feature-name
   ```

7. **创建Pull Request**
   - 访问GitHub
   - 点击"New Pull Request"
   - 填写PR模板
   - 等待审核

---

## 开发环境设置

### 1. Fork和克隆

```bash
# Fork项目后克隆
git clone https://github.com/your-username/ai-invest-tool.git
cd ai-invest-tool

# 添加上游仓库
git remote add upstream https://github.com/original-username/ai-invest-tool.git
```

### 2. 创建虚拟环境

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 3. 安装开发依赖

```bash
# 安装基础依赖
pip install -r requirements.txt

# 安装开发依赖
pip install -r requirements-dev.txt
```

### 4. 配置pre-commit钩子

```bash
# 安装pre-commit
pip install pre-commit

# 安装钩子
pre-commit install
```

### 5. 运行测试

```bash
# 运行所有测试
pytest

# 运行特定测试
pytest tests/test_data_fetcher.py

# 查看覆盖率
pytest --cov=src/ai_inv --cov-report=html
```

---

## 代码规范

### Python代码规范

我们遵循 [PEP 8](https://www.python.org/dev/peps/pep-0008/) 代码风格。

#### 使用Black格式化

```bash
# 安装Black
pip install black

# 格式化代码
black src/ tests/ examples/

# 检查格式
black --check src/ tests/ examples/
```

#### 使用isort排序导入

```bash
# 安装isort
pip install isort

# 排序导入
isort src/ tests/ examples/

# 检查排序
isort --check-only src/ tests/ examples/
```

#### 使用flake8检查

```bash
# 安装flake8
pip install flake8

# 检查代码
flake8 src/ tests/ examples/
```

### 代码示例

#### 好的实践

```python
"""数据获取模块

提供从各种数据源获取股票数据的功能。
"""

from typing import Dict, List, Optional
import pandas as pd
import yfinance as yf


class DataFetcher:
    """数据获取器
    
    用于从Yahoo Finance获取股票数据。
    """
    
    def __init__(self, cache_enabled: bool = True):
        """初始化数据获取器
        
        Args:
            cache_enabled: 是否启用缓存
        """
        self.cache_enabled = cache_enabled
        self._cache = {}
    
    def get_historical_data(
        self,
        symbol: str,
        period: str = '1y'
    ) -> Optional[pd.DataFrame]:
        """获取历史数据
        
        Args:
            symbol: 股票代码
            period: 时间周期
            
        Returns:
            包含历史数据的DataFrame，失败时返回None
        """
        try:
            # 检查缓存
            cache_key = f"{symbol}_{period}"
            if self.cache_enabled and cache_key in self._cache:
                return self._cache[cache_key]
            
            # 获取数据
            data = yf.download(symbol, period=period)
            
            # 缓存数据
            if self.cache_enabled:
                self._cache[cache_key] = data
            
            return data
        
        except Exception as e:
            print(f"获取数据失败: {e}")
            return None
```

#### 不好的实践

```python
# 没有文档字符串
class DataFetcher:
    def __init__(self):
        self.cache = {}
    
    def get_data(self, symbol):
        # 没有类型注解
        data = yf.download(symbol)
        return data
```

### 命名规范

| 类型 | 规范 | 示例 |
|-----|------|------|
| 变量 | 小写下划线 | `stock_price`, `total_return` |
| 常量 | 大写下划线 | `MAX_TRADES`, `API_KEY` |
| 函数 | 小写下划线 | `calculate_rsi`, `get_data` |
| 类 | 大驼峰 | `DataFetcher`, `BacktestEngine` |
| 模块 | 小写下划线 | `data_fetcher.py`, `indicators.py` |

---

## 提交规范

我们使用 [Conventional Commits](https://www.conventionalcommits.org/) 规范。

### 提交格式

```
<type>(<scope>): <subject>

<body>

<footer>
```

### 类型（Type）

| 类型 | 说明 |
|-----|------|
| `feat` | 新功能 |
| `fix` | Bug修复 |
| `docs` | 文档更新 |
| `style` | 代码格式调整（不影响功能） |
| `refactor` | 重构 |
| `test` | 测试相关 |
| `chore` | 构建/工具相关 |
| `perf` | 性能优化 |
| `ci` | CI/CD相关 |

### 示例

```
feat(technical): add Bollinger Bands indicator

添加布林带指标计算功能，包括上轨、中轨和下轨。

- 实现calculate_bollinger_bands函数
- 添加单元测试
- 更新文档

Closes #123
```

```
fix(data): handle missing data gracefully

修复数据缺失时程序崩溃的问题。

当API返回None或空DataFrame时，现在会返回None而不是抛出异常。

Fixes #456
```

```
docs(readme): update installation instructions

更新README中的安装说明，添加Docker部署方法。
```

---

## 测试

### 编写测试

我们使用 [pytest](https://docs.pytest.org/) 进行测试。

#### 测试示例

```python
import unittest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

from src.ai_inv.data_fetcher import DataFetcher


class TestDataFetcher(unittest.TestCase):
    """数据获取器测试"""
    
    def setUp(self):
        """测试前准备"""
        self.fetcher = DataFetcher(cache_enabled=False)
    
    def tearDown(self):
        """测试后清理"""
        self.fetcher = None
    
    def test_get_historical_data(self):
        """测试获取历史数据"""
        # 测试有效股票代码
        data = self.fetcher.get_historical_data('^HSI', period='1mo')
        
        self.assertIsNotNone(data)
        self.assertIsInstance(data, pd.DataFrame)
        self.assertGreater(len(data), 0)
        
        # 检查必要的列
        required_columns = ['Open', 'High', 'Low', 'Close', 'Volume']
        for col in required_columns:
            self.assertIn(col, data.columns)
    
    def test_get_historical_data_invalid_symbol(self):
        """测试无效股票代码"""
        data = self.fetcher.get_historical_data('INVALID', period='1mo')
        
        # 应该返回None
        self.assertIsNone(data)
    
    def test_cache_functionality(self):
        """测试缓存功能"""
        fetcher = DataFetcher(cache_enabled=True)
        
        # 第一次获取
        data1 = fetcher.get_historical_data('^HSI', period='1mo')
        
        # 第二次获取（应该从缓存）
        data2 = fetcher.get_historical_data('^HSI', period='1mo')
        
        # 数据应该相同
        pd.testing.assert_frame_equal(data1, data2)


if __name__ == '__main__':
    unittest.main()
```

### 运行测试

```bash
# 运行所有测试
pytest

# 运行特定测试文件
pytest tests/test_data_fetcher.py

# 运行特定测试函数
pytest tests/test_data_fetcher.py::TestDataFetcher::test_get_historical_data

# 显示详细输出
pytest -v

# 显示覆盖率
pytest --cov=src/ai_inv --cov-report=html

# 只运行失败的测试
pytest --lf
```

### 测试覆盖率

我们要求测试覆盖率至少达到80%。

```bash
# 生成覆盖率报告
pytest --cov=src/ai_inv --cov-report=html

# 在浏览器中查看
open htmlcov/index.html
```

---

## 文档

### 文档要求

1. **代码文档** - 所有公共函数和类必须有文档字符串
2. **API文档** - 新功能需要更新API文档
3. **使用指南** - 新功能需要添加使用示例
4. **变更日志** - 重大变更需要更新CHANGELOG.md

### 文档字符串规范

我们使用 [Google风格](https://google.github.io/styleguide/pyguide.html) 的文档字符串。

```python
def calculate_sma(
    data: pd.DataFrame,
    period: int = 20
) -> pd.Series:
    """计算简单移动平均线
    
    计算给定数据在指定周期内的简单移动平均值。
    
    Args:
        data: 包含价格数据的DataFrame，必须有'Close'列
        period: 移动平均周期，默认为20
        
    Returns:
        包含SMA值的Series
        
    Raises:
        ValueError: 当数据为空或period小于1时
        
    Example:
        >>> data = pd.DataFrame({'Close': [100, 101, 102, 103, 104]})
        >>> sma = calculate_sma(data, period=3)
        >>> print(sma)
        2    101.0
        3    102.0
        4    103.0
        dtype: float64
    """
    if data.empty:
        raise ValueError("数据不能为空")
    
    if period < 1:
        raise ValueError("周期必须大于0")
    
    return data['Close'].rolling(window=period).mean()
```

---

## 问题报告

### 报告Bug前

在报告Bug前，请先：

1. 🔍 搜索已有的Issues
2. 📖 查看文档
3. 🧪 尝试复现问题
4. 📝 收集相关信息

### Bug报告模板

```markdown
**描述**
简要描述遇到的问题。

**复现步骤**
1. 运行 '...'
2. 点击 '....'
3. 滚动到 '....'
4. 看到错误

**预期行为**
描述您期望发生什么。

**实际行为**
描述实际发生了什么。

**截图**
如果适用，添加截图以帮助解释问题。

**环境**
- 操作系统: [e.g. Windows 10, macOS 13.0]
- Python版本: [e.g. 3.9.7]
- 项目版本: [e.g. v1.0.0]

**附加信息**
添加其他有助于解决问题的信息，如错误日志、配置文件等。
```

---

## 功能请求

### 提出新功能前

在提出新功能前，请考虑：

1. 🎯 这个功能是否对大多数用户有用？
2. 📊 是否有足够的使用案例？
3. ⚡ 实现这个功能的复杂度如何？
4. 🔧 是否与现有功能兼容？
5. 📝 您愿意帮忙实现吗？

### 功能请求模板

```markdown
**问题描述**
清晰简洁地描述您想要的功能。

**使用案例**
描述这个功能如何帮助用户。
提供具体的使用场景。

**建议的解决方案**
描述您希望这个功能如何工作。
可以包括伪代码或流程图。

**替代方案**
描述您考虑过的其他解决方案。

**附加信息**
添加其他相关信息，如参考资料、类似实现等。
```

---

## Pull Request指南

### PR标题

遵循提交规范：
```
feat(technical): add new indicator
fix(data): handle missing data
docs(readme): update installation
```

### PR描述模板

```markdown
## 变更说明
简要描述这个PR的变更。

## 相关Issue
Closes #(issue number)

## 变更类型
- [ ] Bug修复
- [ ] 新功能
- [ ] 重大变更
- [ ] 文档更新
- [ ] 性能优化
- [ ] 代码重构

## 测试
- [ ] 已添加测试
- [ ] 所有测试通过
- [ ] 已更新文档

## 检查清单
- [ ] 代码遵循项目规范
- [ ] 已添加必要的文档
- [ ] 已更新CHANGELOG.md（如果适用）
- [ ] 没有引入新的警告
- [ ] 代码已格式化
```

### PR审核流程

1. **自动化检查**
   - 代码风格检查
   - 单元测试
   - 集成测试
   - 代码覆盖率

2. **人工审核**
   - 代码质量
   - 功能实现
   - 文档完整性
   - 向后兼容性

3. **反馈和修改**
   - 审核者提出意见
   - 贡献者修改
   - 重新审核

4. **合并**
   - 审核通过后合并
   - 更新版本号
   - 发布新版本

---

## 行为准则

### 我们的承诺

为了营造开放和友好的环境，我们承诺：

- 🤝 尊重不同的观点和经验
- 💬 优雅地接受建设性批评
- 🎯 专注于对社区最有利的事情
- 🌟 对其他社区成员表示同理心

### 不可接受的行为

- ❌ 使用性化语言或图像
- ❌ 恶意评论、人身攻击或侮辱
- ❌ 骚扰
- ❌ 未经许可发布他人的私人信息
- ❌ 其他在专业场合被认为不当的行为

---

## 获取帮助

如果您需要帮助：

- 📧 联系维护者: your-email@example.com
- 💬 GitHub Discussions
- 🐛 GitHub Issues
- 📚 查看文档

---

感谢您的贡献！🎉
