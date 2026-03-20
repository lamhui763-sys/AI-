@echo off
echo ====================================
echo AI Investment Tool Launcher
echo ====================================
echo.

echo Checking Python...
python --version
if %errorlevel% neq 0 (
    echo ERROR: Python not found!
    pause
    exit /b 1
)

echo.
echo Installing dependencies...
python -m pip install streamlit yfinance pandas plotly openpyxl --quiet

echo.
echo Starting Web Dashboard...
echo.
echo The dashboard will open in your browser at:
echo http://localhost:8501
echo.
echo Press Ctrl+C to stop the server
echo ====================================
echo.

python -m streamlit run src/ai_inv/web_dashboard.py

pause
