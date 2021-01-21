import dash
import dash_html_components as html
import dash_bootstrap_components as dbc
import logging
from dash.dependencies import Input, Output

import visual_quant.components.page as page
from visual_quant.components.container import Container
from visual_quant.components.container_modal import ContainerModal

lists = ["TotalPerformance.TradeStatistics", "TotalPerformance.PortfolioStatistics", "TotalPerformance.ClosedTrades"]
charts = ["Charts.Average Cross", "Charts.Strategy Equity", "Charts.Trade Plot", "Charts.Benchmark"]

if __name__ == "__main__":
    app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

    logger = logging.getLogger("visual_quant")
    logger.setLevel(logging.DEBUG)

    format = logging.Formatter("%(module)s - %(funcName)s - %(levelname)s :: %(message)s")
    handler = logging.StreamHandler()
    handler.setFormatter(format)

    logger.addHandler(handler)

    container = Container(app, "Top Level", "row")
    modal = ContainerModal(app, "root-modal")

    app.layout = html.Div([
        container.get_html(),
        modal.get_html()
    ], id="root")

    #  modal.set_callback()

    app.title = "LEAN Results"
    app.run_server(debug=True)
