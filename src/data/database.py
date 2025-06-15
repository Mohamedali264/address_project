# src/data/database.py

import streamlit as st
import sqlalchemy
from urllib.parse import urlparse

@st.cache_resource(show_spinner="Connecting to the database...")
def get_db_connection():
    """
    Establishes a connection to the PostgreSQL database using Streamlit's secrets.
    Returns the SQLAlchemy engine object.
    Uses st.cache_resource to only connect once.
    """
    try:
        # st.connection automatically reads from secrets.toml
        conn = st.connection("postgresql", type="sql")
        # Vanna needs the underlying SQLAlchemy engine
        return conn.engine
    except Exception as e:
        st.error(f"Could not connect to database. Please check your secrets.toml file. Error: {e}")
        return None