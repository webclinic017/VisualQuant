import dash
import dash_html_components as html
import logging


# super class for all components
class Component:

    def __init__(self, app: dash.Dash, name: str):
        self.app = app
        self.name = name
        self.id = str(hash(id(self)))
        self.logger = logging.getLogger(__name__)

    def get_html(self, *args, **kwargs):
        self.logger.error(f"class {type(self)} does not provide the methode get_html")

    def __str__(self):
        return f"{self.name}-{type(self)}"
