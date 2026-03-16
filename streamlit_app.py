import sys
import os
import streamlit as st

# 設置頁面配置
st.set_page_config(page_title="AI 投資工具啟動器", layout="wide")

# 將專案路徑添加到 Python 路徑中
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.join(current_dir, "ai-invest-tool")
src_path = os.path.join(project_root, "src")

if project_root not in sys.path:
    sys.path.insert(0, project_root)
if src_path not in sys.path:
    sys.path.insert(0, src_path)

# 嘗試導入並運行主儀表板
try:
    from src.ai_inv.web_dashboard import main
    if __name__ == "__main__":
        main()
except ImportError as e:
    st.error(f"❌ 模組導入失敗: {e}")
    st.info("💡 這通常是因為 Streamlit Cloud 還在安裝依賴項，或者 requirements.txt 尚未生效。")
    st.write("### 當前環境診斷：")
    st.write(f"- **Python 版本**: {sys.version}")
    st.write(f"- **專案目錄是否存在**: {os.path.exists(project_root)}")
except Exception as e:
    st.error(f"❌ 運行時出錯: {e}")
    st.exception(e)
