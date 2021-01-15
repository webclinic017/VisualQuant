import logging
import pandas as pd

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from visual_quant.app import app


class Chart:
    name = ""
    series = {}

    def __init__(self):
        self.logger = logging.getLogger(__name__)

        app.callback(Output("graph", "figure"), [Input("dropdown", "value")])(self.update_graph)

    # TODO add type hints
    @classmethod
    def from_series(cls, name: str, series):
        obj = cls()
        obj.name = name
        for s in series:
            obj.add_series(s)
        return obj

    def __str__(self):
        data_frames = ""
        for s in self.series:
            data_frames += str(self.series[s])
        return f"Chart: {self.name}\n{data_frames}"

    def add_series(self, series):
        if series.name in self.series:
            self.logger.warning(f"The series named {series.name} already exists in the chart {self.name}")
        self.series[series.name] = series

    def get_options(self):
        options = []
        for s in self.series:
            options.append({"label": s, "value": s})

    def get_div(self):
        drop_down = dcc.Dropdown(id="dropdown", options=self.get_options(), multi=True)
        graph = dcc.Graph(id="graph")
        return html.Div(children=[drop_down, graph])

    def update_graph(self, values):
        figure = {"data": self.series["FastMA"].values}
        print("call back")
        return figure
