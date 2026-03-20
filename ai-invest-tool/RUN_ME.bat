@echo off
chcp 65001 >nul
title AI投資工具 - 啟動器
color 0A

cls
echo.
echo ========================================
echo    AI投資工具 - 一鍵啟動
echo ========================================
echo.

cd /d "%~dp0"

echo [提示] 正在檢查系統...
echo.

REM 嘗試不同的Python命令
python --version >nul 2>&1
if %errorlevel% equ 0 (
    set PYTHON_CMD=python
    goto :found_python
)

py --version >nul 2>&1
if %errorlevel% equ 0 (
    set PYTHON_CMD=py
    goto :found_python
)

python3 --version >nul 2>&1
if %errorlevel% equ 0 (
    set PYTHON_CMD=python3
    goto :found_python
)

echo ========================================
echo [錯誤] 找不到Python！
echo ========================================
echo.
echo 請按照以下步驟安裝Python：
echo.
echo 1. 打開瀏覽器訪問：
echo    https://www.python.org/downloads/
echo.
echo 2. 下載Python 3.8或更高版本
echo.
echo 3. 運行安裝程序
echo.
echo 4. 重要：安裝時務必勾選：
echo    [√] Add Python to PATH
echo    [√] Install for all users
echo.
echo 5. 安裝完成後，重新啟動電腦
echo.
echo 6. 再次運行此文件
echo.
echo ========================================
echo.
pause
exit /b 1

:found_python
echo [成功] 找到Python: %PYTHON_CMD%
%PYTHON_CMD% --version
echo.

echo [檢查] 正在檢查Streamlit...
%PYTHON_CMD% -c "import streamlit" >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo [提示] 首次運行，需要安裝依賴包
    echo 這可能需要2-5分鐘，請耐心等待...
    echo.
    
    echo 正在安裝: streamlit
    %PYTHON_CMD% -m pip install streamlit --quiet
    
    echo 正在安裝: yfinance
    %PYTHON_CMD% -m pip install yfinance --quiet
    
    echo 正在安裝: pandas
    %PYTHON_CMD% -m pip install pandas --quiet
    
    echo 正在安裝: plotly
    %PYTHON_CMD% -m pip install plotly --quiet
    
    echo 正在安裝: openpyxl
    %PYTHON_CMD% -m pip install openpyxl --quiet
    
    echo 正在安裝: numpy
    %PYTHON_CMD% -m pip install numpy --quiet
    
    echo 正在安裝: pyyaml
    %PYTHON_CMD% -m pip install pyyaml --quiet
    
    echo 正在安裝: matplotlib
    %PYTHON_CMD% -m pip install matplotlib --quiet
    
    echo 正在安裝: scikit-learn
    %PYTHON_CMD% -m pip install scikit-learn --quiet
    
    echo 正在安裝: requests
    %PYTHON_CMD% -m pip install requests --quiet
    
    echo.
    echo [完成] 依賴安裝完成
    echo.
)

echo [啟動] 正在啟動Web服務器...
echo.
echo ========================================
echo 重要提示：
echo - 此窗口必須保持打開
echo - 關閉此窗口將停止應用
echo - 按 Ctrl+C 可停止服務器
echo ========================================
echo.
echo Web應用將在瀏覽器中打開：
echo http://localhost:8501
echo.
echo 如果瀏覽器沒有自動打開，
echo 請手動輸入上面的地址
echo.
echo ========================================
echo.

REM 延遲3秒後打開瀏覽器
start "" cmd /c "ping 127.0.0.1 -n 4 >nul && start http://localhost:8501"

REM 啟動Streamlit
%PYTHON_CMD% -m streamlit run src\ai_inv\web_dashboard.py --server.port 8501

echo.
echo ========================================
echo 應用已停止
echo ========================================
echo.
pause
