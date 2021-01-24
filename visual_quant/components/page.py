import dash
import json
import dash_bootstrap_components as dbc
import dash_html_components as html
import plotly.graph_objects as go
from dash.dependencies import Input, Output, State, MATCH, ALL

from visual_quant.components.component import Component
from visual_quant.components.container import Container
from visual_quant.components.modal import PageModal
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

        self.navbar = dbc.Navbar(
            [
                dbc.Row(
                    [
                        dbc.Col(html.Img(src=ICON_LINK, height="35px")),
                        dbc.Col(
                            [

                            ]
                        )
                    ]
                )
            ],
            color="rgba(10, 10, 10, 255)",
            dark=True,
            sticky="top"
        )

        self.add_container_button = dbc.Button(
            html.I(className="fas fa-plus fa-2x"),
            style={"color": "rgba(200, 200, 200, 255)",
                   "backgroundColor": "rgba(0, 0, 0, 0)",
                   "justify-self": "center"},
            outline=True,
            id={"type": "add-container-button", "uid": id(self)}
        )

        self.modal = PageModal(app, self)

        with open("data/results.json", "r") as f:
            self.data = json.load(f)

        app.callback(
            Output({"type": "container-modal", "uid": MATCH}, "is_open"),
            Input({"type": "add-element-button", "uid": MATCH}, "n_clicks"),
            Input({"type": "modal-add-button", "uid": MATCH}, "n_clicks"),
            State({"type": "container-modal", "uid": MATCH}, "id"),
            initial_callback=False
        )(self.open_modal)

        app.callback(
            Output({"type": "container-layout", "uid": MATCH}, "children"),
            Input({"type": "modal-dropdown", "uid": MATCH}, "value"),
            Input({"type": "modal-input", "uid": MATCH}, "value"),
            Input({"type": "modal-add-button", "uid": MATCH}, "n_clicks"),
            State({"type": "container-layout", "uid": MATCH}, "children"),
        )(self.add_container_element)

        app.callback(
            Output({"type": "chart-graph", "uid": MATCH}, "figure"),
            Input({"type": "chart-dropdown", "uid": MATCH}, "value"),
            State({"type": "chart", "uid": MATCH}, "className")
        )(self.graph_dropdown)

        app.callback(
            Output({"type": "container-root", "uid": MATCH}, "style"),
            Input({"type": "remove-button", "uid": MATCH}, "n_clicks"),
            State({"type": "container-root", "uid": MATCH}, "style"),
        )(self.remove_container)

        app.callback(
            Output({"type": "page-modal", "uid": MATCH}, "is_open"),
            Input({"type": "add-container-button", "uid": MATCH}, "n_clicks"),
            Input({"type": "modal-add-button", "uid": MATCH}, "n_clicks"),
            State({"type": "page-modal", "uid": MATCH}, "id"),
            initial_callback=False
        )(self.open_modal)

        app.callback(
            Output({"type": "page", "uid": MATCH}, "children"),
            Input({"type": "modal-add-button", "uid": MATCH}, "n_clicks"),
            Input({"type": "modal-input", "uid": MATCH}, "value"),
            State({"type": "page", "uid": MATCH}, "children")
        )(self.add_container)

    def get_html(self):
        return html.Div([self.modal.get_html(), self.navbar, self.add_container_button], id=self.id, style={"display": "grid"})

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

    def open_modal(self, n_open, n_close, modal_id):
        origin_id = self.get_id_from_ctx(dash.callback_context)
        if origin_id is None:
            return True

        print(n_open, n_close)

        open = self.is_clicked(f"open-{modal_id}", n_open)
        close = self.is_clicked(f"close-{modal_id}", n_close)

        if origin_id["type"] in ["add-element-button", "add-container-button"]:
            return open
        elif origin_id["type"] == "modal-add-button":
            return not close

    def add_container_element(self, dropdown_value, input_value, n_click, children):

        clicked = self.is_clicked("add", n_click)

        origin_id = self.get_id_from_ctx(dash.callback_context)

        if clicked and input_value is not None:
            children.insert(-1, Container(self.app, input_value, "col").get_html())
            return children

        elif dropdown_value is not None and origin_id["type"] == "modal-dropdown":
            dict_data = self.data
            path = dropdown_value.split(".")
            for p in path:
                dict_data = dict_data[p]

            if path[0] == "Charts":
                children.insert(-1, self.load_chart(dropdown_value, dict_data))
            else:
                children.insert(-1, self.load_list(dropdown_value, dict_data))

        return children

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

    def open_page_modal(self, n_clicks):
        print("open modal", n_clicks)
        return True#self.is_clicked("open page", n_clicks)

    def add_container(self, n_clicks, name, children):
        origin_id = self.get_id_from_ctx(dash.callback_context)

        if self.is_clicked("add container", n_clicks) and origin_id["type"] == "modal-add-button":
            children.insert(-1, Container(self.app, name, "col").get_html())

        return children
