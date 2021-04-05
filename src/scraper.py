import streamlit as st
import datetime
import requests

from bandl.nasdaq import Nasdaq
import plotly.graph_objects as go

import plotting

def format_date(date):
    return f"{date.year:04d}-{date.month:02d}-{date.day:02d}"

def nasdaq_download(ticker, start_date, end_date):
    
    nasdaq = Nasdaq()
    df = nasdaq.get_data("aapl", periods=15)

    # this evil motherfucker has trailing spaces in the columns names
    df.rename(columns=str.strip, inplace=True)
    df.rename(columns={"Close/Last": "Close"}, inplace=True)

    for c in df.columns:
        try:
            df[c] = df[c].str.replace("$", "").astype(float)
        except:
            pass

    plotting.candelstick(df)
    
