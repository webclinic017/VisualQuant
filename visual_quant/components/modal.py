import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import json

from visual_quant.components.component import Component


# dialog for selecting elements to load opened by the add buttons
class Modal(Component):

    def __init__(self, app: dash.Dash, name: str, c_type: str, parent: "Component"):
        super().__init__(app, parent.name)

        self.name = name
        self.type = c_type
        self.parent = parent

        self.button_type = f"{c_type}-modal-button"
        self.input_type = f"{c_type}-modal-input"
        self.dropdown_type = f"{c_type}-modal-dropdown"

        self.options = []
        self.load_options()

        self.input = dbc.Input(
            id={"name": name, "type": self.input_type, "uid": parent.uid},
            placeholder="Container Name",
            type="text",
            style={"background-color": "rgba(50, 50, 50, 255)", "color": "rgba(200, 200, 200, 255)"}
        )

        self.button = dbc.Button(
            html.I(className="fas fa-plus fa-2x"),
            id={"name": name, "type": self.button_type, "uid": parent.uid},
            color="success",
            style={"display": "grid", "justify-self": "end"}
        )

        self.dropdown = dcc.Dropdown(
            id={"name": name, "type": self.dropdown_type, "uid": parent.uid},
            options=self.get_options(),
            value=None,
            style={"background-color": "rgba(50, 50, 50, 255)", "color": "rgba(200, 200, 200, 255)"},
            multi=True
        )

    def load_options(self) -> list:
        return []

    def get_options(self):
        return self.options

    # default empty modal
    def get_html(self):
        self.logger.debug(f"getting html for modal {self.name}")
        modal = dbc.Modal(
            [
                html.P(f"Modal {self.name}")
            ]
        )

        return modal


class AddElementModal(Modal):

    def __init__(self, app: dash.Dash, name: str, parent: Component):
        super().__init__(app, name, "add-element-modal", parent)

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
            id={"name": self.name, "type": self.type, "uid": self.parent.uid},
            is_open=False
        )

        return modal

    def load_options(self, data: dict):
        for chart in data["Charts"]:
            self.options.append(f"Charts.{chart}")

        for list in data["TotalPerformance"]:
            self.options.append(f"TotalPerformance.{list}")

    def get_options(self):
        result = []
        for opt in self.options:
            result.append({"label": str(opt), "value": str(opt)})
        return result


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
            id=self.id,
            is_open=False
        )

        return modal


class SaveModal(Modal):

    def __init__(self, app: dash.Dash, parent: Component):
        super().__init__(app, "layout-save-modal", parent)

    def get_html(self):

        modal = dbc.Modal([
                dbc.ModalHeader(html.H3(f"Save layout")),
                dbc.ModalBody([
                    html.H5("Save a layout"),
                    html.Div([self.input, self.button], style={"display": "grid", "gap": "10px"})
                ])
            ],
                id=self.id,
                is_open=False
            )

        return modal
