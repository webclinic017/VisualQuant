import dash
import dash_bootstrap_components as dbc
import logging

from visual_quant.components.container import Container
from visual_quant.components.page import Page

logger = logging.getLogger("visual_quant")

if __name__ == "__main__":

    app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

    logger.setLevel(logging.DEBUG)

    format = logging.Formatter("%(module)s - %(funcName)s - %(levelname)s :: %(message)s")
    handler = logging.StreamHandler()
    handler.setFormatter(format)
    logger.addHandler(handler)

    container = Container(app, "Results", "col")
    page = Page(app, "Root Page")
    page.add_container(container)

    app.layout = page.get_html()

    app.title = "LEAN Results"
    app.run_server(debug=True, dev_tools_props_check=False)
