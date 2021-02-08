import dash
import dash_html_components as html
import dash_bootstrap_components as dbc

from visual_quant.components.component import Component
from visual_quant.components.modal import AddElementModal


CONTAINER_ADD_ELEMENT_BUTTON = "container-add-element-button"
CONTAINER_LAYOUT = "container-layout"
CONTAINER_REMOVE_BUTTON = "remove-container-button"
CONTAINER_ROOT = "container-root"
CONTAINER_PATH = "container-path"


# hold a list of components and provide buttons to add further ones
class Container(Component):

    # constructors

    def __init__(self, app: dash.Dash, name: str, direction: str, path: str):
        super().__init__(app, name, path)

        self.direction = direction
        self.children = []

        # generate components
        self.modal = AddElementModal(app, f"container-{self.name}-modal", self)

        self.add_element_button = dbc.Button(
            html.I(className="fas fa-plus fa-2x"),
            style={"color": "rgba(200, 200, 200, 255)", "backgroundColor": "rgba(0, 0, 0, 0)", "justify-self": "center"},
            outline=True,
            id={"type": CONTAINER_ADD_ELEMENT_BUTTON, "uid": self.uid}
        )

        self.remove_button = dbc.Button(
            html.I(className="fas fa-trash fa-2x"),
            style={"justify-self": "end", "color": "rgba(200, 200, 200, 255)", "padding": "20px 10px 0px 10px"},
            color="rgba(0, 0, 0, 0)",
            id={"type": CONTAINER_REMOVE_BUTTON, "uid": self.uid}
        )

    # properties

    @property
    def json(self) -> dict:
        json = {
            "type": "container",
            "name": self.name,
            "direction": self.direction,
            "children": {}
        }

        return json

    # methods

    # overwrite the get_html function
    def get_html(self):
        self.logger.debug(f"getting html for container {self.name}")
        if self.direction == "col":
            html_obj = dbc.Col(self.html_list(), id={"type": CONTAINER_ROOT, "uid": self.uid})
        elif self.direction == "row":
            html_obj = dbc.Row(self.html_list(), id={"type": CONTAINER_ROOT, "uid": self.uid})
        else:
            self.logger.error(f"container direction {self.direction} is not supported. Choose from row, col")
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
                        self.children + [self.add_element_button],
                        align="center",
                        style={"display": "grid"}
                    )
                ],
                id={"type": CONTAINER_LAYOUT, "uid": self.uid},
            ),
            # hold the path info in className here no not interferer with bootstrap classNames
            html.Div(style={"display": "none"}, id={"type": CONTAINER_PATH, "uid": self.uid}, className=self.path)
        ]

        return layout_list
