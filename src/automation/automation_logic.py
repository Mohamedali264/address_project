# src/automation/logic.py

import streamlit as st
import pandas as pd
from src.data.database import get_db_connection
from ydata_profiling import ProfileReport

@st.cache_data
def load_automation_data():
    """
    Loads, cleans, and preprocesses data from the database based on the LATEST schema.
    """
    try:
        engine = get_db_connection()
        if engine:
            df = pd.read_sql_table('deals_report', engine)
            
            # --- خطوة تنظيف البيانات وتوحيدها ---
            # 1. توحيد قيم عمود "deal_status"
            if 'deal_status' in df.columns:
                # إزالة المسافات وتوحيد حالة الأحرف (e.g., "cancelled" -> "Cancelled")
                df['deal_status'] = df['deal_status'].str.strip().str.title()

            # 2. تحويل كل الأعمدة الرقمية
            numeric_cols = [
                'unit_price', 
                'per', 
                'per2', 
                'per3', 
                'per4', 
                'per5', 
                'perc',
                'Commission', 
                'paid'
            ]
            for col in numeric_cols:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce')

            # 3. تحويل أعمدة التواريخ
            date_cols = ['reservation_date', 'contract_date']
            for col in date_cols:
                if col in df.columns:
                    df[col] = pd.to_datetime(df[col], errors='coerce')
            
            return df
    except Exception as e:
        st.error(f"Failed to load data: {e}")
    return pd.DataFrame()

@st.cache_data
def generate_ydata_profile_object(df):
    """
    Generates the ProfileReport object in memory.
    This function should not contain any Streamlit UI elements.
    """
    return ProfileReport(df, title="Deals Report Profile", minimal=True)