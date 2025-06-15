from vanna.remote import VannaDefault
from urllib.parse import urlparse
import streamlit as st

@st.cache_resource(show_spinner="📦 Connecting to DB...")
def setup_db_agent():
    db_url = st.secrets["connections"]["postgresql"]["url"]
    parsed = urlparse(db_url)

    agent = VannaDefault(model="dummy@email.com", api_key="vn-fake-key")

    agent.connect_to_postgres(
        host=parsed.hostname,
        dbname=parsed.path.lstrip("/"),
        user=parsed.username,
        password=parsed.password,
        port=parsed.port or 5432
    )
    return agent
