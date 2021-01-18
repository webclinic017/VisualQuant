import dash

from visual_quant.components.component import Component


class Page(Component):

    def __init__(self, app: dash.Dash, name: str):
        super().__init__(app, name)

    @ classmethod
    def from_json(cls, app: dash.Dash, name: str, result_file: str):
        page = cls(app, name)
        with open(result_file, "r") as f:
            page.config = f.read()


    def get_html(self, *args, **kwargs):
        pass
