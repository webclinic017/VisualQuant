import json
import logging
import dash
import dash_html_components as html
import dash_bootstrap_components as dbc

from visual_quant.components.chart import Chart
from visual_quant.components.list import List
from visual_quant.components.component import Component


class Container(Component):

    def __init__(self, app: dash.Dash, name: str, layout: str):
        super().__init__(app, name, class_names=["container", name])

        self.layout = layout
        self.elements = {}

    def load_chart(self, name: str, data: dict):
        self.logger.debug(f"loading chart {name}")

        self.elements[name] = Chart.from_json(self.app, data)

    def load_list(self, name: str, data):
        if type(data) == dict:
            self.elements[name] = List.from_dict(self.app, name, data)
        elif type(data) == list:
            self.elements[name] = List.from_list(self.app, name, data)
        else:
            self.logger.error(f"data for list must be a dict or a list")

    def add_element(self, name: str, ele: Component):
        self.logger.debug(f"adding element {name}")
        self.elements[name] = ele

    def add_container(self, container):
        self.logger.debug(f"adding container {container.name}")
        self.elements[container.name] = container

    def get_html(self):
        if self.layout == "col":
            html = dbc.Col(self.html_list())
        elif self.layout == "row":
            html = dbc.Row(self.html_list())
        else:
            self.logger.error(f"container layout {self.layout} is not supported. Choose from row, col")
            return None

        return self.get_div(children=html)

    def html_list(self):
        return [ele.get_html() for ele in self.elements.values()]
