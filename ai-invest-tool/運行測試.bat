@echo off
echo ====================================
echo 運行簡單測試
echo ====================================
echo.

cd /d "%~dp0"

echo 正在檢查Python...
python simple_test.py

echo.
echo ====================================
echo 測試完成
echo ====================================
echo.
pause
