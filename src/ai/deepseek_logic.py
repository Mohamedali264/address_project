from openai import OpenAI
import streamlit as st
import re

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=st.secrets["api_keys"]["openrouter_api_key"]
)

def generate_sql(question: str) -> str:
    ddl = """
    Table name: deals_report

    Columns:
    - number_deal: INTEGER 
    - deal_id_no: INTEGER
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
    - sales_agent_name: VARCHAR
    - per: INTEGER
    - team_leader_name: VARCHAR
    - per2: INTEGER
    - sales_manager_name: VARCHAR
    - per3: INTEGER
    - sales_director_name: VARCHAR
    - per4: INTEGER
    - head_of_sales: VARCHAR
    - per5: INTEGER
    - outside_broker_name: VARCHAR
    - perc: INTEGER
	- Commission: VARCHAR
	- paid: VARCHAR
    - notes: VARCHAR 
    """

    prompt = f"""
You are a data analyst. Translate this question into a valid SQL query based on this schema:

{ddl}

Question: {question}

SQL:
"""

    try:
        response = client.chat.completions.create(
            model="deepseek/deepseek-r1-0528:free",
            messages=[
                {"role": "system", "content": "You are a helpful SQL assistant."},
                {"role": "user", "content": prompt}
            ],
            extra_headers={
                "HTTP-Referer": "http://localhost:8501",
                "X-Title": "real-estate-dashboard"
            }
        )

        content = response.choices[0].message.content.strip()

        match = re.search(r"```(?:sql)?\s*([\s\S]+?)\s*```", content)
        if match:
            return match.group(1).strip()

        # fallback
        lines = content.splitlines()
        sql_lines = [line for line in lines if "SELECT" in line.upper()]
        if sql_lines:
            return "\n".join(sql_lines).strip()

        return ""

    except Exception as e:
        st.error("❌ Failed to generate SQL from DeepSeek.")
        st.exception(e)
        return ""
