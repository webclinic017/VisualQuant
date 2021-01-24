import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import json

from visual_quant.components.component import Component


# dialog for selecting elements to load opened by the add buttons
class Modal(Component):

    def __init__(self, app: dash.Dash, type_name: str, parent: "Component"):
        super().__init__(app, parent.name, type_name, id(parent))

        self.parent = parent
        self.options = []

        self.dropdown = dcc.Dropdown(
            id={"type": f"modal-dropdown", "uid": str(id(self.parent))},
            options=self.get_options(),
            value=None,
            style={"background-color": "rgba(50, 50, 50, 255)", "color": "rgba(90, 90, 90, 255)"}
        )

        self.input = dbc.Input(
            id={"type": "modal-input", "uid": str(id(self.parent))},
            placeholder="Container Name",
            type="text",
            style={"background-color": "rgba(50, 50, 50, 255)", "color": "rgba(200, 200, 200, 255)"}
        )

        self.button = dbc.Button(
            html.I(className="fas fa-plus fa-2x"),
            id={"type": "modal-add-button", "uid": str(id(self.parent))},
            color="success",
            style={"display": "grid", "justify-self": "end"}
        )

    def get_options(self):
        result = []
        for opt in self.options:
            result.append({"label": str(opt), "value": str(opt)})
        return result

    def get_html(self):
        self.logger.debug(f"getting html for modal {self.name}")
        modal = dbc.Modal([
            html.P(f"Modal {self.name}")
        ],
            id=self.id
        )

        return modal


class ContainerModal(Modal):

    def __init__(self, app: dash.Dash, parent: Component):
        super().__init__(app, "container-modal", parent)

        with open("data/results.json", "r") as f:
            self.data = json.load(f)
        self.load_options(self.data)

    def get_html(self):
        self.logger.debug(f"getting html for modal {self.name}")
        modal = dbc.Modal([
            dbc.ModalHeader(html.H3(f"Add Elements to {self.name}")),
            dbc.ModalBody([
                html.H5("Add List/Chart"),
                # selection dropdown
                self.dropdown,
                html.Br(),
                html.H5("Add Container"),
                html.Div([self.input, self.button], style={"display": "grid", "gap": "10px"})
            ])
        ],
            id=self.id
        )

        return modal

    def load_options(self, data: dict):
        for chart in data["Charts"]:
            self.options.append(f"Charts.{chart}")

        for list in data["TotalPerformance"]:
            self.options.append(f"TotalPerformance.{list}")


class PageModal(Modal):

    def __init__(self, app: dash.Dash, parent: Component):
        super().__init__(app, "page-modal", parent)

    def get_html(self):
        self.logger.debug(f"getting html for modal {self.name}")
        modal = dbc.Modal([
            dbc.ModalHeader(html.H3(f"Add Container")),
            dbc.ModalBody([
                html.H5("Add Container"),
                html.Div([self.input, self.button], style={"display": "grid", "gap": "10px"})
            ])
        ],
            id=self.id
        )

        return modal
