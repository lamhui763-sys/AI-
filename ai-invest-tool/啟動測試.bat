@echo off
chcp 65001 >nul
title AI投資工具 - 測試模式
cd /d "%~dp0"

echo ====================================
echo AI投資工具 - 測試模式
echo ====================================
echo.
echo 正在啟動測試頁面...
echo.

where python >nul 2>&1
if %errorlevel% neq 0 (
    echo 錯誤：找不到Python
    echo 請先安裝Python 3.8或更高版本
    echo 訪問：https://www.python.org/downloads/
    echo 安裝時務必勾選 "Add Python to PATH"
    pause
    exit /b 1
)

echo Python已找到
echo 正在啟動Streamlit...
echo.
echo 瀏覽器將打開: http://localhost:8501
echo.
echo ====================================
echo.

python -m streamlit run test_dashboard.py

echo.
echo 應用已關閉
pause
