import dash
import json
import os
import dash_bootstrap_components as dbc
import dash_html_components as html
import plotly.graph_objects as go
from dash.dependencies import Input, Output, State, MATCH, ALL

import visual_quant.web_components.component as component
import visual_quant.web_components.container as container
import visual_quant.web_components.modal as modal
import visual_quant.web_components.chart as chart
import visual_quant.web_components.list as dash_list
import visual_quant.web_components.series as series
import visual_quant.web_components.table as table
import visual_quant.data.config_loader as cfg

ICON_LINK = "https://camo.githubusercontent.com/1287ea52a264e20bf5ff3a0a31166fe03de778ee5f0a4d3dc9e88fb8340346c2/68747470733a2f2f63646e2e7175616e74636f6e6e6563742e636f6d2f7765622f692f32303138303630312d313631352d6c65616e2d6c6f676f2d736d616c6c2e706e67"

PAGE_ADD_CONTAINER_BUTTON = "page-add-container-button"
PAGE_SAVE_BUTTON = "page-save-button"
PAGE_LOAD_BUTTON = "page-load-button"
PAGE_RESET_BUTTON = "page-reset-button"
PAGE_LAYOUT = "page-layout"
PAGE_NAME = "page"


# hold a tree of components and provide buttons to add further ones
class Page(component.Component):
    app = None

    def __init__(self, app: dash.Dash, name: str):
        super().__init__(name, "")

        self.app = app
        self.clicks = {}
        self.container = None

        self.layout_save_dir = "./layout-saves"
        self.last_save_name = ""

        self.layout = {}

        self.data = cfg.result_file_json()

        # html elements

        self.open_add_container_button = dbc.Button(
            html.I(className="fas fa-plus fa-2x"),
            style={"color": "rgba(200, 200, 200, 255)",
                   "backgroundColor": "rgba(0, 0, 0, 0)",
                   "justify-self": "center",
                   "margin": "10px"},
            outline=True,
            id={"type": PAGE_ADD_CONTAINER_BUTTON, "uid": self.uid}
        )

        self.save_button = dbc.Button(
            [
                html.I(className="fas fa-save fa-2x")
            ],
            style={"color": "rgba(200, 200, 200, 255)",
                   "backgroundColor": "rgba(0, 0, 0, 0)",
                   "justify-self": "end",
                   "margin-right": "0"},
            id={"type": PAGE_SAVE_BUTTON, "uid": self.uid}
        )

        self.reset_button = dbc.Button(
            [
                html.I(className="fas fa-redo-alt fa-2x")
            ],
            style={"color": "rgba(200, 200, 200, 255)",
                   "backgroundColor": "rgba(0, 0, 0, 0)",
                   "margin-right": "0"},
            id=PAGE_RESET_BUTTON
        )

        self.load_button = dbc.Button(
            [
                html.I(className="fas fa-file-download fa-2x")
            ],
            style={"color": "rgba(200, 200, 200, 255)",
                   "backgroundColor": "rgba(0, 0, 0, 0)",
                   "margin-right": "0"},
            id={"type": PAGE_LOAD_BUTTON, "uid": self.uid}
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

        self.add_elements_modal = modal.AddContainerModal(self.add_container_modal_name, self)
        self.load_modal = modal.LoadModal(self.load_modal_name, self, self.layout_save_dir)
        self.save_modal = modal.SaveModal(self.save_modal_name, self)

    # methods

    def get_page_components(self, children):
        components = [
            html.Div([self.add_elements_modal.get_html(), self.load_modal.get_html(), self.save_modal.get_html()]),
            self.navbar,
            html.Div(
                children=children,
                id={"type": PAGE_LAYOUT, "uid": self.uid},
                style={"display": "grid"}
            ),
            self.open_add_container_button
        ]
        return components

    def get_html(self):
        return html.Div(
            children=self.get_page_components([]),
            style={"display": "grid"},
            id={"type": PAGE_NAME, "uid": self.uid}
        )

    def json_from_path(self, path):
        data = self.data

        for p in path.split("."):
            data = data[p]
        return data

    # load chart from json dict
    def load_chart(self, name: str, data: dict):
        self.logger.debug(f"loading chart {name}")
        return chart.Chart.from_json(data)

    # load list from json dict or list
    @staticmethod
    def load_list(name: str, path: str, data):
        return dash_list.List.from_json(name, path, data)

    @staticmethod
    def load_table(name: str, path: str, data):
        return table.Table.from_json(name, path, data)

    def is_clicked(self, name, n):
        if name not in self.clicks:
            self.clicks[name] = 0
        if n is not None:
            clicked = n > self.clicks[name]
            self.clicks[name] = n
            return clicked
        return False

    @staticmethod
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

            if ele_type == "container":
                children = self.load_from_save(ele["children"], path)
                container_element = container.Container(ele["name"], ele["direction"], path)
                container_element.children = children
                result.append(container_element.get_html())

            elif ele_type == "list":
                # load the list from save json
                result_file_data = self.json_from_path(ele["path"])
                result.append(dash_list.List.from_save(self.app, ele, result_file_data).get_html())

            elif ele_type == "table":
                result_file_data = self.json_from_path(ele["path"])
                result.append(table.Table.from_save(self.app, ele, result_file_data).get_html())

            elif ele_type == "chart":
                # load the chart from saved json
                result_file_data = self.json_from_path(ele["path"])
                result.append(chart.Chart.from_save_file(ele, result_file_data).get_html())

        return result

    def get_layout_file_options(self):
        options = []
        if os.path.isdir(self.layout_save_dir):
            for file_name in os.listdir(self.layout_save_dir):
                if os.path.isfile(os.path.join(self.layout_save_dir, file_name)):
                    options.append(file_name)

            result = []
            for opt in options:
                result.append({"label": str(opt), "value": str(opt)})
            return result

        else:
            self.logger.error(f"the save directory {self.layout_save_dir} does not exist")

    # patten-matching-callbacks

    def add_container_modal_handler(self, n_open, n_close, input_name, children, is_open):

        if self.is_clicked("add container open", n_open):
            # toggle open
            return children, True

        if self.is_clicked("add container close", n_close):
            if input_name is not None and input_name not in self.layout and "." not in input_name:

                # TODO make the layout direction changeable
                direction = "col"
                container_element = container.Container(input_name, direction, "")
                children.insert(-1, container_element.get_html())

                self.layout[input_name] = container_element.json
                return children, False

            else:
                self.logger.error(
                    "container name enter is not valid. They can not container '.' or already be in the layout")

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
    def save_modal_handler(self, n_open, n_close, save_name: str, is_open: bool):
        if self.is_clicked("open save", n_open):
            return True, self.get_layout_file_options()

        elif self.is_clicked("close save", n_close):
            # create the output dir if it doesn't exist yet
            if not os.path.isdir(self.layout_save_dir):
                os.mkdir(self.layout_save_dir)

            # save the layout to the file
            with open(os.path.join(self.layout_save_dir, save_name), "w") as f:
                json.dump(self.layout, f, indent=2)
            return False, self.get_layout_file_options()

        return is_open, self.get_layout_file_options()

    def add_element_modal_handler(self, n_open, n_close, dropdown_values: list, input_value: str, children,
                                  is_open: bool, path: str):

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
                    json_path = value.split(".")
                    if json_path[0] == "Charts":
                        chart_ele = self.load_chart(json_path[-1], self.json_from_path(value))
                        children.insert(-1, chart_ele.get_html())
                        loc[json_path[-1]] = chart_ele.json
                    else:
                        list_ele = self.load_list(json_path[-1], path, self.json_from_path(value))
                        children.insert(-1, list_ele.get_html())
                        loc[json_path[-1]] = list_ele.json

            if input_value is not None and not input_value == "" and "." not in input_value:

                if input_value not in loc:
                    direction = "col"
                    container_element = container.Container(input_value, direction, path)
                    # add the container before the button at the end
                    children.insert(-1, container_element.get_html())
                    loc[input_value] = container_element.json
                else:
                    self.logger.warning(f"container named {input_value} already exists")

            return children, False

        return children, is_open

    def remove_container(self, n_clicks, style, path):
        # TODO fix container only being removed after 2 click

        if self.is_clicked(f"remove {path}", n_clicks):

            self.logger.debug(f"removing container at {path}")
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