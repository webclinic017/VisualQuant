import streamlit as st

import settings, execute, results, tools

import ui_util

pages = {
    "Execute": execute,
    "Results": results,
    "Tools": tools,
    "Settings": settings,
}

# simple selection to call the coresponding file for each page
def app():
    st.sidebar.title('Navigation')

    selection = st.sidebar.radio("", list(pages.keys()))
    page = pages[selection]
    page.app()

# configure page looks
ui_util.init_config()
ui_util.load_css()

app()
    
