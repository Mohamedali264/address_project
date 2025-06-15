# app.py

import streamlit as st
import os
import base64
from sqlalchemy import text # نستدعي "text" من SQLAlchemy

# --- استدعاء الدوال اللازمة ---
try:
    from src.data.database import get_db_connection
except ImportError:
    # هذا سيحدث مرة واحدة فقط قبل إنشاء الصفحات الأخرى
    pass

# --- إعدادات الصفحة ---
st.set_page_config(
    layout="wide", 
    page_title="Real Estate Dashboard",
    page_icon="🏠"
)

# --- تحميل ملف CSS (إذا كان موجودًا) ---
def load_css(file_path):
    """A function to load a local CSS file."""
    if os.path.exists(file_path):
        with open(file_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css("assets/style.css")

# --- قسم الترحيب والشرح ---
st.title("Welcome to the AI-Powered Dashboard")
st.info("Please select a page from the sidebar to get started.")
st.markdown("---")

st.header("📋 Application Pages")
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("🏠 Home")
    st.write("The main dashboard displaying your key performance indicators (KPIs) and summary charts of your business performance.")

with col2:
    st.subheader("🤖 Automation")
    st.write("Automated Exploratory Data Analysis (EDA) tools like YData Profiling and PyGWalker for deep data insights.")

with col3:
    st.subheader("💬 Chatbot")
    st.write("An AI-powered assistant to ask questions about your data in natural language and get answers and SQL queries.")

st.divider()

# --- قسم فحص حالة النظام ---
with st.expander("Show System & Connection Status", expanded=True):
    st.write("**Checking system components...**")
    
    # 1. فحص الاتصال بقاعدة البيانات
    try:
        engine = get_db_connection()
        if engine is not None:
            with engine.connect() as connection:
                # --- هذا هو السطر الذي تم تصحيحه ---
                connection.execute(text("SELECT 1"))
            st.success("✅ Database Connection: OK")
        else:
            st.error("❌ Database Connection: Failed to create engine.")
    except Exception as e:
        st.error(f"❌ Database Connection: Failed. Error: {e}")

    # 2. فحص مفتاح PandasAI
    if st.secrets.get("api_keys", {}).get("pandasai_api_key", "").startswith("PAI-"):
        st.success("✅ PandasAI API Key: Found and format is correct.")
    else:
        st.warning("⚠️ PandasAI API Key: Not found or invalid format in secrets.toml.")
        
    # 3. فحص إيميل Vanna
    if st.secrets.get("api_keys", {}).get("vanna_email"):
        st.success("✅ Vanna User Email: Found.")
    else:
        st.warning("⚠️ Vanna User Email: Not found in secrets.toml.")