import streamlit as st
from PIL import Image
import os

def display_image_inside_app(image_path: str):
    """
    Display a saved image inside the Streamlit app.
    """
    if not image_path or not os.path.exists(image_path):
        st.warning("⚠️ Chart image not found.")
        return

    try:
        img = Image.open(image_path)
        st.image(img, caption="📈 Chart", use_column_width=True)
    except Exception as e:
        st.error("❌ Failed to display the image.")
        st.exception(e)
