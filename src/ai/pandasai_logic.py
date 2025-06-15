import streamlit as st
import pandas as pd
import pandasai as pai
from pandasai.smart_dataframe import SmartDataframe
import os
import glob

def setup_pandasai_platform() -> bool:
    """
    Sets the API key for the PandasAI platform.
    """
    api_key = st.secrets.get("api_keys", {}).get("pandasai_api_key")
    if not api_key:
        st.error("❌ PandasAI platform API key (PAI-...) not found in secrets.toml.")
        return False
    
    try:
        pai.api_key.set(api_key)
        return True
    except Exception as e:
        st.error(f"❌ Failed to set PandasAI API key: {e}")
        return False


def generate_chart_from_df_platform(df: pd.DataFrame) -> str:
    """
    Generates a chart from the dataframe using PandasAI Platform and returns the chart file path.
    """
    if df.empty:
        return None

    temp_chart_dir = "temp_charts"
    os.makedirs(temp_chart_dir, exist_ok=True)

    try:
        smart_df = SmartDataframe(
            df,
            config={
                "save_charts": True,
                "save_charts_path": temp_chart_dir,
                "verbose": True
            }
        )

        # ✅ Trigger chart generation
        response = smart_df.chat("Generate the most suitable chart to visualize this data.")

        # ✅ Get latest saved chart image
        chart_files = glob.glob(os.path.join(temp_chart_dir, "*.png"))
        if chart_files:
            latest_chart = max(chart_files, key=os.path.getctime)
            return os.path.abspath(latest_chart)

        # No chart was created
        st.info("ℹ️ PandasAI returned a text response instead of a chart.")
        st.info(response)
        return None

    except Exception as e:
        st.error(f"❌ Error during PandasAI chart generation: {e}")
        return None
