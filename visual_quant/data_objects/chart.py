import logging
import pandas as pd
import json

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go

from visual_quant.data_objects.series import Series, to_unit


class Chart:
    name = ""

    def __init__(self, app, name):
        self.logger = logging.getLogger(__name__)
        self.name = name
        self.series = {}

        app.callback(Output(f"{self.name}-graph", "figure"), [Input(f"{self.name}-dropdown", "value")])(self.create_figures)

        self.layout = {
            "paper_bgcolor": 'rgba(0, 0, 0, 0)',
            "plot_bgcolor": 'rgba(0, 0, 0, 0)',
            "font.color": 'rgba(255, 255, 255, 255)',
            "title.text": self.name
        }

    # constructors

    # TODO add type hints
    @classmethod
    def from_series(cls, app, name: str, series):
        obj = cls(app, name)
        for s in series:
            obj.add_series(s)
        return obj

    @classmethod
    def from_json(cls, app, chart_json: dict):
        logger = logging.getLogger(__name__)
        name = chart_json["Name"]

        series_json = chart_json["Series"]

        series = []
        for s in series_json:
            s = series_json[s]
            if Series.from_json(s) is not None:
                series.append(Series.from_json(s))

        return cls.from_series(app, name, series)

    # internals

    def __str__(self):
        data_frames = ""
        for s in self.series:
            data_frames += str(self.series[s])
        return f"Chart: {self.name}\n{data_frames}"

    # methods

    def add_series(self, series):
        if series.name in self.series:
            self.logger.warning(f"The series named {series.name} already exists in the chart {self.name}")
        self.series[series.name] = series

    def get_options(self):
        options = []
        for s in self.series:
            options.append({"label": s, "value": s})
        return options

    def create_figures(self, names: list, x="x", y="y"):
        fig = go.Figure(layout=self.layout)
        for name in names:
            s = self.series[name]
            fig.add_trace(s.get_figure())

        return fig

    def get_div(self):
        drop_down = dcc.Dropdown(id=f"{self.name}-dropdown", options=self.get_options(), value=list(self.series), multi=True)
        graph = dcc.Graph(id=f"{self.name}-graph")
        return html.Div(children=[drop_down, graph])