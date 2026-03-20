@echo off
chcp 65001 >nul
title 系統診斷
cd /d "%~dp0"

echo ====================================
echo AI投資工具 - 系統診斷
echo ====================================
echo.

echo 檢查1: Python
echo --------------------------------
where python >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] Python已找到
    python --version
) else (
    echo [FAIL] Python未找到
    echo 請先安裝Python: https://www.python.org/downloads/
    echo 安裝時務必勾選 "Add Python to PATH"
)
echo.

echo 檢查2: pip
echo --------------------------------
where pip >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] pip已找到
    pip --version
) else (
    echo [FAIL] pip未找到
)
echo.

echo 檢查3: Streamlit
echo --------------------------------
python -c "import streamlit; print(f'Version: {streamlit.__version__}')" 2>nul
if %errorlevel% equ 0 (
    echo [OK] Streamlit已安裝
    python -c "import streamlit; print(f'Version: {streamlit.__version__}')"
) else (
    echo [FAIL] Streamlit未安裝
    echo 正在安裝...
    python -m pip install streamlit --quiet
)
echo.

echo 檢查4: yfinance
echo --------------------------------
python -c "import yfinance; print(f'Version: {yfinance.__version__}')" 2>nul
if %errorlevel% equ 0 (
    echo [OK] yfinance已安裝
) else (
    echo [FAIL] yfinance未安裝
    echo 正在安裝...
    python -m pip install yfinance --quiet
)
echo.

echo 檢查5: pandas
echo --------------------------------
python -c "import pandas; print(f'Version: {pandas.__version__}')" 2>nul
if %errorlevel% equ 0 (
    echo [OK] pandas已安裝
) else (
    echo [FAIL] pandas未安裝
    echo 正在安裝...
    python -m pip install pandas --quiet
)
echo.

echo 檢查6: plotly
echo --------------------------------
python -c "import plotly; print(f'Version: {plotly.__version__}')" 2>nul
if %errorlevel% equ 0 (
    echo [OK] plotly已安裝
) else (
    echo [FAIL] plotly未安裝
    echo 正在安裝...
    python -m pip install plotly --quiet
)
echo.

echo 檢查7: openpyxl
echo --------------------------------
python -c "import openpyxl; print(f'Version: {openpyxl.__version__}')" 2>nul
if %errorlevel% equ 0 (
    echo [OK] openpyxl已安裝
) else (
    echo [FAIL] openpyxl未安裝
    echo 正在安裝...
    python -m pip install openpyxl --quiet
)
echo.

echo 檢查8: 項目文件
echo --------------------------------
if exist "src\ai_inv\web_dashboard.py" (
    echo [OK] Web Dashboard文件存在
) else (
    echo [FAIL] Web Dashboard文件不存在
)
echo.

echo ====================================
echo 診斷完成
echo ====================================
echo.
echo 如果所有檢查都顯示 [OK]，請運行：
echo   啟動AI工具.bat
echo.
echo 如果有 [FAIL] 請按照提示修復
echo.
pause
