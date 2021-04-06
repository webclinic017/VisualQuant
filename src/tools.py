import streamlit as st
from datetime import datetime

import dataprovider

resolution_options = ["Tick", "Secound", "Minute", "Hour", "Daily"]
data_providers = ["NASDAQ"]

# state = session.get(date_range=50)

def app():
    st.title("Tools")

    st.header("Data")


    ticker = st.text_input("Ticker")
    resolution = st.selectbox("Resolution", resolution_options, index=2)

    col1, col2 = st.beta_columns(2)
    with col1:
        start_date = st.date_input("Starting Date", value=datetime(2010, 1, 1))
    with col2:
        end_date = st.date_input("End Date", value=datetime.today())

    provider = st.selectbox("Data Provider", data_providers)

    if st.button("Download data"):
        dataprovider.download(provider, ticker, start_date, end_date, resolution)