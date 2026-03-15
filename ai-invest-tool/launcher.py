"""
AI投資工具 - 啟動腳本
這個腳本會檢查所有依賴並啟動應用
"""

import sys
import os
import subprocess

def check_python():
    """檢查Python版本"""
    print("=" * 60)
    print("AI投資工具 - 啟動診斷")
    print("=" * 60)
    print()
    
    print("[1/5] 檢查Python環境...")
    print(f"Python版本: {sys.version}")
    print(f"Python路徑: {sys.executable}")
    print("✓ Python正常")
    print()

def check_and_install_dependencies():
    """檢查並安裝依賴"""
    print("[2/5] 檢查依賴包...")
    
    required = {
        'streamlit': 'streamlit',
        'yfinance': 'yfinance',
        'pandas': 'pandas',
        'plotly': 'plotly',
        'openpyxl': 'openpyxl',
        'numpy': 'numpy'
    }
    
    missing = []
    
    for module, package in required.items():
        try:
            __import__(module)
            print(f"  ✓ {package}")
        except ImportError:
            print(f"  ✗ {package} (缺失)")
            missing.append(package)
    
    if missing:
        print()
        print(f"正在安裝缺失的包: {', '.join(missing)}")
        print("這可能需要幾分鐘...")
        
        for package in missing:
            try:
                subprocess.run(
                    [sys.executable, '-m', 'pip', 'install', package, '--quiet'],
                    check=True
                )
                print(f"  ✓ {package} 安裝完成")
            except:
                print(f"  ✗ {package} 安裝失敗")
    
    print()

def check_project_files():
    """檢查項目文件"""
    print("[3/5] 檢查項目文件...")
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    dashboard_path = os.path.join(script_dir, 'src', 'ai_inv', 'web_dashboard.py')
    
    if os.path.exists(dashboard_path):
        print(f"  ✓ Dashboard文件存在")
        print(f"    路徑: {dashboard_path}")
    else:
        print(f"  ✗ Dashboard文件不存在！")
        print(f"    預期路徑: {dashboard_path}")
        return False
    
    print()
    return True

def start_streamlit():
    """啟動Streamlit"""
    print("[4/5] 啟動Streamlit服務器...")
    print()
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    dashboard_path = os.path.join('src', 'ai_inv', 'web_dashboard.py')
    
    print("=" * 60)
    print("重要提示：")
    print("- 這個窗口必須保持打開")
    print("- 關閉此窗口將停止應用")
    print("- 按 Ctrl+C 可以停止服務器")
    print("=" * 60)
    print()
    
    print("正在啟動...")
    print("瀏覽器將打開: http://localhost:8501")
    print()
    
    # 自動打開瀏覽器
    import threading
    import webbrowser
    import time
    
    def open_browser():
        time.sleep(5)
        webbrowser.open('http://localhost:8501')
    
    browser_thread = threading.Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()
    
    # 啟動Streamlit
    try:
        os.chdir(script_dir)
        subprocess.run([
            sys.executable, '-m', 'streamlit', 'run',
            dashboard_path,
            '--server.port', '8501'
        ])
    except KeyboardInterrupt:
        print()
        print("服務器已停止")
    except Exception as e:
        print()
        print(f"啟動失敗: {e}")

def main():
    """主函數"""
    try:
        check_python()
        check_and_install_dependencies()
        
        if not check_project_files():
            print()
            print("項目文件缺失，無法啟動")
            input("按Enter鍵退出...")
            return
        
        print("[5/5] 準備啟動...")
        print()
        
        start_streamlit()
        
    except Exception as e:
        print()
        print(f"發生錯誤: {e}")
        import traceback
        traceback.print_exc()
        input("按Enter鍵退出...")

if __name__ == "__main__":
    main()
