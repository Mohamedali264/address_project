# src/components/ui_elements.py

import streamlit as st
from src.automation.automation_logic import load_automation_data, generate_ydata_profile_object

def display_go_back_button():
    """Displays a button that resets the tool choice and clears ALL relevant caches."""
    if st.button("⬅️ Go Back to Tool Selection"):
        st.session_state.automation_tool = None
        # --- هذا هو التعديل: مسح كل أنواع الكاش ---
        load_automation_data.clear()
        generate_ydata_profile_object.clear()
        st.rerun()