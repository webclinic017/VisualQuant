import streamlit as st
from datetime import datetime
import scraper

resolution_options = ["Tick", "Secound", "Minute", "Hour", "Daily"]

# state = session.get(date_range=50)

def app():
    st.title("Tools")

    st.header("Data Scraper")
    st.subheader("NASDAQ Data")

    ticker = st.text_input("Ticker")
    # resolution = st.selectbox("Resolution", resolution_options, index=2)

    col1, col2 = st.beta_columns(2)
    with col1:
        start_date = st.date_input("Starting Date", value=datetime(1998, 1, 1))
    with col2:
        end_date = st.date_input("End Date", value=datetime.today())

    if st.button("Download data"):
        scraper.nasdaq_download(ticker, start_date, end_date)
