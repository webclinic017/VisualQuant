import json
import logging
import dash

from visual_quant.data_objects.chart import Chart


class Graph:

    def __init__(self, app: dash.Dash, result_file: str):
        self.logger = logging.getLogger(__name__)
        self.app = app

        with open(result_file, "r") as f:
            self.config = json.load(f)

        self.charts = {}

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

        self.charts[name] = Chart.from_json(self.app, chart_json)

    def get_html(self, name: str):
        if name in self.charts:
            return self.charts[name].get_div()
        else:
            self.logger.warning(f"the graph named {name} was not found")

    def html_list(self):
        return [chart.get_div() for chart in self.charts]
