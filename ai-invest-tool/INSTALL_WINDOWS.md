# Windows 安裝和啟動指南

## 🔧 方法1：手動安裝（推薦）

### 步驟1：安裝Python

如果還沒有安裝Python，請：
1. 訪問 https://www.python.org/downloads/
2. 下載並安裝Python 3.8或更高版本
3. **重要**：安裝時勾選 "Add Python to PATH"

### 步驟2：打開命令提示符或PowerShell

按 `Win + R`，輸入 `cmd` 或 `powershell`，按回車

### 步驟3：進入項目目錄

```cmd
cd C:\Users\makai\WorkBuddy\Claw\ai-invest-tool
```

### 步驟4：安裝依賴

```cmd
pip install streamlit yfinance pandas plotly openpyxl
```

或者使用：
```cmd
python -m pip install streamlit yfinance pandas plotly openpyxl
```

等待安裝完成（大約2-5分鐘）

### 步驟5：啟動應用

```cmd
streamlit run src/ai_inv/web_dashboard.py
```

### 步驟6：打開瀏覽器

瀏覽器會自動打開，或者手動訪問：
```
http://localhost:8501
```

## 🚀 方法2：一鍵啟動（最簡單）

### 步驟1：雙擊啟動腳本

在文件管理器中找到：
```
C:\Users\makai\WorkBuddy\Claw\ai-invest-tool\start_tool.bat
```

雙擊這個文件

### 步驟2：等待安裝和啟動

腳本會自動：
1. 檢查Python
2. 安裝所有依賴
3. 啟動Web界面

### 步驟3：打開瀏覽器

瀏覽器會自動打開，或手動訪問：
```
http://localhost:8501
```

## ❓ 故障排除

### 問題1：Python找不到

**錯誤信息**：`'python' is not recognized`

**解決方法**：
1. 確認Python已安裝
2. 重新安裝Python，確保勾選 "Add Python to PATH"
3. 或使用完整路徑：
   ```cmd
   C:\Users\makai\AppData\Local\Programs\Python\Python3x\python.exe -m pip install ...
   ```

### 問題2：pip找不到

**錯誤信息**：`'pip' is not recognized`

**解決方法**：
```cmd
python -m pip install streamlit yfinance pandas plotly openpyxl
```

### 問題3：無法連接到localhost

**錯誤信息**：`ERR_CONNECTION_REFUSED`

**解決方法**：

1. 檢查Streamlit是否在運行
   - 命令窗口應該顯示：
     ```
     You can now view your Streamlit app in your browser.
     Local URL: http://localhost:8501
     ```

2. 檢查端口8501是否被佔用
   ```cmd
   netstat -ano | findstr :8501
   ```

3. 嘗試使用不同端口
   ```cmd
   streamlit run src/ai_inv/web_dashboard.py --server.port 8502
   ```

### 問題4：權限錯誤

**錯誤信息**：`Permission denied`

**解決方法**：
- 以管理員身份運行命令提示符（右鍵選擇"以管理員身份運行"）
- 或者安裝到用戶目錄：
  ```cmd
  pip install --user streamlit yfinance pandas plotly openpyxl
  ```

### 問題5：網絡錯誤

**錯誤信息**：無法連接到pypi.org或GitHub

**解決方法**：
1. 檢查網絡連接
2. 如果使用代理，配置pip使用代理：
   ```cmd
   set HTTP_PROXY=http://your-proxy:port
   set HTTPS_PROXY=http://your-proxy:port
   pip install ...
   ```

## 🔍 驗證安裝

運行以下命令驗證所有依賴已正確安裝：

```cmd
python -c "import streamlit, yfinance, pandas, plotly; print('All packages installed successfully!')"
```

如果沒有錯誤，說明安裝成功。

## 📊 安裝後測試

### 測試1：檢查Python和依賴

創建測試文件 `test_env.py`：

```python
import sys
print(f"Python version: {sys.version}")

try:
    import streamlit
    print(f"✓ Streamlit: {streamlit.__version__}")
except ImportError:
    print("✗ Streamlit not installed")

try:
    import yfinance
    print(f"✓ yfinance: {yfinance.__version__}")
except ImportError:
    print("✗ yfinance not installed")

try:
    import pandas
    print(f"✓ pandas: {pandas.__version__}")
except ImportError:
    print("✗ pandas not installed")

try:
    import plotly
    print(f"✓ plotly: {plotly.__version__}")
except ImportError:
    print("✗ plotly not installed")

try:
    import openpyxl
    print(f"✓ openpyxl: {openpyxl.__version__}")
except ImportError:
    print("✗ openpyxl not installed")
```

運行：
```cmd
python test_env.py
```

### 測試2：啟動應用

```cmd
streamlit run src/ai_inv/web_dashboard.py
```

應該看到：
```
You can now view your Streamlit app in your browser.
Local URL: http://localhost:8501
Network URL: http://192.168.x.x:8501
```

## 💡 提示

1. **保持命令窗口打開** - Streamlit需要在命令窗口中運行才能保持Web服務器開啟
2. **Ctrl+C停止** - 按Ctrl+C可以停止Streamlit服務器
3. **端口配置** - 如果8501端口被佔用，可以使用 `--server.port` 參數更改端口
4. **自動刷新** - 修改代碼後，Streamlit會自動刷新瀏覽器（或按R鍵）

## 📞 獲取幫助

如果仍然無法運行，請：
1. 檢查錯誤信息
2. 查看項目文檔：`README.md`
3. 檢查快速開始指南：`QUICKSTART.md`
