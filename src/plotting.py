import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# create plotly figure from data = (name, pd.Dataframe)
def create_figure(fig, data, mode):
    for d in data:
        name, df = d
        series = go.Scatter(x=df["x"], y=df["y"], name=name, mode=mode)
        fig.add_trace(series)
    return fig

# dataframe as list
def create_list(data):
    df = pd.DataFrame.from_dict(data, orient="index", columns=[""])
    st.table(df)

def candelstick(df):
    fig = go.Figure(data=[go.Candlestick(
        x=df.index,
        open=df["Open"],
        high=df["High"],
        low=df["Low"],
        close=df["Close"]
    )])
    fig.update_layout(xaxis_rangeslider_visible=False)
    st.plotly_chart(fig, use_container_width=True)

# data frame as table, the header is hidden for lists so add it back manually
def create_table(data, header=True):
    if header:
        df = pd.DataFrame.from_dict(data)

        # copy the column names into the first row
        df.loc[-1] = df.columns
        df.index = df.index + 1
        df = df.sort_index()

        # set the first colum to the index, then drop the row itself
        df.set_index(df.iloc[:,0], inplace=True)
        df.drop(df.columns[0], axis=1, inplace=True)
        
        st.table(df)
    else:
        st.table(data)

# parse the chart section
def parse_charts(data):
    charts = data["Charts"]
    orders = data["Orders"]

    for chart_name, chart in charts.items():
        series = chart["Series"]
        if series is None:
            continue

        data = []

        for series_name, serie in series.items():
            df = pd.DataFrame.from_dict(serie["Values"])

            try:
                df["x"] = pd.to_datetime(df["x"], unit="s")
                data.append((series_name, df))
            except KeyError as e:
                st.write(f"ERROR: {e}")
                continue
        fig = go.Figure()
        create_figure(fig, data, "lines")

        expander = st.beta_expander(chart_name)
        with expander: 
            st.plotly_chart(fig, use_container_width=True)

# parse TotalPerformance section
def parse_total_performance(data):

    total_performance = data["TotalPerformance"]
    expander = st.beta_expander("Total Performance")

    with expander:
        col1, col2 = st.beta_columns(2)

        with col1:
            st.subheader("Trade Statistics")
            create_list(total_performance["TradeStatistics"])
        with col2:
            st.subheader("Portfolio Statistics")
            create_list(total_performance["PortfolioStatistics"])

        st.subheader("Closed Trades")
        trades = total_performance["ClosedTrades"]
        for i, trade in enumerate(trades):
            trades[i]["Symbol"] = trade["Symbol"]["Value"]
        create_table(trades)

# parse the last 2 Statistics sections
def parse_statistics(data):

    expander = st.beta_expander("Statistics")

    with expander:
        col1, col2 = st.beta_columns(2)

        with col1:
            st.subheader("Statistics")
            create_list(data["Statistics"])
        with col2:
            st.subheader("Runtime Statistics")
            create_list(data["RuntimeStatistics"])
        
        