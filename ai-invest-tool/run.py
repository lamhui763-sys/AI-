"""
AI投资工具 - 简单启动器
这个脚本会检查依赖并启动Web界面
"""

import sys
import os
import subprocess
import webbrowser
import time

def check_python():
    """检查Python版本"""
    print("=" * 60)
    print("AI投资工具 - 启动器")
    print("=" * 60)
    print()
    
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 9):
        print(f"[错误] Python版本过低: {version.major}.{version.minor}")
        print("需要Python 3.9或更高版本")
        print()
        print("请下载最新版Python: https://www.python.org/downloads/")
        return False
    
    print(f"[✓] Python版本: {version.major}.{version.minor}.{version.micro}")
    return True

def install_dependencies():
    """安装必要的依赖"""
    print()
    print("[步骤1] 安装依赖包...")
    print("-" * 60)
    
    packages = [
        "streamlit",
        "plotly",
        "openpyxl",
        "pandas",
        "numpy",
        "yfinance",
        "openai"
    ]
    
    for package in packages:
        try:
            __import__(package.replace("-", "_"))
            print(f"[✓] {package} 已安装")
        except ImportError:
            print(f"[↓] 安装 {package}...")
            try:
                subprocess.check_call([
                    sys.executable, "-m", "pip", "install", "-q", package
                ])
                print(f"[✓] {package} 安装成功")
            except subprocess.CalledProcessError:
                print(f"[✗] {package} 安装失败")
                return False
    
    return True

def start_web_dashboard():
    """启动Web仪表板"""
    print()
    print("[步骤2] 启动Web界面...")
    print("-" * 60)
    
    # 设置环境变量
    os.environ['STREAMLIT_SERVER_PORT'] = '8501'
    os.environ['STREAMLIT_SERVER_HEADLESS'] = 'true'
    
    print()
    print("=" * 60)
    print("Web界面正在启动...")
    print("=" * 60)
    print()
    print("📱 访问地址: http://localhost:8501")
    print()
    print("💡 提示:")
    print("  - 浏览器会自动打开（如果没有，请手动访问上面的地址）")
    print("  - 按 Ctrl+C 停止服务器")
    print("  - 修改代码后会自动刷新")
    print()
    print("=" * 60)
    print()
    
    # 延迟几秒后打开浏览器
    def open_browser():
        time.sleep(3)
        print("[正在打开浏览器...]")
        webbrowser.open("http://localhost:8501")
    
    # 在新线程中打开浏览器
    import threading
    browser_thread = threading.Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()
    
    # 启动Streamlit
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run",
            "src/ai_inv/web_dashboard.py"
        ])
    except KeyboardInterrupt:
        print()
        print()
        print("=" * 60)
        print("Web界面已停止")
        print("=" * 60)
    except Exception as e:
        print(f"[错误] 启动失败: {e}")
        print()
        print("请尝试手动运行:")
        print("  streamlit run src/ai_inv/web_dashboard.py")

def main():
    """主函数"""
    try:
        # 检查Python
        if not check_python():
            return
        
        # 安装依赖
        if not install_dependencies():
            print()
            print("[错误] 依赖安装失败")
            return
        
        # 启动Web界面
        start_web_dashboard()
    
    except KeyboardInterrupt:
        print()
        print()
        print("用户中断")
        return

if __name__ == "__main__":
    main()
