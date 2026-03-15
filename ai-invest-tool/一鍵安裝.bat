@echo off
chcp 65001 >nul
title AI投資工具 - 一鍵安裝
cd /d "%~dp0"

echo ====================================
echo AI投資工具 - 一鍵安裝程序
echo ====================================
echo.

echo 正在安裝依賴包...
echo 這可能需要2-5分鐘，請耐心等待...
echo.

python -m pip install streamlit yfinance pandas plotly openpyxl numpy matplotlib scikit-learn requests --quiet

echo.
echo ====================================
echo 正在創建桌面快捷方式...
echo ====================================
echo.

set DESKTOP=%USERPROFILE%\Desktop
set SCRIPT_PATH=%~dp0啟動AI工具.bat

echo @echo off > "%SCRIPT_PATH%"
echo chcp 65001 ^>nul >> "%SCRIPT_PATH%"
echo cd /d "%%~dp0" >> "%SCRIPT_PATH%"
echo python -m streamlit run src/ai_inv/web_dashboard.py >> "%SCRIPT_PATH%"
echo pause >> "%SCRIPT_PATH%"

powershell -Command "$WshShell = New-Object -ComObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%DESKTOP%\AI投資工具.lnk'); $Shortcut.TargetPath = '%SCRIPT_PATH%'; $Shortcut.WorkingDirectory = '%~dp0'; $Shortcut.Description = 'AI Investment Tool'; $Shortcut.Save()"

echo.
echo ====================================
echo ✓ 安裝完成！
echo ====================================
echo.
echo 桌面已創建「AI投資工具」圖標
echo 雙擊該圖標即可啟動應用
echo.
pause
