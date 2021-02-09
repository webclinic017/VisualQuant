import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import os
import json

import visual_quant.web_components.component as component


MODAL_BUTTON = "modal-button"
MODAL_INPUT = "modal-input"
MODAL_DROPDOWN = "modal-dropdown"

MODAL_ADD_ELEMENT = "add-element-modal"
MODAL_ADD_CONTAINER = "add-container-modal"
MODAL_SAVE_LAYOUT = "layout-save-modal"
MODAL_LOAD_LAYOUT = "layout-load-modal"


# dialog for selecting elements to load opened by the add buttons
class Modal(component.Component):

    def __init__(self, app: dash.Dash, name: str, c_type: str, parent: component.Component):
        super().__init__(app, parent.name, parent.path)

        self.name = name
        self.type = c_type
        self.parent = parent
        self.id = {"type": self.type, "uid": self.parent.uid}

        self.options = []

        self.input = None
        self.button = None
        self.dropdown = None

    def generate_html(self, multi_dropdown):
        self.input = dbc.Input(
            id={"type": MODAL_INPUT + self.type, "uid": self.parent.uid},
            placeholder="Container Name",
            type="text",
            style={"background-color": "rgba(50, 50, 50, 255)", "color": "rgba(200, 200, 200, 255)"}
        )

        self.button = dbc.Button(
            html.I(className="fas fa-plus fa-2x"),
            id={"type": MODAL_BUTTON + self.type, "uid": self.parent.uid},
            color="success",
            style={"display": "grid", "justify-self": "end"}
        )

        self.dropdown = dcc.Dropdown(
            id={"type": MODAL_DROPDOWN + self.type, "uid": self.parent.uid},
            options=self.get_options(),
            value=None,
            style={"background-color": "rgba(50, 50, 50, 255)", "color": "rgba(40, 40, 40, 255)", "font-color": "rgba(0, 0, 0, 255)"},
            multi=multi_dropdown
        )

    def load_options(self, *args) -> list:
        return []

    def get_options(self):
        result = []
        for opt in self.options:
            result.append({"label": str(opt), "value": str(opt)})
        return result

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

    def __init__(self, app: dash.Dash, name: str, parent: component.Component):
        super().__init__(app, name, MODAL_ADD_ELEMENT, parent)

        with open(result_file, "r") as f:
            self.data = json.load(f)
        self.load_options(self.data)

        self.generate_html(True)

    def get_html(self):
        self.logger.debug(f"getting html for modal {self.name}, uid: {self.parent.uid}")
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
            id=self.id,
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
            # only show last name of path as name
            result.append({"label": opt.split(".")[-1], "value": str(opt)})
        return result


class AddContainerModal(Modal):

    def __init__(self, app: dash.Dash, name: str, parent: component.Component):
        super().__init__(app, name, MODAL_ADD_CONTAINER, parent)
        self.generate_html(False)

    def get_html(self):
        self.logger.debug(f"getting html for modal {self.type}, uid: {self.parent.uid}")
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


class SaveModal(Modal):

    def __init__(self, app: dash.Dash, name: str, parent: component.Component):
        super().__init__(app, name, MODAL_SAVE_LAYOUT, parent)
        self.generate_html(False)

    def get_html(self):
        modal = dbc.Modal([
            dbc.ModalHeader(html.H3(f"Save layout")),
            dbc.ModalBody([
                html.H5("Save a layout"),
                html.Div([self.input, self.button], style={"display": "grid", "gap": "10px"})
            ])
        ],
            id=self.id
        )

        return modal


class LoadModal(Modal):

    def __init__(self, app: dash.Dash, name: str, parent: component.Component, save_directory: str):
        super().__init__(app, name, MODAL_LOAD_LAYOUT, parent)

        self.save_directory = save_directory
        self.load_options()

        self.generate_html(False)

    def get_html(self):
        modal = dbc.Modal(
            [
                dbc.ModalHeader(html.H3(f"Load layout")),
                dbc.ModalBody(
                    [
                        html.Div([self.dropdown, self.button], style={"display": "grid", "gap": "10px"})
                    ]
                )
            ],
            id=self.id
        )

        return modal

