import dash
import dash_html_components as html
import dash_bootstrap_components as dbc

from visual_quant.components.component import Component
from visual_quant.components.modal import AddElementModal


# hold a list of components and provide buttons to add further ones
class Container(Component):

    def __init__(self, app: dash.Dash, name: str, layout: str):
        super().__init__(app, name)

        self.layout = layout
        # decide when to make add buttons visible
        self.show_buttons = False

        self.layout_type_name = "container-layout"
        self.add_element_button_type = "open-add-element-modal-button"
        self.remove_button_type = "remove-container-button"

        # generate components
        self.modal = AddElementModal(app, f"container-{self.name}-modal", self)

        self.add_element_button = dbc.Button(
            html.I(className="fas fa-plus fa-2x"),
            style={"color": "rgba(200, 200, 200, 255)", "backgroundColor": "rgba(0, 0, 0, 0)", "justify-self": "center"},
            outline=True,
            id={"type": self.add_element_button_type, "uid": self.uid}
        )

        self.remove_button = dbc.Button(
            html.I(className="fas fa-trash fa-2x"),
            style={"justify-self": "end", "color": "rgba(200, 200, 200, 255)", "padding": "20px 10px 0px 10px"},
            color="rgba(0, 0, 0, 0)",
            id={"type": self.remove_button_type, "uid": self.uid}
        )

    # overwrite the get_html function
    def get_html(self):
        self.logger.debug(f"getting html for container {self.name}")
        if self.layout == "col":
            html_obj = dbc.Col(self.html_list(), id={"type": "container-root", "uid": id(self)})
        elif self.layout == "row":
            html_obj = dbc.Row(self.html_list(), id={"type": "container-root", "uid": id(self)})
        else:
            self.logger.error(f"container layout {self.layout} is not supported. Choose from row, col")
            return None

        return html_obj

    def html_list(self):
        layout_list = [
            self.modal.get_html(),  # normally hidden modal
            html.Div(
                [
                    html.H2(self.name, style={"justify-self": "start", "margin-top": "8px", "margin-bottom": "0px"}),
                    self.remove_button
                ],
                style={"display": "grid", "grid-template-columns": "1fr 1fr"}
            ),
            html.Hr(style={"background-color": "rgba(252, 156, 4, 255)", "height": "10px", "border-width": "0", "border-radius": "7px 7px 7px 7px"}),
            dbc.Row(
                children=[
                    dbc.Col(
                        self.add_element_button,
                        align="center",
                        style={"display": "grid"}
                    )
                ],
                id={"type": self.layout_type_name, "uid": self.uid}
            )
        ]

        return layout_list
