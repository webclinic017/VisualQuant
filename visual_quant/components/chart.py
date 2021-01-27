import logging
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import dash
import dash_bootstrap_components as dbc
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

        self.dropdown_type = "chart-dropdown"
        self.graph_type = "chart-graph"

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

    # methods

    @staticmethod
    def layout(name):
        # TODO don't hard code colors, base them on the selected theme
        layout = {
            "paper_bgcolor": "rgba(0, 0, 0, 0)",
            "plot_bgcolor": "rgba(0, 0, 0, 0)",
            "title.text": name,
            "title.font.color": "rgba(220, 220, 220, 255)",
            "legend.font.color": "rgba(220, 220, 220, 255)",
        }

        return layout

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
        self.logger.debug(f"get options. options are {options}")
        return options

    # TODO
    # callback function for dropdown
    # build figure based on the values from the dropdown
    def create_figures(self, series_names: list):
        self.logger.debug(f"creating figures with series {list(self.series.keys())}")
        fig = go.Figure(layout=self.layout(self.name))
        for name in series_names:
            s = self.series[name]
            fig.add_trace(s.get_figure())
        return fig

    def get_html(self):

        drop_down = dcc.Dropdown(id={"name": self.name, "type": self.dropdown_type, "uid": self.uid}, options=self.get_options(),
                                 value=list(self.series.keys()),
                                 multi=True,
                                 className=f"dropdown {self.name}",
                                 style={"background-color": "rgba(0, 0, 0, 0)", "color": "rgba(30, 30, 30, 255)"})

        graph = dcc.Graph(id={"name": self.name, "type": self.graph_type, "uid": self.uid})

        self.logger.debug(f"getting html for graph {self.name}")

        return dbc.Col(
            dbc.Card(
                [
                    drop_down,
                    graph
                ]
            ),
            style={"padding": "10px", "min-width": "900px"}
        )
