@echo off
chcp 65001 >nul
title SkillHub CLI 安裝程序

echo ========================================
echo SkillHub CLI 安裝程序
echo ========================================
echo.

REM 設置安裝目錄
set "INSTALL_DIR=%USERPROFILE%\.skillhub"
set "BIN_DIR=%INSTALL_DIR%\bin"
set "CLI_URL=https://skillhub-1388575217.cos.ap-guangzhou.myqcloud.com/cli/skillhub.exe"
set "CLI_PATH=%BIN_DIR%\skillhub.exe"

echo [1/4] 創建安裝目錄...
if not exist "%BIN_DIR%" (
    mkdir "%BIN_DIR%" 2>nul
    echo   已創建: %BIN_DIR%
) else (
    echo   目錄已存在: %BIN_DIR%
)
echo.

echo [2/4] 下載 SkillHub CLI...
echo   正在下載...
powershell -Command "Invoke-WebRequest -Uri '%CLI_URL%' -OutFile '%CLI_PATH%' -UseBasicParsing"
if exist "%CLI_PATH%" (
    echo   下載完成: %CLI_PATH%
) else (
    echo   錯誤: 下載失敗
    pause
    exit /b 1
)
echo.

echo [3/4] 添加到 PATH...
powershell -Command "$currentPath = [Environment]::GetEnvironmentVariable('PATH', 'User'); if ($currentPath -notlike '*%BIN_DIR%*') { [Environment]::SetEnvironmentVariable('PATH', \"$currentPath;%BIN_DIR%\", 'User'); Write-Host '  已添加到 PATH' } else { Write-Host '  PATH 已配置' }"
echo.

echo [4/4] 驗證安裝...
if exist "%CLI_PATH%" (
    "%CLI_PATH%" --version 2>nul
    if %errorlevel% equ 0 (
        echo   安裝成功！
    ) else (
        echo   警告: 無法執行 skillhub --version
    )
) else (
    echo   錯誤: CLI 文件不存在
)
echo.

echo ========================================
echo 安裝完成！
echo ========================================
echo.
echo 安裝位置: %CLI_PATH%
echo.
echo 常用命令:
echo   skillhub search [關鍵詞]    - 搜索可用技能
echo   skillhub install [技能名]   - 安裝技能
echo   skillhub list               - 列出已安裝技能
echo   skillhub --help             - 查看幫助
echo.
echo 下一步:
echo   1. 重新啟動終端
echo   2. 運行: skillhub --version
echo   3. 搜索技能: skillhub search
echo.
pause
