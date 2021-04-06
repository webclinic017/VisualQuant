import streamlit as st
import datetime
import requests
import pandas as pd
import bandl
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
        df = tmp.join(df["Volume"])
    except:
        st.error("Data does not have the required columns")

    compression_opts = dict(method='zip', archive_name=f'{ticker}.csv')

    path = os.path.join(settings.get_value("path"), f"Data/{asset_type}/{region}/{resolution}/{ticker}.zip")
    df.to_csv(path, header=False, date_format="%Y%m%d %H:%M", compression=compression_opts)
    st.success(f"Data written to {path}")

def binance():
    pass

def nasdaq(ticker: str, start_date, end_date, resolution):
    
    provider = bandl.nasdaq.Nasdaq()
    try:
        df = provider.get_data(ticker, start=start_date, end=end_date)
    except:
        st.error("Couldn't retrive data from NASDAQ api")
        return

    # this evil motherfucker has trailing spaces in the columns names
    df.rename(columns=str.strip, inplace=True)
    df.rename(columns={"Close/Last": "Close"}, inplace=True)

    df.index = pd.to_datetime(df.index)
    df.sort_index(inplace=True)

    for c in df.columns:
        try:
            df[c] = df[c].str.strip(" $").astype(float)
        except:
            pass
    
    st.success(f"Downloaded data from {df.index[0]} to {df.index[-1]}")
    lowres_series_import(ticker, "daily", "equity", "usa", df)


providers = {
    "NASDAQ": nasdaq,
    "BINANCE": binance
}

def download(provider: str, ticker: str, start_date, end_date, resolution):
    function = providers[provider]
    function(ticker, start_date, end_date, resolution)
    
