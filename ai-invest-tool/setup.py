"""
AI投資工具 - 安裝程序
這個腳本會自動安裝所有依賴並在桌面創建快捷方式
"""

import os
import sys
import subprocess
import webbrowser
from pathlib import Path
import time

def print_step(step, message):
    """打印安裝步驟"""
    print(f"\n{'='*60}")
    print(f"步驟 {step}: {message}")
    print('='*60)

def check_python():
    """檢查Python版本"""
    print_step(1, "檢查Python環境")
    print(f"Python版本: {sys.version}")
    print(f"Python路徑: {sys.executable}")
    return True

def install_dependencies():
    """安裝依賴包"""
    print_step(2, "安裝依賴包")

    dependencies = [
        'streamlit',
        'yfinance',
        'pandas',
        'plotly',
        'openpyxl',
        'numpy',
        'matplotlib',
        'scikit-learn',
        'requests'
    ]

    print("\n需要安裝以下包:")
    for dep in dependencies:
        print(f"  - {dep}")

    print("\n正在安裝...（這可能需要2-5分鐘，請耐心等待）\n")

    try:
        # 使用pip安裝
        cmd = [sys.executable, '-m', 'pip', 'install'] + dependencies
        subprocess.run(cmd, check=True, capture_output=False)
        print("\n✓ 所有依賴包安裝成功！")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n✗ 安裝失敗: {e}")
        return False

def create_desktop_shortcut():
    """在桌面創建快捷方式"""
    print_step(3, "創建桌面快捷方式")

    try:
        import win32com.client

        # 獲取桌面路徑
        desktop = os.path.join(os.path.expanduser("~"), "Desktop")

        # 項目路徑
        project_path = os.path.dirname(os.path.abspath(__file__))
        script_path = os.path.join(project_path, "run_ai_tool.bat")

        # 創建啟動腳本
        create_launch_script(project_path)

        # 創建快捷方式
        shortcut_path = os.path.join(desktop, "AI投資工具.lnk")
        shell = win32com.client.Dispatch("WScript.Shell")
        shortcut = shell.CreateShortCut(shortcut_path)

        shortcut.Targetpath = script_path
        shortcut.WorkingDirectory = project_path
        shortcut.Description = "AI Investment Tool - Click to launch"
        shortcut.IconLocation = script_path
        shortcut.save()

        print(f"\n✓ 桌面快捷方式已創建:")
        print(f"  {shortcut_path}")
        return True

    except ImportError:
        print("\n⚠ 需要安裝 pywin32 才能創建快捷方式")
        print("正在安裝 pywin32...")

        try:
            subprocess.run([sys.executable, '-m', 'pip', 'install', 'pywin32'], check=True)
            print("✓ pywin32 安裝成功，正在重試創建快捷方式...")
            return create_desktop_shortcut()
        except:
            print("✗ 無法創建快捷方式，請手動運行腳本")
            return False

    except Exception as e:
        print(f"\n✗ 創建快捷方式失敗: {e}")
        print("但工具仍然可以使用，請手動運行啟動腳本")
        return False

def create_launch_script(project_path):
    """創建啟動腳本"""
    script_content = '''@echo off
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
'''

    script_path = os.path.join(project_path, "run_ai_tool.bat")
    with open(script_path, 'w', encoding='utf-8') as f:
        f.write(script_content)

    print(f"✓ 啟動腳本已創建: {script_path}")

def verify_installation():
    """驗證安裝"""
    print_step(4, "驗證安裝")

    try:
        import streamlit
        print(f"✓ Streamlit {streamlit.__version__}")

        import yfinance
        print(f"✓ yfinance {yfinance.__version__}")

        import pandas
        print(f"✓ pandas {pandas.__version__}")

        import plotly
        print(f"✓ plotly {plotly.__version__}")

        import openpyxl
        print(f"✓ openpyxl {openpyxl.__version__}")

        print("\n✓ 所有組件驗證成功！")
        return True

    except ImportError as e:
        print(f"\n✗ 驗證失敗: {e}")
        return False

def main():
    """主函數"""
    print("\n" + "="*60)
    print("   AI投資工具 - 自動安裝程序")
    print("   AI Investment Tool - Auto Installer")
    print("="*60)

    # 步驟1：檢查Python
    if not check_python():
        print("\n✗ Python環境檢查失敗！")
        input("\n按Enter鍵退出...")
        sys.exit(1)

    # 步驟2：安裝依賴
    if not install_dependencies():
        print("\n✗ 依賴安裝失敗！")
        input("\n按Enter鍵退出...")
        sys.exit(1)

    # 步驟3：創建快捷方式
    create_desktop_shortcut()

    # 步驟4：驗證安裝
    if not verify_installation():
        print("\n✗ 安裝驗證失敗！")
        input("\n按Enter鍵退出...")
        sys.exit(1)

    # 完成
    print("\n" + "="*60)
    print("   ✓✓✓ 安裝完成！✓✓✓")
    print("="*60)

    print("\n🎉 恭喜！AI投資工具已成功安裝！\n")

    print("🚀 如何啟動：")
    print("   方法1：雙擊桌面上的「AI投資工具」圖標")
    print("   方法2：運行項目目錄下的 run_ai_tool.bat")
    print("   方法3：在命令行運行: streamlit run src/ai_inv/web_dashboard.py")

    print("\n📱 使用說明：")
    print("   1. 啟動後，瀏覽器會自動打開 http://localhost:8501")
    print("   2. 在「股票分析」頁面輸入股票代碼（如：^HSI）")
    print("   3. 點擊「開始分析」查看結果")
    print("   4. 點擊「導出為Excel」生成報告")

    print("\n📚 更多幫助：")
    print("   - 查看 README.md 了解完整功能")
    print("   - 查看 QUICKSTART.md 快速上手")
    print("   - 查看 安裝完成說明.md 使用指南")

    # 詢問是否立即啟動
    print("\n" + "="*60)
    response = input("是否立即啟動應用？(Y/n): ").strip().upper()

    if response != 'N':
        print("\n正在啟動應用...\n")
        time.sleep(1)

        try:
            # 啟動Streamlit
            os.chdir(os.path.dirname(os.path.abspath(__file__)))
            subprocess.run([sys.executable, '-m', 'streamlit', 'run', 'src/ai_inv/web_dashboard.py'])
        except KeyboardInterrupt:
            print("\n\n應用已停止")

    else:
        print("\n稍後您可以雙擊桌面圖標啟動應用")
        input("\n按Enter鍵退出...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n安裝已取消")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n發生錯誤: {e}")
        import traceback
        traceback.print_exc()
        input("\n按Enter鍵退出...")
        sys.exit(1)
