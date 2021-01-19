import json
import logging
import dash
import dash_html_components as html

from visual_quant.components.chart import Chart
from visual_quant.components.list import List
from visual_quant.components.component import Component


class Container(Component):

    def __init__(self, app: dash.Dash, name: str, result_file: str):
        super().__init__(app, name, class_names=["container", name])
        self.result_file = result_file

        with open(result_file, "r") as f:
            self.config = json.load(f)

        self.elements = {}

    @classmethod
    def create_container(cls, app: dash.Dash, name: str, path: str, result_file: str, style: dict = {}):
        page = cls(app, name, result_file, style)
        path_list = path.split(".")
        data = page.config
        try:
            for n in path_list:
                data = data[n]
        except KeyError as e:
            page.logger.error(f"did not find list named {name} in result file {page.result_file}\n{e}")

        if type(data) != dict:
            return
        elif path_list[0] == "Charts" and len(path_list) == 2:
            page.load_chart(path_list[-1])
        elif type(data.values()) not in [dict, list]:
            # TODO don't hard code columns count
            page.load_list(name, path, 4)
        else:
            page.logger.warning(f"cant load from given path: {path}, empty page returned")
        return page

    def load_all_charts(self):
        try:
            chart_names = self.config["Charts"]
        except KeyError as e:
            logging.critical(f"the result file provided does not contain any charts\n{e}")
            return

        for name in chart_names:
            self.load_chart(name)

    def load_chart(self, name: str):
        self.logger.debug(f"loading chart {name}")
        try:
            chart_json = self.config["Charts"][name]
        except KeyError as e:
            self.logger.error(f"did not find chart named {name} in result file {self.result_file}\n{e}")
            return

        self.elements[name] = Chart.from_json(self.app, chart_json)

    def load_list(self, list_name: str, path: str):
        self.logger.debug(f"loading list {list_name}")
        path_list = path.split(".")
        data = self.config
        try:
            for p in path_list:
                data = data[p]
        except KeyError as e:
            self.logger.error(f"did not find list at {path} in result file {self.result_file}\n{e}")

        if type(data) is dict:
            self.elements[list_name] = List.from_dict(self.app, list_name, data)
        elif type(data) is list:
            # TODO
            col = {"Symbol": "Value"} if list_name == "ClosedTrades" else None
            self.elements[list_name] = List.from_list(self.app, list_name, data, collapse=col)

    def add_element(self, name: str, ele: Component):
        self.logger.debug(f"adding element {name}")
        self.elements[name] = ele

    def add_container(self, container):
        self.logger.debug(f"adding container {container.name}")
        self.elements[container.name] = container

    def get_one_html(self, name: str):
        if name in self.elements:
            return self.elements[name].get_html()
        else:
            self.logger.warning(f"the element named {name} was not found")

    def get_html(self):
        return self.get_div(children=[html.H1(self.name), html.Div(children=self.html_list(), className=f"grid {self.name}")])

    def html_list(self):
        return [ele.get_html() for ele in self.elements.values()]
