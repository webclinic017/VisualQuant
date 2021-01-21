import logging
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import dash
import dash_html_components as html

from visual_quant.components.series import Series
from visual_quant.components.component import Component


# provides a interactive chart using the dash graph and dropdown
# can hold multiple series
class Chart(Component):

    # constructors

    def __init__(self, app, name):
        super().__init__(app, name)
        self.series = {}

    # constructor for directly adding series to the chart
    @classmethod
    def from_series(cls, app: dash.Dash, name: str, series: list):
        obj = cls(app, name)
        for s in series:
            obj.add_series(s)
        return obj

    # load the chart from a json dict
    @classmethod
    def from_json(cls, app: dash.Dash, chart_json: dict):
        logger = logging.getLogger(__name__)

        try:
            name = chart_json["Name"]
            series_json = chart_json["Series"]
        except KeyError as e:
            logger.error(f"Trying to load chart from json dict that has no name or series field\n{e}")
            return None

        # add the all series in the chart
        series = []
        for s in series_json:
            s = series_json[s]
            if Series.from_json(app, s) is not None:
                series.append(Series.from_json(app, s))

        return cls.from_series(app, name, series)

    # magic

    def __str__(self):
        # nice way to print chart information
        data_frames = ""
        for s in self.series:
            data_frames += str(self.series[s])
        return f"Chart: {self.name}\n{data_frames}"

    # properties

    @property
    def layout(self):
        # TODO dont hard code colors, base them on the selected theme
        layout = {
            "paper_bgcolor": "rgba(0, 0, 0, 0)",
            "plot_bgcolor": "rgba(0, 0, 0, 0)",
            "title.text": self.name,
            "title.font.color": "rgba(220, 220, 220, 255)",
            "legend.font.color": "rgba(220, 220, 220, 255)",
        }

        return layout

    # methods

    def set_callback(self):
        if len(self.series) > 0:
            self.app.callback(Output(f"{self.name}-graph", "figure"), [Input(f"{self.name}-dropdown", "value")])(self.create_figures)

    def add_series(self, series: Series):
        if series.name in self.series:
            self.logger.warning(f"The series named {series.name} already exists in the chart {self.name}")
        self.series[series.name] = series

    def join(self, other: "Chart"):
        self.series = {**self.series, **other.series}

    # get options in format for dropdown
    def get_options(self):
        options = []
        for s in self.series:
            options.append({"label": s, "value": s})
        return options

    # callback function for dropdown
    # build figure based on the values from the dropdown
    def create_figures(self, series_names: list):
        fig = go.Figure(layout=self.layout)
        for name in series_names:
            s = self.series[name]
            fig.add_trace(s.get_figure())

        return fig

    def get_html(self):
        # register the callback only when needed, so only when it is rendered to avoid errors because ids missing in app layout
        self.set_callback()

        if len(self.series) == 0:
            self.logger.warning(f"chart {self.name} does not contain any series. Won't render")
            return None

        drop_down = dcc.Dropdown(id=f"{self.name}-dropdown", options=self.get_options(), value=list(self.series), multi=True, className=f"dropdown {self.name}",
                                 style={"background-color": "rgba(0, 0, 0, 0)", "color": "rgba(30, 30, 30, 255)"})
        graph = dcc.Graph(id=f"{self.name}-graph")

        return html.Div(children=[drop_down, graph])
