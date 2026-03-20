@echo off
chcp 65001 >nul
title AI投資工具
cd /d "%~dp0"

cls
echo ========================================
echo    AI投資工具 - 正在啟動...
echo ========================================
echo.
echo 提示：這個窗口必須保持打開！
echo       關閉此窗口將停止應用
echo.
echo ========================================
echo.

REM 檢查Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [錯誤] 找不到Python！
    echo.
    echo 請先安裝Python：
    echo 1. 訪問 https://www.python.org/downloads/
    echo 2. 下載並安裝Python
    echo 3. 安裝時務必勾選 [√] Add Python to PATH
    echo 4. 重新啟動電腦
    echo 5. 再次運行此腳本
    echo.
    pause
    exit /b 1
)

echo [檢測] Python已找到
echo.

REM 檢查Streamlit
python -c "import streamlit" >nul 2>&1
if %errorlevel% neq 0 (
    echo [提示] 首次運行，正在安裝依賴...
    echo 這可能需要2-5分鐘，請耐心等待...
    echo.
    python -m pip install streamlit yfinance pandas plotly openpyxl numpy --quiet
    echo.
    echo [完成] 依賴安裝完成
    echo.
)

echo [啟動] 正在啟動Web服務器...
echo.
echo 瀏覽器將自動打開：http://localhost:8501
echo.
echo 如果瀏覽器沒有自動打開，請手動輸入上面的地址
echo.
echo ========================================
echo.

REM 啟動瀏覽器（延遲3秒）
start "" cmd /c "timeout /t 3 /nobreak >nul && start http://localhost:8501"

REM 啟動Streamlit
python -m streamlit run src/ai_inv/web_dashboard.py --server.port 8501

echo.
echo ========================================
echo 應用已停止
echo ========================================
echo.
pause
