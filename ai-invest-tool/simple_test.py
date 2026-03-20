import sys
print("Python is working!")
print(f"Python version: {sys.version}")

try:
    import streamlit
    print(f"Streamlit version: {streamlit.__version__}")
    print("Streamlit is installed!")
except ImportError:
    print("Streamlit is NOT installed")
    print("Please run: pip install streamlit")
