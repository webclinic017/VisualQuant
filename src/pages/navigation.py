import streamlit as st

import configuration, execute, results, tools

pages = {
    "Execute": execute,
    "Results": results,
    "Tools": tools,
    "Configuration": configuration,
}

# simple selection to call the coresponding file for each page
def app():
    st.sidebar.title('Navigation')

    selection = st.sidebar.radio("", list(pages.keys()))
    page = pages[selection]
    page.app()

app()
    
