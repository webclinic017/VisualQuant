import dash
import json
import dash_bootstrap_components as dbc
import dash_html_components as html
import plotly.graph_objects as go
from dash.dependencies import Input, Output, State, MATCH, ALL

from visual_quant.components.component import Component
from visual_quant.components.container import Container
from visual_quant.components.chart import Chart
from visual_quant.components.list import List
from visual_quant.components.series import Series


ICON_LINK = "https://camo.githubusercontent.com/1287ea52a264e20bf5ff3a0a31166fe03de778ee5f0a4d3dc9e88fb8340346c2/68747470733a2f2f63646e2e7175616e74636f6e6e6563742e636f6d2f7765622f692f32303138303630312d313631352d6c65616e2d6c6f676f2d736d616c6c2e706e67"

# hold a tree of components and provide buttons to add further ones
class Page(Component):

    app = None

    def __init__(self, app: dash.Dash, name: str):
        super().__init__(app, name, "page", id(self))

        self.app = app
        self.last_n = 0
        self.container = None

        self.navbar = dbc.Navbar(
            [
                dbc.Row(
                    [
                        dbc.Col(html.Img(src=ICON_LINK, height="35px"))
                    ]
                )
            ],
            color="rgba(10, 10, 10, 255)",
            dark=True,
            sticky="top"
        )

        with open("data/results.json", "r") as f:
            self.data = json.load(f)

        app.callback(
            Output({"type": "container-modal", "uid": MATCH}, "is_open"),
            Input({"type": "add-element-button", "uid": MATCH}, "n_clicks")
        )(self.open_modal)

        app.callback(
            Output({"type": "container-layout", "uid": MATCH}, "children"),
            Input({"type": "modal-dropdown", "uid": MATCH}, "value"),
            State({"type": "container-layout", "uid": MATCH}, "children")
        )(self.add_container_element)

        app.callback(
            Output({"type": "chart-graph", "uid": MATCH}, "figure"),
            Input({"type": "chart-dropdown", "uid": MATCH}, "value"),
            State({"type": "chart", "uid": MATCH}, "className")
        )(self.graph_dropdown)

    def set_container(self, container: Container):
        self.container = container

    def get_html(self):
        return html.Div([self.navbar, self.container.get_html(style={"margin-top": "10px"})])

    # load chart from json dict
    def load_chart(self, name: str, data: dict):
        self.logger.debug(f"loading chart {name}")
        return Chart.from_json(self.app, data).get_html()

    # load list from json dict or list
    def load_list(self, name: str, data):
        if type(data) == dict:
            return List.from_dict(self.app, name, data).get_html()
        elif type(data) == list:
            return List.from_list(self.app, name, data).get_html()
        else:
            self.logger.error(f"data for list must be a dict or a list")

    # patten-matching-callbacks

    def open_modal(self, n):
        open = n is not None and n > self.last_n
        self.last_n = n if n is not None else 0
        return open

    def add_container_element(self, value, children):
        if value is not None:

            if value == "Container":
                children.append(Container(self.app, value, "col").get_html())
                return children

            dict_data = self.data
            path = value.split(".")
            for p in path:
                dict_data = dict_data[p]

            if path[0] == "Charts":
                children.append(self.load_chart(value, dict_data))
            else:
                children.append(self.load_list(value, dict_data))

        return children

    # TODO
    # callback function for dropdown
    # build figure based on the values from the dropdown
    def graph_dropdown(self, values: list, chart_name: str):
        print(chart_name)
        fig = go.Figure(layout=Chart.layout(chart_name))
        if values is not None:
            for series_name in values:
                s = Series.from_json(self.app, self.data["Charts"][chart_name]["Series"][series_name])
                fig.add_trace(s.get_figure())
        return fig
