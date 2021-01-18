import dash
import dash_html_components as html
import logging
import random
import string

from visual_quant.data_objects.page import Page


if __name__ == "__main__":
    app = dash.Dash(__name__)

    logging.getLogger("visual_quant").setLevel(logging.DEBUG)
    page = Page(app, "data/results.json")
    page.load_list("TotalPerformance")

    app.layout = html.Div(children=page.get_html("TotalPerformance"))
    app.run_server(debug=True)
