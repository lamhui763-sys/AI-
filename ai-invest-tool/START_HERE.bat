@echo off
chcp 65001 >nul
title AI投資工具 - 完整安裝指南
color 0A

echo.
echo ========================================
echo    AI投資工具 - 完整安裝指南
echo ========================================
echo.

echo [步驟 1/5] 檢查Python環境...
echo.

REM 檢查Python是否在PATH中
python --version >nul 2>&1
if %errorlevel% equ 0 (
    echo [成功] Python已找到
    python --version
    goto :install_deps
)

echo [警告] Python未找到或未添加到PATH
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
echo.
echo 5. 完成安裝後，重新運行此腳本
echo.
echo ========================================
echo.
pause
exit /b 1

:install_deps
echo.
echo ========================================
echo [步驟 2/5] 安裝依賴包...
echo ========================================
echo.
echo 這可能需要2-5分鐘，請耐心等待...
echo.

python -m pip install --upgrade pip --quiet
python -m pip install streamlit yfinance pandas plotly openpyxl numpy matplotlib scikit-learn requests --quiet

if %errorlevel% equ 0 (
    echo.
    echo [成功] 所有依賴包已安裝
) else (
    echo.
    echo [警告] 部分依賴安裝失敗，但將繼續...
)

echo.
echo ========================================
echo [步驟 3/5] 驗證安裝...
echo ========================================
echo.

python -c "import streamlit; print('Streamlit:', streamlit.__version__)" 2>nul
if %errorlevel% equ 0 (
    echo [成功] Streamlit已安裝
) else (
    echo [失敗] Streamlit未安裝
)

python -c "import yfinance; print('yfinance:', yfinance.__version__)" 2>nul
if %errorlevel% equ 0 (
    echo [成功] yfinance已安裝
) else (
    echo [失敗] yfinance未安裝
)

python -c "import pandas; print('pandas:', pandas.__version__)" 2>nul
if %errorlevel% equ 0 (
    echo [成功] pandas已安裝
) else (
    echo [失敗] pandas未安裝
)

echo.
echo ========================================
echo [步驟 4/5] 創建桌面快捷方式...
echo ========================================
echo.

set DESKTOP=%USERPROFILE%\Desktop
set BAT_PATH=%~dp0啟動AI工具.bat

REM 創建啟動腳本
echo @echo off > "%~dp0啟動AI工具.bat"
echo chcp 65001 ^>nul >> "%~dp0啟動AI工具.bat"
echo cd /d "%%~dp0" >> "%~dp0啟動AI工具.bat"
echo echo 正在啟動AI投資工具... >> "%~dp0啟動AI工具.bat"
echo start http://localhost:8501 >> "%~dp0啟動AI工具.bat"
echo python -m streamlit run src/ai_inv/web_dashboard.py >> "%~dp0啟動AI工具.bat"
echo pause >> "%~dp0啟動AI工具.bat"

REM 創建桌面快捷方式
powershell -Command "$ws = New-Object -ComObject WScript.Shell; $s = $ws.CreateShortcut('%DESKTOP%\AI投資工具.lnk'); $s.TargetPath = '%BAT_PATH%'; $s.WorkingDirectory = '%~dp0'; $s.Save()"

if exist "%DESKTOP%\AI投資工具.lnk" (
    echo [成功] 桌面快捷方式已創建
) else (
    echo [警告] 桌面快捷方式創建失敗
)

echo.
echo ========================================
echo [步驟 5/5] 準備啟動...
echo ========================================
echo.

echo 所有準備工作已完成！
echo.
echo 現在您可以：
echo.
echo 1. 雙擊桌面上的「AI投資工具」圖標
echo 2. 或雙擊項目文件夾中的「啟動AI工具.bat」
echo.
echo 瀏覽器將自動打開：http://localhost:8501
echo.
echo ========================================

choice /C YN /M "是否現在啟動應用"
if %errorlevel% equ 1 (
    echo.
    echo 正在啟動...
    start http://localhost:8501
    python -m streamlit run src/ai_inv/web_dashboard.py
)

echo.
pause
