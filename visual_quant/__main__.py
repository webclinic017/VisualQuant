import dash
import dash_html_components as html
import logging
import random
import string

from visual_quant.components.container import Container

if __name__ == "__main__":
    app = dash.Dash(__name__)

    logger = logging.getLogger("visual_quant")
    logger.setLevel(logging.DEBUG)

    format = logging.Formatter("%(module)s - %(funcName)s - %(levelname)s :: %(message)s")
    handler = logging.StreamHandler()
    handler.setFormatter(format)

    logger.addHandler(handler)

    c1 = Container.create_page(app, "Trade", "TotalPerformance.TradeStatistics", "data/results.json")

    c2 = Container.create_page(app, "Equity", "Charts.Strategy Equity", "data/results.json")
    c3 = Container.create_page(app, "Benchmark", "Charts.Benchmark", "data/results.json")

    c4 = Container(app, "Graphs", "data/results.json", rows=[1, 1])
    c4.add_container(c2)
    c4.add_container(c3)

    c = Container(app, "Results", "data/results.json", columns=[1, 3])
    c.add_container(c1)
    c.add_container(c4)

    app.layout = html.Div(children=c.get_html())
    app.run_server(debug=True)
