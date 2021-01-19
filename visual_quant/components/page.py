import dash
import json

from visual_quant.components.component import Component
from visual_quant.components.container import Container
from visual_quant.components.list import List
from visual_quant.components.chart import Chart


def result_file_to_array(app: dash.Dash, file_path: str, lists: list, charts: list):
    elements = {}
    with open(file_path, "r") as f:
        json_data = json.load(f)

    for name in lists:
        path = name.split(".")
        data = json_data
        for p in path:
            data = data[p]

        if type(data) is dict:
            elements[name] = List.from_dict(app, name, data)
        elif type(data) is list:
            # TODO
            col = {"Symbol": "Value"} if name == "TotalPerformance.ClosedTrades" else None
            elements[name] = List.from_list(app, name, data, collapse=col)

    for name in charts:
        path = name.split(".")
        data = json_data
        for p in path:
            data = data[p]

        elements[name] = Chart.from_json(app, data)

    return elements


class Page(Component):

    def __init__(self, app: dash.Dash, name: str):
        super().__init__(app, name, class_names=["page", name])
        self.elements = {}

    @ classmethod
    def from_json(cls, app: dash.Dash, name: str, result_file: str):
        page = cls(app, name)

        with open(result_file, "r") as f:
            page.config = json.load(f)

        rolling_windows = Container(app, "RollingWindow", result_file)
        for time_frame in page.config["RollingWindow"]:
            window_frame = Container(app, str(time_frame), result_file)

            for key in page.config["RollingWindow"][time_frame]:
                if key == "ClosedTrades":
                    continue
                window_frame.load_list(str(key), f"RollingWindow.{time_frame}.{key}")

            rolling_windows.add_container(window_frame)

        total_performance_s = Container(app, "Performance", result_file)
        for key in ["TradeStatistics", "PortfolioStatistics"]:
            total_performance_s.load_list(str(key), f"TotalPerformance.{key}")

        total_performance_o = Container(app, "ClosedTrades", result_file)
        total_performance_o.load_list("ClosedTrades", "TotalPerformance.ClosedTrades")

        total_performance = Container(app, "TotalPerformance", result_file)
        total_performance.add_container(total_performance_s)
        total_performance.add_container(total_performance_o)

        charts = Container(app, "Charts", result_file)
        for chart in page.config["Charts"]:
            charts.load_chart(str(chart))

        stats = Container(app, "Stats", result_file)
        for key in ["ProfitLoss", "Statistics", "RuntimeStatistics"]:
            stats.load_list(str(key), str(key))

        page.add_container(total_performance)
        page.add_container(charts)
        page.add_container(stats)
        # page.add_container(rolling_windows)

        return page

    def add_element(self, name: str, ele: Component):
        self.logger.debug(f"adding element {name}")
        self.elements[name] = ele

    def add_container(self, container):
        self.logger.debug(f"adding page {container.name}")
        self.elements[container.name] = container

    def get_html(self):
        return self.get_div(children=self.html_list())

    def html_list(self):
        return [ele.get_html() for ele in self.elements.values()]
