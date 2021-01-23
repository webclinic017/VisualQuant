import dash
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, MATCH, ALL

from visual_quant.components.component import Component
import visual_quant.components.container_modal


# hold a list of components and provide buttons to add further ones
class Container(Component):

    def __init__(self, app: dash.Dash, name: str, layout: str):
        super().__init__(app, name, "container", id(self))

        self.layout = layout
        # decide when to make add buttons visible
        self.show_buttons = False

        # generate components
        self.modal = visual_quant.components.container_modal.ContainerModal(app, f"{self.name}", self)
        self.button = dbc.Button("Add", color="primary", className="add-button", id={"type": "add-element-button", "uid": id(self)}, outline=True)

    # overwrite the get_html function
    def get_html(self):
        self.logger.debug(f"getting html for container {self.name}")
        if self.layout == "col":
            html_obj = dbc.Col(self.html_list())
        elif self.layout == "row":
            html_obj = dbc.Row(self.html_list())
        else:
            self.logger.error(f"container layout {self.layout} is not supported. Choose from row, col")
            return None

        return html_obj

    def html_list(self):
        self.logger.debug(f"getting html_list for container {self.name}")

        layout_list = [
            self.modal.get_html(),  # normally hidden modal
            dbc.Row(html.H4(self.name), justify="center"),  # heading
            dbc.Row(children=[], id={"type": "container-layout", "uid": str(id(self))}),  # callback container
            dbc.Row(self.button, justify="center")  # add element button
        ]

        return layout_list
