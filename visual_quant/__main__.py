import dash
import dash_bootstrap_components as dbc
import logging
import dash_html_components as html

from visual_quant.components.container import Container
from visual_quant.components.page import Page

FONT_AWESOME = "https://use.fontawesome.com/releases/v5.7.2/css/all.css"


def run():
    app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY, FONT_AWESOME])

    logger = logging.getLogger("visual_quant")
    logger.setLevel(logging.DEBUG)

    format = logging.Formatter("%(module)s - %(funcName)s - %(levelname)s :: %(message)s")
    handler = logging.StreamHandler()
    handler.setFormatter(format)
    logger.addHandler(handler)

    page = Page(app, "Root Page")
    app.layout = html.Div(page.get_html(), id="root")

    app.title = "LEAN Results"
    app.run_server(debug=True, dev_tools_props_check=False)


if __name__ == "__main__":
    run()
