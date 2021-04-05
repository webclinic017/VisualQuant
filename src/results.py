import streamlit as st
import json
import os
import configuration
import pandas as pd

import plotting

def parse_result(path, name):
    file_path = os.path.join(path, f"{name}.json")

    # load the file
    with open(os.path.join(file_path), "r") as f:
        try:
            result_data = json.load(f)
        except:
            st.warning("Invalid json file")
            return

    # build the result page
    plotting.parse_charts(result_data)
    plotting.parse_total_performance(result_data)
    plotting.parse_statistics(result_data)

def app():
    st.title("Results")

    # each folder in Results is an option to select
    lean_location = configuration.get_value("path")
    result_path = os.path.join(lean_location, "Results")
    options = [d for d in os.listdir(result_path) if os.path.isdir(os.path.join(result_path, d))]

    algo_name = st.selectbox("", options)
    parse_result(os.path.join(result_path, algo_name), algo_name)
