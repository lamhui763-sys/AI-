# AI投資工具 - 自動安裝腳本
# AI Investment Tool - Auto Installer

Write-Host "====================================" -ForegroundColor Cyan
Write-Host "AI投資工具 - 自動安裝程序" -ForegroundColor Cyan
Write-Host "====================================" -ForegroundColor Cyan
Write-Host ""

# 設置目錄
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptDir

# 步驟1：檢查Python
Write-Host "步驟 1: 檢查Python環境" -ForegroundColor Green
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ Python版本: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Python未找到，請先安裝Python" -ForegroundColor Red
    Write-Host "  訪問: https://www.python.org/downloads/" -ForegroundColor Yellow
    Write-Host "  安裝時務必勾選 'Add Python to PATH'" -ForegroundColor Yellow
    Read-Host "按Enter鍵退出"
    exit 1
}

# 步驟2：安裝依賴
Write-Host ""
Write-Host "步驟 2: 安裝依賴包" -ForegroundColor Green
Write-Host "這可能需要2-5分鐘，請耐心等待..." -ForegroundColor Yellow
Write-Host ""

$packages = @(
    'streamlit',
    'yfinance',
    'pandas',
    'plotly',
    'openpyxl',
    'numpy',
    'matplotlib',
    'scikit-learn',
    'requests'
)

foreach ($pkg in $packages) {
    Write-Host "正在安裝 $pkg..." -ForegroundColor Cyan
    python -m pip install $pkg --quiet
}

Write-Host ""
Write-Host "✓ 所有依賴安裝完成！" -ForegroundColor Green

# 步驟3：創建啟動腳本
Write-Host ""
Write-Host "步驟 3: 創建啟動腳本" -ForegroundColor Green

$batContent = @"
@echo off
chcp 65001 >nul
title AI投資工具
cd /d "%~dp0"
echo ====================================
echo AI投資工具 - 正在啟動...
echo ====================================
echo.
python -m streamlit run src/ai_inv/web_dashboard.py
echo.
echo 應用已關閉
pause
"@

$batPath = Join-Path $scriptDir "啟動AI工具.bat"
$batContent | Out-File -FilePath $batPath -Encoding UTF8

Write-Host "✓ 啟動腳本已創建: 啟動AI工具.bat" -ForegroundColor Green

# 步驟4：在桌面創建快捷方式
Write-Host ""
Write-Host "步驟 4: 創建桌面快捷方式" -ForegroundColor Green

try {
    $WshShell = New-Object -ComObject WScript.Shell
    $desktop = [Environment]::GetFolderPath("Desktop")
    $shortcutPath = Join-Path $desktop "AI投資工具.lnk"

    $shortcut = $WshShell.CreateShortcut($shortcutPath)
    $shortcut.TargetPath = $batPath
    $shortcut.WorkingDirectory = $scriptDir
    $shortcut.Description = "AI Investment Tool - Click to launch"
    $shortcut.Save()

    Write-Host "✓ 桌面快捷方式已創建!" -ForegroundColor Green
    Write-Host "  位置: $shortcutPath" -ForegroundColor Cyan
} catch {
    Write-Host "⚠ 無法創建桌面快捷方式" -ForegroundColor Yellow
    Write-Host "  但您仍然可以雙擊 '啟動AI工具.bat' 來啟動應用" -ForegroundColor Yellow
}

# 步驟5：驗證安裝
Write-Host ""
Write-Host "步驟 5: 驗證安裝" -ForegroundColor Green

$imports = @{
    'streamlit' = 'streamlit'
    'yfinance' = 'yfinance'
    'pandas' = 'pandas'
    'plotly' = 'plotly'
    'openpyxl' = 'openpyxl'
}

$allSuccess = $true
foreach ($module in $imports.Keys) {
    try {
        $result = python -c "import $module; print($module.__version__)" 2>&1
        Write-Host "✓ $module: $result" -ForegroundColor Green
    } catch {
        Write-Host "✗ $module: 安裝失敗" -ForegroundColor Red
        $allSuccess = $false
    }
}

# 完成
Write-Host ""
Write-Host "====================================" -ForegroundColor Cyan
Write-Host "✓✓✓ 安裝完成！" -ForegroundColor Green -BackgroundColor Black
Write-Host "====================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "🚀 如何啟動：" -ForegroundColor Yellow
Write-Host "   方法1: 雙擊桌面上的「AI投資工具」圖標" -ForegroundColor White
Write-Host "   方法2: 雙擊項目目錄下的「啟動AI工具.bat」" -ForegroundColor White
Write-Host "   方法3: 在命令行運行: streamlit run src/ai_inv/web_dashboard.py" -ForegroundColor White

Write-Host ""
Write-Host "📱 使用說明：" -ForegroundColor Yellow
Write-Host "   1. 啟動後，瀏覽器會自動打開 http://localhost:8501" -ForegroundColor White
Write-Host "   2. 在「股票分析」頁面輸入股票代碼（如：^HSI）" -ForegroundColor White
Write-Host "   3. 點擊「開始分析」查看結果" -ForegroundColor White
Write-Host "   4. 點擊「導出為Excel」生成報告" -ForegroundColor White

Write-Host ""
Write-Host "📚 更多幫助：" -ForegroundColor Yellow
Write-Host "   - 查看 README.md 了解完整功能" -ForegroundColor White
Write-Host "   - 查看 QUICKSTART.md 快速上手" -ForegroundColor White
Write-Host "   - 查看 安裝完成說明.md 使用指南" -ForegroundColor White

# 詢問是否立即啟動
Write-Host ""
Write-Host "====================================" -ForegroundColor Cyan
$response = Read-Host "是否立即啟動應用？(Y/n)"

if ($response -ne 'n' -and $response -ne 'N') {
    Write-Host ""
    Write-Host "正在啟動應用..." -ForegroundColor Yellow
    Write-Host ""

    Start-Process python -ArgumentList "-m", "streamlit", "run", "src/ai_inv/web_dashboard.py"
    Start-Sleep -Seconds 3
    Start-Process "http://localhost:8501"

    Write-Host ""
    Write-Host "✓ 應用已啟動！" -ForegroundColor Green
    Write-Host "  如果瀏覽器沒有自動打開，請手動訪問: http://localhost:8501" -ForegroundColor White
} else {
    Write-Host ""
    Write-Host "稍後您可以雙擊桌面圖標啟動應用" -ForegroundColor Yellow
}

Write-Host ""
Read-Host "按Enter鍵退出"
