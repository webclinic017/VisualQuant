import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
from dash.dependencies import Input, Output, State

from visual_quant.components.component import Component


# dialog for selecting elements to load opened by the add buttons
class ContainerModal(Component):

    def __init__(self, app: dash.Dash, name: str):
        super().__init__(app, name)
        self.modal_callback_inputs = [Input("loader-modal-dropdown", "value")]
        self.is_open = False

    def dropdown_callback(self, value):
        print("callback", value)
        return dbc.Card([dbc.CardBody("new element")])

    def load_options(self):
        pass

    def get_options(self):
        return [{"label": "A", "value": "A"}]

    def set_callback(self):
        pass

    def get_html(self):
        modal = dbc.Modal([
            dbc.ModalHeader(self.name),
            dbc.ModalBody([
                # selection dropdown
                dcc.Dropdown(id=f"{self.id}-dropdown", options=self.get_options(), value=None, style={"background-color": "rgba(50, 50, 50, 255)", "color": "rgba(90, 90, 90, 255)"})
            ])
        ], id=self.name, is_open=self.is_open)

        self.app.callback(Output(self.name, "children"), [Input(f"{self.id}-dropdown", "value")], prevent_initial_call=True)(self.dropdown_callback)

        return modal

