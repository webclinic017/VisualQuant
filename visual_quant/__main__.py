import dash
import dash_html_components as html
import dash_bootstrap_components as dbc
import logging
from dash.dependencies import Input, Output
import json

import visual_quant.components.page as page
from visual_quant.components.container import Container
from visual_quant.components.container_modal import ContainerModal

lists = ["TotalPerformance.TradeStatistics", "TotalPerformance.PortfolioStatistics", "TotalPerformance.ClosedTrades"]
charts = ["Charts.Average Cross", "Charts.Strategy Equity", "Charts.Trade Plot", "Charts.Benchmark"]

logger = logging.getLogger("visual_quant")


if __name__ == "__main__":
    app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

    logger.setLevel(logging.DEBUG)

    format = logging.Formatter("%(module)s - %(funcName)s - %(levelname)s :: %(message)s")
    handler = logging.StreamHandler()
    handler.setFormatter(format)

    logger.addHandler(handler)

    container = Container(app, "Results", "col")

    app.layout = container.get_html()

    #  modal.set_callback()

    app.title = "LEAN Results"
    app.run_server(debug=True, dev_tools_ui=False, dev_tools_props_check=False)
