import streamlit as st
import datetime
import requests
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
import os

import plotting
import settings

def format_date(date):
    return f"{date.year:04d}-{date.month:02d}-{date.day:02d}"

# add hour/daily price series data to the lean engine
def lowres_series_import(ticker, resolution, asset_type, region, df: pd.DataFrame):
    # reorder the columns
    try:
        tmp = (df[["Open", "High", "Low", "Close"]] * 10000).astype(int)
        df = tmp.join(df["Volume"].astype(int))
    except:
        st.error("Data does not have the required columns")
        return

    ticker = ticker.lower()
    compression_opts = dict(method='zip', archive_name=f'{ticker}.csv')

    path = os.path.join(settings.get_value("path"), f"Data/{asset_type}/{region}/{resolution}/{ticker}.zip")
    df.to_csv(path, header=False, date_format="%Y%m%d %H:%M", compression=compression_opts)
    st.success(f"Data written to {path}")

def binance():
    pass

def yahoo(ticker: str, start_date, end_date, resolution, use_max):
    
    try:
        ticker_obj = yf.Ticker(ticker)
        if use_max:
            df = ticker_obj.history(period="max")
            print(df)
        else:
            df = ticker_obj.history(start=start_date, end=end_date)
        df.dropna(inplace=True)
    except:
        st.error("Couldn't retrive data from YAHOO api")
        return
    
    st.success(f"Downloaded data from {df.index[0]} to {df.index[-1]}")
    lowres_series_import(ticker, "daily", "equity", "usa", df)

providers = {
    "YAHOO": yahoo,
    "BINANCE": binance
}

def download(provider: str, ticker: str, start_date, end_date, resolution, use_max):
    function = providers[provider]
    function(ticker, start_date, end_date, resolution, use_max)
    
