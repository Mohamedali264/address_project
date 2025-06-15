import streamlit as st
from openai import OpenAI
import requests

# إعداد الـ client الخاص بـ OpenRouter
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=st.secrets["api_keys"]["openrouter_api_key"]
)

# تعريف شكل جدول البيانات
DDL_SCHEMA = """
Table name: deals_report

Columns:
- number_deal: INTEGER
- deal_id_no: VARCHAR
- deal_status: VARCHAR
- collected: VARCHAR
- selling_type: VARCHAR
- reservation_date: DATE
- contract_date: DATE
- client_name: VARCHAR
- client_mobile_number: VARCHAR
- source_of_lead: VARCHAR
- developer: VARCHAR
- project: VARCHAR
- unit: VARCHAR
- unit_type: VARCHAR
- unit_price: INTEGER
- sales_person_name: VARCHAR
- team_leader_name: VARCHAR
- sales_manager_name: VARCHAR
- sales_director: VARCHAR
- outside_broker_name: VARCHAR
- perc_commission: VARCHAR
- commission: NUMERIC
- paid: NUMERIC
- notes: TEXT
"""

def generate_sql_with_openrouter(question: str) -> str:
    prompt = f"""
You are a data analyst assistant. Given the following table schema:

{DDL_SCHEMA}

Translate the following question into a valid SQL query:

Question: {question}
SQL:
"""

    try:
        completion = client.chat.completions.create(
            model="deepseek/deepseek-r1-0528:free",
            messages=[
                {"role": "system", "content": "You are a helpful SQL assistant."},
                {"role": "user", "content": prompt}
            ],
            extra_headers={
                "HTTP-Referer": "http://localhost:8501",  # اختياري
                "X-Title": "address-dashboard"
            }
        )
        return completion.choices[0].message.content.strip()
    except Exception as e:
        st.error("❌ Failed to generate SQL with OpenRouter.")
        st.exception(e)
        return ""

# واجهة Streamlit
st.title("🧠 DeepSeek via OpenRouter – SQL Generator")

question = st.text_input("Ask a question about your deals report:")

if question:
    sql = generate_sql_with_openrouter(question)
    if sql:
        st.code(sql, language="sql")
