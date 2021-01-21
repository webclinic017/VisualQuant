import json
import logging
import dash
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

from visual_quant.components.chart import Chart
from visual_quant.components.list import List
from visual_quant.components.component import Component
from visual_quant.components.container_modal import ContainerModal


# hold a list of components and provide buttons to add further ones
class Container(Component):

    def __init__(self, app: dash.Dash, name: str, layout: str):
        super().__init__(app, name)

        self.layout = layout
        # decide when to make add buttons visible
        self.show_buttons = False

        button_id = f"{self.id}-button"

        self.button = dbc.Button("Add", color="primary", className="add-button", id=button_id)
        self.app.callback(Output("root-modal", "is_open"), [Input(button_id, "n_clicks")])(self.button_callback)

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
            html_obj = dbc.Col(self.html_list(), align="center", id=self.id)
        elif self.layout == "row":
            html_obj = dbc.Row(self.html_list(), justify="center", id=self.id)
        else:
            self.logger.error(f"container layout {self.layout} is not supported. Choose from row, col")
            return None

        return html_obj

    # callback to update the col/row children
    def button_callback(self, n: int):
        return n is not None and n > 0

    def html_list(self):
        # TODO clean up
        html_list = [self.button] + [ele.get_html() for ele in self.elements.values()]
        card_list = [dbc.Card(
            dbc.CardBody([
                html.H4(self.name.split(".")[-1], style={"display": "grid", "justify-self": "center"}),
                x
            ], style={"display": "grid", "justify-items": "stretch"}
            ), style={"width": "300px"}) for x in html_list]

        return card_list