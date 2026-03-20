print("Python is working!")
try:
    import streamlit
    print(f"Streamlit version: {streamlit.__version__}")
except ImportError:
    print("Streamlit not installed")

try:
    import yfinance
    print(f"yfinance version: {yfinance.__version__}")
except ImportError:
    print("yfinance not installed")

try:
    import pandas
    print(f"pandas version: {pandas.__version__}")
except ImportError:
    print("pandas not installed")
