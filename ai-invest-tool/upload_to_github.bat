@echo off
echo ============================================
echo      GitHub上传助手
echo ============================================
echo.
echo 此脚本将引导您将AI投资工具项目上传到GitHub。
echo.

REM 检查Git是否安装
where git >nul 2>nul
if %errorlevel% neq 0 (
    echo ✗ Git未安装
    echo 请先安装Git：
    echo 1. 访问 https://git-scm.com/download/win
    echo 2. 下载并安装Git for Windows
    echo 3. 重新运行此脚本
    echo.
    echo 或者运行 install_git.bat 获取详细指南
    pause
    exit /b 1
)

echo ✓ Git已安装
git --version
echo.

echo 当前目录：%cd%
echo.

echo 步骤1：初始化Git仓库
git init
echo.

echo 步骤2：添加文件到暂存区
git add .
echo.

echo 步骤3：提交更改
git commit -m "Initial commit: AI投资工具项目"
echo.

echo 步骤4：连接到GitHub远程仓库
echo.
echo 重要：您需要提供完整的GitHub仓库地址
echo 例如：https://github.com/lamhui763-sys/AI-invest-tool.git
echo.
set /p repo_url="请输入您的GitHub仓库地址: "

if "%repo_url%"=="" (
    echo 错误：未提供仓库地址
    echo 请先创建GitHub仓库并获取地址
    pause
    exit /b 1
)

echo 正在添加远程仓库：%repo_url%
git remote add origin "%repo_url%"
if %errorlevel% neq 0 (
    echo 错误：添加远程仓库失败
    pause
    exit /b 1
)

echo.
echo 步骤5：推送代码到GitHub
echo 注意：首次推送可能需要身份验证
echo.
git branch -M main
git push -u origin main

if %errorlevel% equ 0 (
    echo.
    echo ✓ 恭喜！代码已成功推送到GitHub
    echo 仓库地址：%repo_url%
) else (
    echo.
    echo ✗ 推送失败
    echo 可能的原因：
    echo 1. 身份验证失败 - 请检查用户名和密码/令牌
    echo 2. 网络问题 - 请检查网络连接
    echo 3. 权限不足 - 确保您有权限推送到该仓库
    echo.
    echo 请查看详细指南：GITHUB_UPLOAD_GUIDE.md
)

echo.
pause