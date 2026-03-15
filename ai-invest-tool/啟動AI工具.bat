@echo off 
chcp 65001 >nul 
cd /d "%~dp0" 
echo 正在啟動AI投資工具... 
start http://localhost:8501 
python -m streamlit run src/ai_inv/web_dashboard.py 
pause 
