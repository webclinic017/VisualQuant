import dash
import dash_bootstrap_components as dbc
import logging

from visual_quant.components.container import Container
from visual_quant.components.page import Page

FONT_AWESOME = "https://use.fontawesome.com/releases/v5.7.2/css/all.css"

if __name__ == "__main__":

    app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY, FONT_AWESOME])

    logger = logging.getLogger("visual_quant")
    logger.setLevel(logging.DEBUG)

    format = logging.Formatter("%(module)s - %(funcName)s - %(levelname)s :: %(message)s")
    handler = logging.StreamHandler()
    handler.setFormatter(format)
    logger.addHandler(handler)

    container = Container(app, "Results", "col")
    page = Page(app, "Root Page")
    page.set_container(container)

    app.layout = page.get_html()

    app.title = "LEAN Results"
    app.run_server(debug=True, dev_tools_props_check=False)
