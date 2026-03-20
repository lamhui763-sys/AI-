"""簡化版測試頁面"""

import streamlit as st

# 頁面配置
st.set_page_config(
    page_title="AI投资分析工具",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("📈 AI投资分析工具")

st.write("歡迎使用AI投资分析工具！")

st.markdown("---")

st.header("測試頁面")

st.write("如果您能看到這個頁面，說明Streamlit運行正常！")

st.success("✅ 測試成功！")

st.markdown("""
## 功能列表

1. 📊 股票分析 - 查看即時股價和交易信號
2. 🔬 技術分析 - 技術指標分析
3. 🤖 AI分析 - ChatGPT智能分析
4. ⏱️ 回測引擎 - 策略回測
5. 💼 投資組合 - 投資組合管理
6. 📰 新聞分析 - 新聞情感分析
""")

st.info("💡 如果您看到這個頁面，請點擊右上角的「X」關閉，然後重新啟動完整版應用")
