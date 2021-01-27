import dash
import json
import dash_bootstrap_components as dbc
import dash_html_components as html
import plotly.graph_objects as go
from dash.dependencies import Input, Output, State, MATCH, ALL

from visual_quant.components.component import Component
from visual_quant.components.container import Container
from visual_quant.components.modal import AddContainerModal, SaveModal, LoadModal
from visual_quant.components.chart import Chart
from visual_quant.components.list import List
from visual_quant.components.series import Series

ICON_LINK = "https://camo.githubusercontent.com/1287ea52a264e20bf5ff3a0a31166fe03de778ee5f0a4d3dc9e88fb8340346c2/68747470733a2f2f63646e2e7175616e74636f6e6e6563742e636f6d2f7765622f692f32303138303630312d313631352d6c65616e2d6c6f676f2d736d616c6c2e706e67"


# hold a tree of components and provide buttons to add further ones
class Page(Component):
    app = None

    def __init__(self, app: dash.Dash, name: str):
        super().__init__(app, name)

        self.type = "page"
        self.app = app
        self.clicks = {}
        self.container = None

        with open("data/results.json", "r") as f:
            self.data = json.load(f)

        # html elements

        self.open_add_container_button = dbc.Button(
            html.I(className="fas fa-plus fa-2x"),
            style={"color": "rgba(200, 200, 200, 255)",
                   "backgroundColor": "rgba(0, 0, 0, 0)",
                   "justify-self": "center",
                   "margin": "10px"},
            outline=True,
            id={"type": "open-add-container-button", "uid": id(self)}
        )

        self.save_button = dbc.Button(
            [
                html.I(className="fas fa-save fa-2x")
            ],
            style={"color": "rgba(200, 200, 200, 255)",
                   "backgroundColor": "rgba(0, 0, 0, 0)",
                   "justify-self": "end",
                   "margin-right": "0"},
            id={"type": "navbar-save-button", "uid": id(self)}
        )

        self.reset_button = dbc.Button(
            [
                html.I(className="fas fa-redo-alt fa-2x")
            ],
            style={"color": "rgba(200, 200, 200, 255)",
                   "backgroundColor": "rgba(0, 0, 0, 0)",
                   "margin-right": "0"},
            id={"type": "navbar-reset-button", "uid": id(self)}
        )

        self.load_button = dbc.Button(
            [
                html.I(className="fas fa-file-download fa-2x")
            ],
            style={"color": "rgba(200, 200, 200, 255)",
                   "backgroundColor": "rgba(0, 0, 0, 0)",
                   "margin-right": "0"},
            id={"type": "navbar-load-button", "uid": id(self)}
        )

        self.navbar = dbc.Navbar(
            [
                html.Img(src=ICON_LINK, height="35px"),
                self.reset_button,
                self.load_button,
                self.save_button
            ],
            color="rgba(10, 10, 10, 255)",
            dark=True,
            sticky="top",
            style={"display": "grid", "grid-template-columns": "1fr auto auto auto", "gap": "10px"}
        )

        # modals

        self.add_container_modal_name = "add-container-modal"
        self.load_modal_name = "page-load-modal"
        self.save_modal_name = "page-save-modal"

        self.add_elements_modal = AddContainerModal(app, self.add_container_modal_name, self)
        self.load_modal = LoadModal(app, self.load_modal_name, self)
        self.save_modal = SaveModal(app, self.save_modal_name, self)

        # modal callbacks

        app.callback(
            [
                Output({"type": self.type, "uid": MATCH}, "children"),
                Output({"type": self.add_container_modal_name, "uid": MATCH}, "is_open")
            ],
            Input({"type": "open-add-container-button", "uid": MATCH}, "n_clicks"),  # open
            Input({"type": "add-container-modal-button", "uid": MATCH}, "n_clicks"),  # close
            Input({"type": "add-container-modal-input", "uid": MATCH}, "value"),

            State({"type": self.type, "uid": MATCH}, "children"),
            State({"type": self.add_container_modal_name, "uid": MATCH}, "is_open"),
        )(self.add_container_modal_handler)

        app.callback(
            [
                Output({"type": "page-layout", "uid": MATCH}, "children"),
                Output({"type": "layout-load-modal", "uid": MATCH}, "is_open")
            ],
            Input({"type": "navbar-load-button", "uid": MATCH}, "n_clicks"),  # open
            Input({"type": "layout-load-modal-button", "uid": MATCH}, "n_clicks"),  # close

            State({"type": "page-layout", "uid": MATCH}, "children"),
            State({"type": "layout-load-modal", "uid": MATCH}, "is_open")
        )(self.load_modal_handler)

        app.callback(
            Output({"type": "layout-save-modal", "uid": MATCH}, "is_open"),

            Input({"type": "navbar-save-button", "uid": MATCH}, "n_clicks"),  # open
            Input({"type": "layout-save-modal-button", "uid": MATCH}, "n_clicks"),  # close

            State({"type": "layout-save-modal", "uid": MATCH}, "is_open"),
            State({"type": self.type, "uid": MATCH}, "children")
        )(self.save_modal_handler)

        app.callback(
            [
                Output({"type": "container-layout", "uid": MATCH}, "children"),
                Output({"type": "add-element-modal", "uid": MATCH}, "is_open")
            ],
            Input({"type": "open-add-element-modal-button", "uid": MATCH}, "n_clicks"),  # open
            Input({"type": "add-element-modal-button", "uid": MATCH}, "n_clicks"),  # close
            Input({"type": "add-element-modal-dropdown", "uid": MATCH}, "value"),
            Input({"type": "add-element-modal-input", "uid": MATCH}, "value"),

            State({"type": "container-layout", "uid": MATCH}, "children"),
            State({"type": "add-element-modal", "uid": MATCH}, "is_open")
        )(self.add_element_modal_handler)

        # graph callbacks

        app.callback(
            Output({"type": "chart-graph", "uid": MATCH}, "figure"),
            Input({"type": "chart-dropdown", "uid": MATCH}, "value"),
            State({"type": "chart", "uid": MATCH}, "className")
        )(self.graph_dropdown)

        # remove container callback

        app.callback(
            Output({"type": "container-root", "uid": MATCH}, "style"),
            Input({"type": "remove-container-button", "uid": MATCH}, "n_clicks"),
            State({"type": "container-root", "uid": MATCH}, "style")
        )(self.remove_container)

    # methods

    def get_html(self):
        return html.Div(
            [
                html.Div([self.add_elements_modal.get_html(), self.load_modal.get_html(), self.save_modal.get_html()]),
                self.navbar,
                html.Div(
                    children=[],
                    id={"type": "page-layout", "uid": self.uid},
                    style={"display": "grid"}
                ),
                self.open_add_container_button
            ],
            style={"display": "grid"},
            id={"type": self.type, "uid": self.uid}
        )

    def json_from_path(self, path):
        data = self.data
        print(path)
        for p in path.split("."):
            data = data[p]
        return data

    # load chart from json dict
    def load_chart(self, name: str, data: dict):
        self.logger.debug(f"loading chart {name}")
        return Chart.from_json(self.app, data).get_html()

    # load list from json dict or list
    def load_list(self, name: str, data):
        if type(data) == dict:
            return List.from_dict(self.app, name, data).get_html()
        elif type(data) == list:
            return List.from_list(self.app, name, data).get_html()
        else:
            self.logger.error(f"data for list must be a dict or a list")

    def is_clicked(self, name, n):
        if name not in self.clicks:
            self.clicks[name] = 0
        if n is not None:
            clicked = n > self.clicks[name]
            self.clicks[name] = n
            return clicked
        return False

    def get_id_from_ctx(self, ctx: dash.callback_context):
        origin_id = ctx.triggered[0]['prop_id'].split('.')[0]

        if origin_id != "":
            return json.loads(origin_id)
        else:
            return None

    # patten-matching-callbacks

    def add_container_modal_handler(self, n_open, n_close, input_name, children, is_open):
        print("add container modal callback")
        origin_id = self.get_id_from_ctx(dash.callback_context)

        if n_open and origin_id["type"] == "open-add-container-button":
            # toggle open
            return children, True

        if self.is_clicked("page-modal-close", n_close) and input_name is not None:
            children.insert(-1, Container(self.app, input_name, "col").get_html())
            return children, False

        return children, is_open

    def load_modal_handler(self, n_open, n_close, children, is_open):
        print("load modal callback")
        if n_open or n_close:
            return children, not is_open
        return children, is_open

    def save_modal_handler(self, n_open, n_close, is_open, children):
        print("save modal callback")
        if n_open or n_close:
            return not is_open
        return is_open

    def add_element_modal_handler(self, n_open, n_close, dropdown_values: list, input_values, children, is_open):
        origin_id = self.get_id_from_ctx(dash.callback_context)
        if origin_id is None:
            return children, is_open

        if n_open and origin_id["type"] == "open-container-modal-button":
            # toggle open
            return children, True

        close = self.is_clicked(f"close-{origin_id['uid']}", n_close)

        if close:
            # add containers and elements
            if dropdown_values is not None:
                for value in dropdown_values:
                    if value.split(".")[0] == "Charts":
                        children.insert(-1, self.load_chart(value, self.json_from_path(value)))
                    else:
                        children.insert(-1, self.load_list(value, self.json_from_path(value)))

            if input_values is not None:
                children.insert(-1, Container(self.app, input_values, "col").get_html())

            return children, False

        return children, is_open

    def graph_dropdown(self, values: list, chart_name: str):
        fig = go.Figure(layout=Chart.layout(chart_name))
        if values is not None:
            for series_name in values:
                s = Series.from_json(self.app, self.data["Charts"][chart_name]["Series"][series_name])
                fig.add_trace(s.get_figure())
        return fig

    def remove_container(self, n_clicks, style):
        if n_clicks is None:
            return style
        else:
            return {"display": "none"}
