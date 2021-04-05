import streamlit as st
from PIL import Image

style_sheet = "./resource/style.css"
icon_path = "./resource/lean.ico"

# add css
def css(css):
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

def load_css():
    with open(style_sheet, "r") as f:
        style = f.read()

    css(style)

def init_config():
    # TODO load theme
    icon = Image.open(icon_path).convert("RGBA")
    # TODO load the icon so it has an alpha channel and look good
    st.set_page_config(
        page_title="LEAN Webapp",
        layout="wide",
        initial_sidebar_state="expanded"
    )