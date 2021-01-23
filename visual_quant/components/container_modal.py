import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import json

from visual_quant.components.component import Component


# dialog for selecting elements to load opened by the add buttons
class ContainerModal(Component):

    def __init__(self, app: dash.Dash, name: str, container: "Container"):
        super().__init__(app, name, "container-modal", id(container))

        self.container = container

        self.options = []
        with open("data/results.json", "r") as f:
            self.data = json.load(f)
        self.load_options(self.data)

    def load_options(self, data: dict):
        for chart in data["Charts"]:
            self.options.append(f"Charts.{chart}")

        for list in data["TotalPerformance"]:
            self.options.append(f"TotalPerformance.{list}")

        self.options.append("Container")

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
                dcc.Dropdown(
                    id={"type": "modal-dropdown", "uid": str(id(self.container))},
                    options=self.get_options(),
                    value=None,
                    style={"background-color": "rgba(50, 50, 50, 255)", "color": "rgba(90, 90, 90, 255)"}
                )
            ])
        ],
            id=self.id
        )

        return modal

