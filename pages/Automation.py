# pages/Automation.py

import streamlit as st

from src.automation.automation_logic import load_automation_data, generate_ydata_profile_object
from src.automation.ui_elements import display_go_back_button
from streamlit_pandas_profiling import st_profile_report
from pygwalker.api.streamlit import StreamlitRenderer

st.set_page_config(layout="wide", page_title="Automated EDA")
st.title("🤖 Automated Analysis Tools")

if 'automation_tool' not in st.session_state:
    st.session_state.automation_tool = None

if st.session_state.automation_tool is None:
    st.info("Choose an analysis tool to get started.")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Generate Comprehensive Data Profile (YData)", use_container_width=True):
            st.session_state.automation_tool = 'YData'
            st.rerun()
    with col2:
        if st.button("Launch Interactive Exploration (PyGWalker)", use_container_width=True):
            st.session_state.automation_tool = 'PyGWalker'
            st.rerun()
else:
    display_go_back_button()
    st.divider()
    
    df = load_automation_data()

    if not df.empty:
        if st.session_state.automation_tool == 'YData':
            st.header("📊 YData Profiling Report")
            # --- هذا هو التعديل: نعرض الرسالة هنا ---
            st.info("Generating YData Profile... The result will be cached for this session.", icon="⚙️")
            profile = generate_ydata_profile_object(df)
            st_profile_report(profile, navbar=True)

        elif st.session_state.automation_tool == 'PyGWalker':
            st.header("🔍 PyGWalker Interactive UI")
            renderer = StreamlitRenderer(df, spec="./pygwalker_spec.json", dark='dark')
            renderer.explorer()
    else:
        st.warning("Could not load data for analysis.")