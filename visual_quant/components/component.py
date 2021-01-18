import dash
import logging


class Component:

    def __init__(self, app: dash.Dash, name: str):
        self.app = app
        self.name = name
        self.logger = logging.getLogger(__name__)

    def get_html(self, *args, **kwargs):
        self.logger.error(f"class {type(self)} does not provide the methode get_html")
