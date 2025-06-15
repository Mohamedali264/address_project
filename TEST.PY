#                 #     CREATE TABLE deals_report (
#                 #         number_deal INTEGER PRIMARY KEY,
#                 #         deal_id_no VARCHAR(255),
#                 #         deal_status VARCHAR(50),
#                 #         collected VARCHAR(255),
#                 #         selling_type VARCHAR(255),
#                 #         reservation_date DATE,
#                 #         contract_date DATE,
#                 #         client_name VARCHAR(255),
#                 #         client_mobile_number VARCHAR(50),
#                 #         source_of_lead VARCHAR(255),
#                 #         developer VARCHAR(255),
#                 #         project VARCHAR(255),
#                 #         unit VARCHAR(100),
#                 #         unit_type VARCHAR(100),
#                 #         unit_price INTEGER,
#                 #         sales_person_name VARCHAR(255),
#                 #         team_leader_name VARCHAR(255),
#                 #         sales_manager_name VARCHAR(255),
#                 #         sales_director VARCHAR(255),
#                 #         outside_broker_name VARCHAR(255),
#                 #         perc_commission VARCHAR(50),
#                 #         commission NUMERIC(15, 2),
#                 #         paid NUMERIC(15, 2),
#                 #         notes TEXT
#                 #     )
#                 # """

# import streamlit as st
# import pandas as pd
# import os
# from urllib.parse import urlparse
# from vanna.chromadb import ChromaDB_VectorStore
# from vanna.google import GoogleGeminiChat

# class MyVanna(ChromaDB_VectorStore, GoogleGeminiChat):
#     def __init__(self, config=None):
#         self.chromadb_path = 'chroma_db'
#         ChromaDB_VectorStore.__init__(self, config=config)
#         gemini_api_key = st.secrets.get("api_keys", {}).get("google_api_key")
#         GoogleGeminiChat.__init__(self, config={'api_key': gemini_api_key})

# @st.cache_resource(show_spinner="Setting up Vanna AI Agent...")
# def setup_vanna_agent():
#     # ✅ تحقق من وجود secrets
#     if "connections" not in st.secrets or "postgresql" not in st.secrets["connections"]:
#         st.error("❌ Missing database connection in secrets.toml")
#         return None

#     vn_agent = MyVanna()

#     try:
#         url = urlparse(st.secrets["connections"]["postgresql"]["url"])
#         vn_agent.connect_to_postgres(
#             host=url.hostname,
#             dbname=url.path.lstrip('/'),
#             user=url.username,
#             password=url.password,
#             port=url.port or 5432  # ✅ استخدم 5432 كبورت افتراضي
#         )

#     except Exception as e:
#         st.error("❌ Database connection failed. Check your connection URL in secrets.toml.")
#         st.exception(e)
#         return None

#     try:
#         if len(vn_agent.get_training_data()) == 0 and not os.path.exists(vn_agent.chromadb_path):
#             st.info("📚 First-time setup: Training Vanna agent...")
#             with st.spinner("Training Vanna on your database schema..."):
#                 ddl_statement = """
#                     CREATE TABLE deals_report (
#                         number_deal INTEGER PRIMARY KEY,
#                         deal_id_no VARCHAR(255),
#                         deal_status VARCHAR(50),
#                         collected VARCHAR(255),
#                         selling_type VARCHAR(255),
#                         reservation_date DATE,
#                         contract_date DATE,
#                         client_name VARCHAR(255),
#                         client_mobile_number VARCHAR(50),
#                         source_of_lead VARCHAR(255),
#                         developer VARCHAR(255),
#                         project VARCHAR(255),
#                         unit VARCHAR(100),
#                         unit_type VARCHAR(100),
#                         unit_price INTEGER,
#                         sales_person_name VARCHAR(255),
#                         team_leader_name VARCHAR(255),
#                         sales_manager_name VARCHAR(255),
#                         sales_director VARCHAR(255),
#                         outside_broker_name VARCHAR(255),
#                         perc_commission VARCHAR(50),
#                         commission NUMERIC(15, 2),
#                         paid NUMERIC(15, 2),
#                         notes TEXT
#                     )
#                 """
#                 vn_agent.train(ddl=ddl_statement)
#                 st.success("✅ Vanna agent trained successfully!")
#         else:
#             st.success("✅ Vanna agent is ready!")
#     except Exception as e:
#         st.error("❌ Failed to train Vanna agent.")
#         st.exception(e)
#         return None

#     return vn_agent

# def get_sql_from_question(agent, question: str) -> str:
#     if agent:
#         return agent.generate_sql(question=question)
#     return ""

# def get_dataframe_from_sql(agent, sql: str) -> pd.DataFrame:
#     if agent and sql:
#         try:
#             return agent.run_sql(sql=sql)
#         except Exception as e:
#             st.error(f"❌ Error executing SQL: {e}")
#             return pd.DataFrame()
#     return pd.DataFrame()


# #---------------------------local-------------------------

# # import streamlit as st
# # import pandas as pd
# # from vanna.remote import VannaDefault

# # class MyVanna(VannaDefault):
# #     def __init__(self):
# #         email = st.secrets["api_keys"]["vanna_email"]
# #         api_key = st.secrets["api_keys"]["vanna_api_key"]
# #         super().__init__(model=email, api_key=api_key)

# #         # ✅ الاتصال بقاعدة البيانات SQLite من Google Drive مباشرة
# #         self.connect_to_sqlite("https://drive.google.com/uc?export=download&id=1hKG6EzxzHGtcGoT3a6SYf3-nOTE241fy")


# # @st.cache_resource(show_spinner="🔄 Setting up Vanna Cloud Agent...")
# # def setup_vanna_agent():
# #     try:
# #         vn_agent = MyVanna()
# #         st.success("✅ Vanna Cloud agent ready!")
# #         return vn_agent

# #     except Exception as e:
# #         st.error("❌ Failed to set up Vanna agent.")
# #         st.exception(e)
# #         return None


# # def get_sql_from_question(agent, question: str) -> str:
# #     if agent:
# #         try:
# #             prompt = f"""
# # You are an expert SQL generator.
# # Assume a table called deals_report with the following columns:

# # - number_deal (integer)
# # - deal_id_no (text)
# # - deal_status (text)
# # - collected (text)
# # - selling_type (text)
# # - reservation_date (date)
# # - contract_date (date)
# # - client_name (text)
# # - client_mobile_number (text)
# # - source_of_lead (text)
# # - developer (text)
# # - project (text)
# # - unit (text)
# # - unit_type (text)
# # - unit_price (integer)
# # - sales_person_name (text)
# # - team_leader_name (text)
# # - sales_manager_name (text)
# # - sales_director (text)
# # - outside_broker_name (text)
# # - perc_commission (text)

# # Generate an SQL query to answer: {question}
# # """
# #             sql_tuple = agent.ask(prompt)
# #             if not sql_tuple or not sql_tuple[0]:
# #                 st.error("❌ The agent did not return a valid SQL string.")
# #                 st.write("🧪 Raw agent.ask() response:", sql_tuple)
# #                 return ""
# #             sql = sql_tuple[0].strip()
# #             return sql

# #             # ✅ استخدم ask بدل llm
# #         except Exception as e:
# #             st.error("❌ Failed to generate SQL.")
# #             st.exception(e)
# #     return ""


# # def get_dataframe_from_sql(agent, sql: str) -> pd.DataFrame:
# #     if agent and sql:
# #         try:
# #             return agent.run_sql(sql=sql)
# #         except Exception as e:
# #             st.error("❌ Error executing SQL.")
# #             st.exception(e)
# #     return pd.DataFrame()





