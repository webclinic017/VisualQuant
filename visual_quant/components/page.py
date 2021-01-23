import dash
import json
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output, State, MATCH, ALL

from visual_quant.components.component import Component
from visual_quant.components.container import Container
from visual_quant.components.chart import Chart
from visual_quant.components.list import List


# hold a tree of components and provide buttons to add further ones
class Page(Component):

    app = None

    def __init__(self, app: dash.Dash, name: str):
        super().__init__(app, name, "page", id(self))

        self.elements = {}
        self.app = app
        self.last_n = 0

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

    def add_container(self, container):
        self.logger.debug(f"adding page {container.name}")
        self.elements[container.name] = container

    def get_html(self):
        return html.Div([x.get_html() for x in self.elements.values()])

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
