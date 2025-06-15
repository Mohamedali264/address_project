import streamlit as st
import pandas as pd
import os
from PIL import Image

from src.ai.deepseek_logic import generate_sql
from src.ai.vanna_logic import setup_db_agent
from src.ai.pandasai_logic import (
    setup_pandasai_platform,
    generate_chart_from_df_platform
)
from src.ai.image_display import display_image_inside_app  # ✅ استدعاء الدالة الجديدة

st.set_page_config(page_title="🤖 Chatbot", layout="wide")
st.title("💬 AI Chatbot")

# ✅ إعداد الاتصال بمنصة PandasAI
pandasai_ready = setup_pandasai_platform()

# ✅ المستخدم يكتب السؤال
question = st.text_input("Ask your question about the deals report:")

if question:
    with st.spinner("🤖 Generating SQL..."):
        sql = generate_sql(question)

    if sql:
        st.subheader("🧠 Generated SQL:")
        st.code(sql, language="sql")

        agent = setup_db_agent()

        with st.spinner("📊 Running SQL..."):
            try:
                df = agent.run_sql(sql)

                if not df.empty:
                    st.subheader("📈 Query Results:")
                    st.dataframe(df, use_container_width=True)

                    # ✅ تحليل الرسم فقط لو PandasAI جاهز
                    if pandasai_ready:
                        with st.expander("📊 Generate Suggested Chart"):
                            with st.spinner("Generating chart..."):
                                chart_path = generate_chart_from_df_platform(df)
                                if chart_path and os.path.exists(chart_path):
                                    display_image_inside_app(chart_path)  # ✅ عرض الصورة داخل الموقع
                                else:
                                    st.warning("⚠️ No chart was generated.")
                else:
                    st.warning("✅ Query ran, but no results found.")

            except Exception as e:
                st.error("❌ Failed to run SQL.")
                st.exception(e)
