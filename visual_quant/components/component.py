import dash
import dash_html_components as html
import logging


class Component:

    def __init__(self, app: dash.Dash, name: str, class_names: list = None):
        self.app = app
        self.name = name
        self.logger = logging.getLogger(__name__)
        self.class_names = class_names

    def get_div(self, **kwargs):
        return html.Div(**kwargs, className=" ".join(self.class_names))

    def get_html(self, *args, **kwargs):
        self.logger.error(f"class {type(self)} does not provide the methode get_html")

    def __str__(self):
        return f"{self.name}-{type(self)}"
