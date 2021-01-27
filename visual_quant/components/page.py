import dash
import json
import dash_bootstrap_components as dbc
import dash_html_components as html
import plotly.graph_objects as go
from dash.dependencies import Input, Output, State, MATCH, ALL

from visual_quant.components.component import Component
from visual_quant.components.container import Container
from visual_quant.components.modal import PageModal, SaveModal
from visual_quant.components.chart import Chart
from visual_quant.components.list import List
from visual_quant.components.series import Series

ICON_LINK = "https://camo.githubusercontent.com/1287ea52a264e20bf5ff3a0a31166fe03de778ee5f0a4d3dc9e88fb8340346c2/68747470733a2f2f63646e2e7175616e74636f6e6e6563742e636f6d2f7765622f692f32303138303630312d313631352d6c65616e2d6c6f676f2d736d616c6c2e706e67"


# hold a tree of components and provide buttons to add further ones
class Page(Component):
    app = None

    def __init__(self, app: dash.Dash, name: str):
        super().__init__(app, name, "page", id(self))

        self.app = app
        self.clicks = {}
        self.container = None

        self.add_container_button = dbc.Button(
            html.I(className="fas fa-plus fa-2x"),
            style={"color": "rgba(200, 200, 200, 255)",
                   "backgroundColor": "rgba(0, 0, 0, 0)",
                   "justify-self": "center",
                   "margin": "10px"},
            outline=True,
            id={"type": "open-page-modal-button", "uid": id(self)}
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

        self.page_modal = PageModal(app, self)
        self.save_modal = SaveModal(app, self)

        with open("data/results.json", "r") as f:
            self.data = json.load(f)

        app.callback(
            [Output({"type": "page", "uid": MATCH}, "children"),
             Output({"type": "page-modal", "uid": MATCH}, "is_open")],
            Input({"type": "open-page-modal-button", "uid": MATCH}, "n_clicks"),  # open
            Input({"type": "modal-add-button", "uid": MATCH}, "n_clicks"),  # close
            Input({"type": "modal-input", "uid": MATCH}, "value"),
            State({"type": "page", "uid": MATCH}, "children"),
            State({"type": "page-modal", "uid": MATCH}, "is_open"),
        )(self.add_page_modal_handler)

        app.callback(
            [Output({"type": "container-layout", "uid": MATCH}, "children"),
             Output({"type": "container-modal", "uid": MATCH}, "is_open")],
            Input({"type": "open-container-modal-button", "uid": MATCH}, "n_clicks"),
            Input({"type": "modal-add-button", "uid": MATCH}, "n_clicks"),
            Input({"type": "modal-dropdown", "uid": MATCH}, "value"),
            Input({"type": "modal-input", "uid": MATCH}, "value"),
            State({"type": "container-layout", "uid": MATCH}, "children"),
            State({"type": "container-modal", "uid": MATCH}, "is_open")
        )(self.add_container_modal_handler)

        app.callback(
            Output({"type": "layout-save-modal", "uid": MATCH}, "is_open"),
            Input({"type": "navbar-save-button", "uid": MATCH}, "n_clicks"),
            Input({"type": "modal-add-button", "uid": MATCH}, "n_clicks"),
            State({"type": "layout-save-modal", "uid": MATCH}, "is_open")
        )(self.save_modal_handler)

        app.callback(
            Output({"type": "chart-graph", "uid": MATCH}, "figure"),
            Input({"type": "chart-dropdown", "uid": MATCH}, "value"),
            State({"type": "chart", "uid": MATCH}, "className")
        )(self.graph_dropdown)

        app.callback(
            Output({"type": "container-root", "uid": MATCH}, "style"),
            Input({"type": "remove-container-button", "uid": MATCH}, "n_clicks"),
            State({"type": "container-root", "uid": MATCH}, "style")
        )(self.remove_container)

    def get_html(self):
        return html.Div(
            [
                html.Div([self.page_modal.get_html(), self.save_modal.get_html()]),
                self.navbar, self.add_container_button
            ],
            id=self.id,
            style={"display": "grid"}
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

    def add_container_modal_handler(self, n_open, n_close, dropdown_values: list, input_values, children, is_open):
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

    def add_page_modal_handler(self, n_open, n_close, input_name, children, is_open):
        origin_id = self.get_id_from_ctx(dash.callback_context)

        if n_open and origin_id["type"] == "open-page-modal-button":
            # toggle open
            return children, True

        if self.is_clicked("page-modal-close", n_close) and input_name is not None:
            children.insert(-1, Container(self.app, input_name, "col").get_html())
            return children, False

        return children, is_open

    def save_modal_handler(self, n_open, n_close, is_open):
        if n_open or n_close:
            return not is_open
        return is_open
