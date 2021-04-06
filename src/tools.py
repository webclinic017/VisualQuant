import streamlit as st
from datetime import datetime

import dataprovider

resolution_options = ["Tick", "Secound", "Minute", "Hour", "Daily"]
data_providers = list(dataprovider.providers.keys())

# state = session.get(date_range=50)

def app():
    st.title("Tools")

    st.header("Time Series Data")

    ticker = st.text_input("Ticker")
    provider = st.selectbox("Data Provider", data_providers)

    resolution = st.selectbox("Resolution", resolution_options, index=2)

    use_max = st.checkbox("Download all avilable", value=True)

    if not use_max:
        col1, col2 = st.beta_columns(2)
        with col1:
            start_date = st.date_input("Starting Date", value=datetime(2010, 1, 1))
        with col2:
            end_date = st.date_input("End Date", value=datetime.today())
    else:
        start_date = None
        end_date = None

    if st.button("Download data"):
        if ticker is "":
            st.error("Enter a ticker symbol")
            return
        dataprovider.download(provider, ticker, start_date, end_date, resolution, use_max)