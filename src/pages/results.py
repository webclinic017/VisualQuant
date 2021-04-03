import streamlit as st
import json
import os
import configuration
import pandas as pd

def parse_charts(data):
    charts = data["Charts"]
    for name, chart in charts.items():
        series = chart["Series"]
        if series is None:
            continue
        
        for n, s in series.items():
            df = pd.DataFrame.from_dict(s["Values"])

            try:
                df["x"] = pd.to_datetime(df["x"], unit="s")
                df = df.set_index("x")
            except KeyError as e:
                st.write(f"ERROR: {e}")
                continue

            st.write(n)
            print(df)
            st.line_chart(df)

def parse_result(data):
    parse_charts(data)

def app():
    st.title("Results")

    lean_location = configuration.get_value("path")
    path = os.path.join(lean_location, "Results")
    files = [f for f in os.listdir(path) 
         if os.path.isfile(os.path.join(path, f))]

    file_name = st.selectbox("Result file", files)
    with open(os.path.join(path, file_name), "r") as f:
        try:
            data = json.load(f)
        except:
            st.write("Invalid json file")
            return

    parse_result(data)
