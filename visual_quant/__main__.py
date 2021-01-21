import dash
import dash_html_components as html
import dash_bootstrap_components as dbc
import logging
import random
import string

from visual_quant.components.container import Container
import visual_quant.components.page as page

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

    page = page.Page.from_file(app, "Results", "data/results.json", lists, charts)

    app.layout = html.Div(page.get_html())

    app.title = "LEAN Results"
    app.run_server(debug=True)
