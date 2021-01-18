import dash
import dash_html_components as html
import logging
import random
import string

from visual_quant.components.page import Page

if __name__ == "__main__":
    app = dash.Dash(__name__)

    logging.getLogger("visual_quant").setLevel(logging.DEBUG)
    page1 = Page.create_page(app, "Trade", "TotalPerformance.TradeStatistics", "data/results.json")
    page2 = Page.create_page(app, "Strategy Equity", "Charts.Strategy Equity", "data/results.json")
    page = Page(app, "Results", "data/results.json")
    page.add_page(page1)
    page.add_page(page2)

    app.layout = html.Div(children=page.get_html())
    app.run_server(debug=True)
