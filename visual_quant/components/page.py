import dash
import json
import dash_bootstrap_components as dbc
import dash_html_components as html

from visual_quant.components.component import Component
from visual_quant.components.container import Container


# hold a tree of components and provide buttons to add further ones
class Page(Component):

    def __init__(self, app: dash.Dash, name: str, file_path: str):
        super().__init__(app, name)

        self.elements = {}

        with open(file_path, "r") as f:
            self.config = json.load(f)

    @classmethod
    def from_file(cls, app: dash.Dash, name: str, file_path: str, lists: list, charts: list):
        page = cls(app, name, file_path)

        for name in lists:
            path = name.split(".")
            data = page.config
            for p in path:
                data = data[p]

            c = Container(app, name, "row")
            c.load_list(name, data)
            page.add_container(c)

        for name in charts:
            path = name.split(".")
            data = page.config
            for p in path:
                data = data[p]

            c = Container(app, name, "row")
            c.load_chart(name, data)
            page.add_container(c)

        return page

    def __getitem__(self, index):
        return self.elements[index].get_html()

    def make_card(self, com: Component):
        return com

    def add_element(self, name: str, ele: Component):
        self.logger.debug(f"adding element {name}")
        self.elements[name] = ele

    def add_container(self, container):
        self.logger.debug(f"adding page {container.name}")
        self.elements[container.name] = container

    def get_html(self):
        return html.Div(children=self.html_list())

    def html_list(self):
        return [ele.get_html() for ele in self.elements.values()]
