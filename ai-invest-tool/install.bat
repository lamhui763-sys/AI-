@echo off
chcp 65001 >nul
title AI投資工具 - 安裝程序
cd /d "%~dp0"

echo ====================================
echo AI投資工具 - 自動安裝程序
echo ====================================
echo.

echo 正在啟動安裝程序...
echo.

python setup.py

if %errorlevel% neq 0 (
    echo.
    echo 安裝失敗，請檢查Python是否正確安裝
    pause
)
