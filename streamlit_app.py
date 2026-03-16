import sys
import os

# 將專案路徑添加到 Python 路徑中
# Add project path to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.join(current_dir, "ai-invest-tool")
src_path = os.path.join(project_root, "src")

if project_root not in sys.path:
    sys.path.insert(0, project_root)
if src_path not in sys.path:
    sys.path.insert(0, src_path)

# 導入並運行主儀表板
# Import and run the main dashboard
try:
    from src.ai_inv.web_dashboard import main
    if __name__ == "__main__":
        main()
except ImportError as e:
    import streamlit as st
    st.error(f"無法加載應用程序模塊。錯誤詳情: {e}")
    st.info("請確保 GitHub 倉庫結構正確，且 ai-invest-tool 目錄存在。")
