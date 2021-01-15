import dash
import dash_html_components as html
import dash_core_components as dcc
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output
import plotly.graph_objects as go

from visual_quant.app import app

import visual_quant.parser.result_parser as result_parser

chart = result_parser.get_chart("data/results.json", "Average Cross")
print(chart)


app.layout = html.Div(children=chart.get_div())

if __name__ == "__main__":
    app.run_server(debug=True)
