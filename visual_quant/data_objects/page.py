import json
import logging
import dash

from visual_quant.data_objects.chart import Chart
from visual_quant.data_objects.list import List


class Page:

    def __init__(self, app: dash.Dash, name: str, result_file: str):
        self.logger = logging.getLogger(__name__)
        self.app = app
        self.name = name

        with open(result_file, "r") as f:
            self.config = json.load(f)

        self.elements = {}

    @classmethod
    def create_page(cls, app: dash.Dash, name: str, result_file: str):
        page = cls(app, name)

    def load_all_charts(self):
        try:
            chart_names = self.config["Charts"]
        except KeyError as e:
            logging.critical(f"the result file provided does not contain any charts\n{e}")
            return

        for name in chart_names:
            self.load_chart(name)

    def load_chart(self, name: str):
        try:
            chart_json = self.config["Charts"][name]
        except KeyError as e:
            self.logger.error(f"did not find chart named {name} in result file {self.result_file}\n{e}")
            return

        self.elements[name] = Chart.from_json(self.app, chart_json)

    def load_list(self, name: str, columns_count: int):
        path = name.split(".")
        list_json = self.config
        try:
            for n in path:
                list_json = list_json[n]
        except KeyError as e:
            self.logger.error(f"did not find list named {name} in result file {self.result_file}\n{e}")

        html_list = List(path[-1], columns_count)

        for entry_name in list_json:
            value = list_json[entry_name]
            if type(list_json[entry_name]) not in [dict, list]:
                html_list.add_entry(entry_name, value)

        self.elements[name] = html_list

    def add_element(self, name: str, ele):
        self.elements[name] = ele

    def get_html(self, name: str):
        if name in self.elements:
            return self.elements[name].get_html()
        else:
            self.logger.warning(f"the element named {name} was not found")

    def get_div(self):


    def html_list(self):
        return [ele.get_html() for ele in self.elements]
