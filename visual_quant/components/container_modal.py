import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import json

from visual_quant.components.component import Component


# dialog for selecting elements to load opened by the add buttons
class ContainerModal(Component):

    def __init__(self, app: dash.Dash, name: str, container: "Container"):
        super().__init__(app, name)

        self.modal_callback_inputs = [Input("loader-modal-dropdown", "value")]
        self.container = container

        self.options = []
        with open("data/results.json", "r") as f:
            self.data = json.load(f)
        self.load_options(self.data)

        self.logger.debug(f"setting modal {self.name} callback")
        self.app.callback(Output(self.container.id, "children"), [Input(f"{self.id}-dropdown", "value")])(self.dropdown_callback)

    def dropdown_callback(self, value):
        if value is not None:
            chart_data = self.data
            for p in value.split("."):
                chart_data = chart_data[p]
            self.container.load_chart(value, chart_data)
        return self.container.html_list()

    def load_options(self, data: dict):
        for chart in data["Charts"]:
            self.options.append(f"Charts.{chart}")

    def get_options(self):
        result = []
        for opt in self.options:
            result.append({"label": str(opt), "value": str(opt)})
        return result

    def get_html(self):
        self.logger.debug(f"getting html for modal {self.name}")
        modal = dbc.Modal([
            dbc.ModalHeader(self.name),
            dbc.ModalBody([
                # selection dropdown
                dcc.Dropdown(id=f"{self.id}-dropdown", options=self.get_options(), value=None, style={"background-color": "rgba(50, 50, 50, 255)", "color": "rgba(90, 90, 90, 255)"})
            ])
        ], id=self.id, is_open=False)

        return modal

