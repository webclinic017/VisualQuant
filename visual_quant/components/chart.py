import logging
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import dash

from visual_quant.components.series import Series
from visual_quant.components.component import Component


class Chart(Component):

    def __init__(self, app, name, bg_color="rgba(0, 0, 0, 0)", font_color="rgba(200, 200, 200, 255)"):
        super().__init__(app, name)
        self.series = {}

        app.callback(Output(f"{self.name}-graph", "figure"), [Input(f"{self.name}-dropdown", "value")])(self.create_figures)

        self.layout = {
            "paper_bgcolor": bg_color,
            "plot_bgcolor": bg_color,
            "font.color": font_color,
            "title.text": self.name
        }

    # constructors

    @classmethod
    def from_series(cls, app: dash.Dash, name: str, series: Series):
        obj = cls(app, name)
        for s in series:
            obj.add_series(s)
        return obj

    @classmethod
    def from_json(cls, app: dash.Dash, chart_json: dict):
        logger = logging.getLogger(__name__)
        name = chart_json["Name"]

        series_json = chart_json["Series"]

        series = []
        for s in series_json:
            s = series_json[s]
            if Series.from_json(s) is not None:
                series.append(Series.from_json(s))

        return cls.from_series(app, name, series)

    # magic

    def __str__(self):
        data_frames = ""
        for s in self.series:
            data_frames += str(self.series[s])
        return f"Chart: {self.name}\n{data_frames}"

    # methods

    def add_series(self, series: Series):
        if series.name in self.series:
            self.logger.warning(f"The series named {series.name} already exists in the chart {self.name}")
        self.series[series.name] = series

    def get_options(self):
        options = []
        for s in self.series:
            options.append({"label": s, "value": s})
        return options

    # callback for dropdown
    def create_figures(self, series_names: list):
        fig = go.Figure(layout=self.layout)
        for name in series_names:
            s = self.series[name]
            fig.add_trace(s.get_figure())

        return fig

    def get_html(self):
        drop_down = dcc.Dropdown(id=f"{self.name}-dropdown", options=self.get_options(), value=list(self.series), multi=True)
        graph = dcc.Graph(id=f"{self.name}-graph")
        return html.Div(children=[drop_down, graph])