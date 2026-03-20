@echo off
echo ============================================
echo         Git 安装脚本
echo ============================================
echo.
echo 此脚本将帮助您安装Git，以便将代码上传到GitHub。
echo.

REM 检查是否已安装Git
where git >nul 2>nul
if %errorlevel% equ 0 (
    echo ✓ Git 已安装
    git --version
    goto :SKIP_INSTALL
)

echo 正在下载Git安装程序...
echo 请访问: https://git-scm.com/download/win
echo.
echo 或者使用winget安装（如果可用）:
echo winget install --id Git.Git -e --source winget
echo.

echo 安装完成后，请重新打开命令提示符并运行:
echo git --version
echo 来验证安装。
echo.

:SKIP_INSTALL
echo.
echo 安装Git后，请按照以下步骤上传代码到GitHub:
echo.
echo 1. 打开命令提示符，导航到当前目录
echo 2. 运行: git init
echo 3. 运行: git add .
echo 4. 运行: git commit -m "Initial commit"
echo 5. 运行: git remote add origin https://github.com/lamhui763-sys/AI-
echo 6. 运行: git push -u origin main
echo.
echo 注意: 第5步的仓库地址可能需要调整，确保正确。
echo.
pause