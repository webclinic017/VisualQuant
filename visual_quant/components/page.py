import dash
import json
import os
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
from visual_quant.components.table import Table

ICON_LINK = "https://camo.githubusercontent.com/1287ea52a264e20bf5ff3a0a31166fe03de778ee5f0a4d3dc9e88fb8340346c2/68747470733a2f2f63646e2e7175616e74636f6e6e6563742e636f6d2f7765622f692f32303138303630312d313631352d6c65616e2d6c6f676f2d736d616c6c2e706e67"


# hold a tree of components and provide buttons to add further ones
class Page(Component):
    app = None

    def __init__(self, app: dash.Dash, name: str):
        super().__init__(app, name, "")

        self.type = "page"
        self.app = app
        self.clicks = {}
        self.container = None

        self.layout_save_dir = "./layout-saves"
        self.last_save_name = ""

        self.layout = {}

        # TODO configurable result file
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
            id="page-reset-button"
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
        self.load_modal = LoadModal(app, self.load_modal_name, self, self.layout_save_dir)
        self.save_modal = SaveModal(app, self.save_modal_name, self)

        # modal callbacks

        app.callback(
            [
                Output({"type": "page-layout", "uid": MATCH}, "children"),
                Output({"type": self.add_container_modal_name, "uid": MATCH}, "is_open")
            ],
            Input({"type": "open-add-container-button", "uid": MATCH}, "n_clicks"),  # open
            Input({"type": "add-container-modal-button", "uid": MATCH}, "n_clicks"),  # close
            Input({"type": "add-container-modal-input", "uid": MATCH}, "value"),

            State({"type": "page-layout", "uid": MATCH}, "children"),
            State({"type": self.add_container_modal_name, "uid": MATCH}, "is_open"),
        )(self.add_container_modal_handler)

        app.callback(
            [
                Output({"type": self.type, "uid": MATCH}, "children"),
                Output({"type": "layout-load-modal", "uid": MATCH}, "is_open")
            ],
            Input({"type": "navbar-load-button", "uid": MATCH}, "n_clicks"),  # open
            Input({"type": "layout-load-modal-button", "uid": MATCH}, "n_clicks"),  # close
            Input({"type": "layout-load-modal-dropdown", "uid": MATCH}, "value"),

            State({"type": self.type, "uid": MATCH}, "children"),
            State({"type": "layout-load-modal", "uid": MATCH}, "is_open")
        )(self.load_modal_handler)

        app.callback(
            Output({"type": "layout-save-modal", "uid": MATCH}, "is_open"),

            Input({"type": "navbar-save-button", "uid": MATCH}, "n_clicks"),  # open
            Input({"type": "layout-save-modal-button", "uid": MATCH}, "n_clicks"),  # close
            Input({"type": "layout-save-modal-input", "uid": MATCH}, "value"),

            State({"type": "layout-save-modal", "uid": MATCH}, "is_open"),
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
            State({"type": "add-element-modal", "uid": MATCH}, "is_open"),
            State({"type": "container-path", "uid": MATCH}, "className")
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

            State({"type": "container-root", "uid": MATCH}, "style"),
            State({"type": "container-path", "uid": MATCH}, "className")
        )(self.remove_container)

        app.callback(
            Output("root", "children"),

            Input("page-reset-button", "n_clicks"),

            State("root", "children")
        )(self.reset_page)

    # methods

    def get_page_components(self, children):
        components = [
            html.Div([self.add_elements_modal.get_html(), self.load_modal.get_html(), self.save_modal.get_html()]),
            self.navbar,
            html.Div(
                children=children,
                id={"type": "page-layout", "uid": self.uid},
                style={"display": "grid"}
            ),
            self.open_add_container_button
        ]
        return components

    def get_html(self):
        return html.Div(
            children=self.get_page_components([]),
            style={"display": "grid"},
            id={"type": self.type, "uid": self.uid}
        )

    def json_from_path(self, path):
        data = self.data

        for p in path.split("."):
            data = data[p]
        return data

    # load chart from json dict
    def load_chart(self, name: str, data: dict):
        self.logger.debug(f"loading chart {name}")
        return Chart.from_json(self.app, data)

    # load list from json dict or list
    def load_list(self, name: str, path: str, data):
        return List.from_json(self.app, name, path, data)

    def load_table(self, name: str, path: str, data):
        return Table.from_json(self.app, name, path, data)

    def is_clicked(self, name, n):
        if name not in self.clicks:
            self.clicks[name] = 0
        if n is not None:
            clicked = n > self.clicks[name]
            self.clicks[name] = n
            return clicked
        return False

    @ staticmethod
    def get_id_from_ctx(ctx: dash.callback_context):
        origin_id = ctx.triggered[0]['prop_id'].split('.')[0]

        if origin_id != "":
            return json.loads(origin_id)
        else:
            return None

    def layout_at(self, path: str):
        path_list = list(filter(None, path.split(".")))
        loc = self.layout
        for p in path_list:
            loc = loc[p]
            if loc["type"] == "container":
                loc = loc["children"]
        return loc

    def load_from_save(self, data: dict, path: str) -> list:
        # function only gets called on containers. build them and recursively add their children
        result = []
        for k in data.keys():
            ele = data[k]
            ele_type = ele["type"]

            result_file_data = self.json_from_path(ele["path"])

            if ele_type == "container":
                children = self.load_from_save(ele["children"], path)
                container = Container(self.app, ele["name"], ele["direction"], path)
                container.children = children
                result.append(container.get_html())

            elif ele_type == "list":
                # load the list from save json
                result.append(List.from_save(self.app, ele, result_file_data).get_html())

            elif ele_type == "table":
                result.append(Table.from_save(self.app, ele, result_file_data).get_html())

            elif ele_type == "chart":
                # load the chart from saved json
                result.append(Chart.from_save(self.app, ele, result_file_data).get_html())

        return result

    # patten-matching-callbacks

    def add_container_modal_handler(self, n_open, n_close, input_name, children, is_open):

        if self.is_clicked("add container open", n_open):
            # toggle open
            return children, True

        if self.is_clicked("add container close", n_close) and input_name is not None:
            if "." in input_name:
                self.logger.error("container names can't container a '.'")
                return children, is_open
            # TODO make the layout direction changeable
            direction = "col"
            container = Container(self.app, input_name, direction, "")
            children.insert(-1, container.get_html())

            self.layout[input_name] = container.json
            return children, False

        return children, is_open

    def load_modal_handler(self, n_open: int, n_close: int, file_name: str, children: list, is_open: bool):
        # TODO
        if self.is_clicked("open load", n_open):
            return children, True

        if self.is_clicked("close load", n_close):
            if os.path.isfile(os.path.join(self.layout_save_dir, file_name)):
                # the file exists, load the json
                with open(os.path.join(self.layout_save_dir, file_name), "r") as f:
                    json_data = json.load(f)
                    self.layout = json_data
                    new_children = self.load_from_save(json_data, "")

            return self.get_page_components(new_children), False

        return children, is_open

    # callback
    def save_modal_handler(self, n_open, n_close, is_open, save_name: str):
        if self.is_clicked("open save", n_open):
            return not is_open

        elif self.is_clicked("close save", n_close):
            # create the output dir if it doesn't exist yet
            if not os.path.isdir(self.layout_save_dir):
                os.mkdir(self.layout_save_dir)

            # save the layout to the file
            # if the name hasn't changed save to the same file
            save_name = save_name if type(save_name) is str else self.last_save_name
            self.last_save_name = save_name

            with open(os.path.join(self.layout_save_dir, save_name), "w") as f:
                json.dump(self.layout, f, indent=2)
            return False

        return is_open

    def add_element_modal_handler(self, n_open, n_close, dropdown_values: list, input_value: str, children, is_open: bool, path: str):

        # use id to identify unique buttons because callback is shared between containers
        origin_id = self.get_id_from_ctx(dash.callback_context)
        if origin_id is None:
            return children, is_open

        # TODO change hardcoded name
        if self.is_clicked(f"open-{origin_id['uid']}", n_open):
            # toggle open
            return children, True

        if self.is_clicked(f"close-{origin_id['uid']}", n_close):
            # traverse the self.layout to add the container as a child
            loc = self.layout_at(path)

            # add containers and elements
            if dropdown_values is not None:
                for value in dropdown_values:
                    path = value.split(".")
                    if value.split(".")[0] == "Charts":
                        chart = self.load_chart(path[-1], self.json_from_path(value))
                        children.insert(-1, chart.get_html())
                        loc[path[-1]] = chart.json
                    else:
                        list_ele = self.load_list(path[-1], ".".join(path[:-1]), self.json_from_path(value))
                        children.insert(-1, list_ele.get_html())
                        loc[path[-1]] = list_ele.json

            if input_value is not None and not input_value == "":

                direction = "col"
                container = Container(self.app, input_value, direction, path)
                # add the container before the button at the end
                children.insert(-1, container.get_html())
                loc[input_value] = container.json

            return children, False

        return children, is_open

    def graph_dropdown(self, values: list, chart_name: str):
        fig = go.Figure(layout=Chart.layout(chart_name))
        if values is not None:
            for series_name in values:
                s = Series.from_json(self.app, self.data["Charts"][chart_name]["Series"][series_name])
                fig.add_trace(s.get_figure())
        return fig

    def remove_container(self, n_clicks, style, path):
        if n_clicks is not None:
            # TODO better way to delete from layout dict
            path_list = list(filter(None, path.split(".")))
            loc = self.layout
            for p in path_list[:-1]:
                loc = loc[p]
                if loc["type"] == "container":
                    loc = loc["children"]
            del loc[path_list[-1]]
            return {"display": "none"}
        return style

    def reset_page(self, n_clicks, children):
        if n_clicks is not None:
            self.layout = {}
            return self.get_html()
        return children
