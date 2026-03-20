# SkillHub CLI 安裝腳本 (Windows 版本)
# 僅安裝 CLI 工具

param(
    [switch]$CliOnly = $true
)

$ErrorActionPreference = "Stop"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "SkillHub CLI 安裝程序" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 設置安裝目錄
$InstallDir = Join-Path $env:USERPROFILE ".skillhub"
$BinDir = Join-Path $InstallDir "bin"

Write-Host "[1/4] 創建安裝目錄..." -ForegroundColor Yellow

if (-not (Test-Path $InstallDir)) {
    New-Item -ItemType Directory -Path $InstallDir -Force | Out-Null
    Write-Host "  創建目錄: $InstallDir" -ForegroundColor Gray
}

if (-not (Test-Path $BinDir)) {
    New-Item -ItemType Directory -Path $BinDir -Force | Out-Null
    Write-Host "  創建目錄: $BinDir" -ForegroundColor Gray
}

Write-Host "  完成" -ForegroundColor Green
Write-Host ""

# 下載 SkillHub CLI
Write-Host "[2/4] 下載 SkillHub CLI..." -ForegroundColor Yellow

$CliUrl = "https://skillhub-1388575217.cos.ap-guangzhou.myqcloud.com/cli/skillhub.exe"
$CliPath = Join-Path $BinDir "skillhub.exe"

try {
    # 檢查是否已有舊版本
    if (Test-Path $CliPath) {
        Write-Host "  發現舊版本，正在更新..." -ForegroundColor Gray
        Remove-Item $CliPath -Force
    }
    
    # 下載新版本
    Write-Host "  正在下載..." -ForegroundColor Gray
    Invoke-WebRequest -Uri $CliUrl -OutFile $CliPath -UseBasicParsing
    Write-Host "  完成" -ForegroundColor Green
} catch {
    Write-Host "  錯誤: 無法下載 CLI" -ForegroundColor Red
    Write-Host "  詳情: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

Write-Host ""

# 配置 PATH
Write-Host "[3/4] 配置環境變量..." -ForegroundColor Yellow

$CurrentPath = [Environment]::GetEnvironmentVariable("PATH", "User")
if ($CurrentPath -notlike "*$BinDir*") {
    [Environment]::SetEnvironmentVariable("PATH", "$CurrentPath;$BinDir", "User")
    Write-Host "  已添加到 PATH: $BinDir" -ForegroundColor Gray
    Write-Host "  注意: 需要重新啟動終端才能生效" -ForegroundColor Yellow
} else {
    Write-Host "  PATH 已配置" -ForegroundColor Gray
}

Write-Host "  完成" -ForegroundColor Green
Write-Host ""

# 驗證安裝
Write-Host "[4/4] 驗證安裝..." -ForegroundColor Yellow

try {
    $Version = & $CliPath --version 2>&1
    Write-Host "  SkillHub CLI 版本: $Version" -ForegroundColor Green
} catch {
    Write-Host "  警告: 無法獲取版本信息" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "安裝完成！" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "安裝位置: $CliPath" -ForegroundColor White
Write-Host ""

Write-Host "常用命令:" -ForegroundColor Yellow
Write-Host "  skillhub search [關鍵詞]    - 搜索可用技能" -ForegroundColor White
Write-Host "  skillhub install [技能名]   - 安裝技能到當前工作區" -ForegroundColor White
Write-Host "  skillhub list               - 列出已安裝的技能" -ForegroundColor White
Write-Host "  skillhub --help             - 查看幫助" -ForegroundColor White
Write-Host ""

Write-Host "下一步:" -ForegroundColor Yellow
Write-Host "1. 重新啟動終端或命令提示符" -ForegroundColor White
Write-Host "2. 運行 'skillhub --version' 驗證安裝" -ForegroundColor White
Write-Host "3. 運行 'skillhub search [關鍵詞]' 搜索技能" -ForegroundColor White
Write-Host ""
