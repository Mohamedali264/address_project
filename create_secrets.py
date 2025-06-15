# create_secrets.py
import os

# ----------------------------------------------------
# -- قم بملء بياناتك الحقيقية هنا في هذه المتغيرات --
# ----------------------------------------------------
NEON_DB_URL = "postgresql://neondb_owner:npg_UyAYQdV21CkN@ep-round-darkness-a85td7ux-pooler.eastus2.azure.neon.tech/neondb?sslmode=require"
PANDASAI_API_KEY = "PAI-c692f014-a1b6-4596-9b5e-d0f7fcd907eb"
GOOGLE_API_KEY = "AIzaSyAEVFhQeh8lrwr5O_MmLpaTSqCTLUeEWrU"
# ----------------------------------------------------


# هذا الكود سيقوم بإنشاء الملف بالمحتوى الصحيح
secrets_content = f"""
[connections.postgresql]
url = "{NEON_DB_URL}"

[api_keys]
pandasai_api_key = "{PANDASAI_API_KEY}"
google_api_key = "{GOOGLE_API_KEY}"
"""

# التأكد من وجود مجلد .streamlit
if not os.path.exists(".streamlit"):
    os.makedirs(".streamlit")

# كتابة الملف بالترميز الصحيح
try:
    with open(".streamlit/secrets.toml", "w", encoding="utf-8") as f:
        f.write(secrets_content.strip())
    print("\n✅ File 'secrets.toml' created successfully in '.streamlit' folder!")
    print("You can now run the main app.\n")
except Exception as e:
    print(f"\n❌ An error occurred: {e}")