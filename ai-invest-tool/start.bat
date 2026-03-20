@echo off
echo ====================================
echo AI投资工具 - Web界面启动器
echo ====================================
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] 未检测到Python，请先安装Python
    echo 下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [1/5] 检查Python环境...
python --version

echo.
echo [2/5] 检查虚拟环境...
if not exist "venv" (
    echo [提示] 虚拟环境不存在，正在创建...
    python -m venv venv
    echo [完成] 虚拟环境创建成功
)

echo [3/5] 激活虚拟环境...
call venv\Scripts\activate.bat

echo.
echo [4/5] 安装/更新依赖包...
pip install -q streamlit plotly openpyxl pandas numpy yfinance openai

echo.
echo [5/5] 启动Web界面...
echo ====================================
echo.
echo Web界面正在启动...
echo.
echo 浏览器会自动打开，如果没有，请访问:
echo http://localhost:8501
echo.
echo 按 Ctrl+C 停止服务器
echo ====================================
echo.

streamlit run src/ai_inv/web_dashboard.py

pause
