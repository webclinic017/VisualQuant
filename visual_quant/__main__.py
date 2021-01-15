import dash
import dash_html_components as html
import logging

from visual_quant.data_objects.graph import Graph
from visual_quant.data_objects.list import List


if __name__ == "__main__":
    app = dash.Dash(__name__)

    logging.getLogger("visual_quant").setLevel(logging.DEBUG)
    graph = Graph(app, "data/results.json")
    html_list = List(2, 25)

    html_list.add_entry("sharp ratio", 24.5)
    html_list.add_entry("sharp ratio", 24.5)
    html_list.add_entry("sharp ratio", 24.5)
    html_list.add_entry("sharp ratio", 24.5)
    html_list.add_entry("sharp ratio", 24.5)
    html_list.add_entry("sharp ratio", 24.5)
    html_list.add_entry("sharp ratio", 24.5)
    html_list.add_entry("sharp ratio", 24.5)
    html_list.add_entry("sharp ratio", 24.5)
    html_list.add_entry("sharp ratio", 24.5)
    html_list.add_entry("sharp ratio", 24.5)
    html_list.add_entry("sharp ratio", 24.5)
    html_list.add_entry("sharp ratio", 24.5)
    html_list.add_entry("sharp ratio", 24.5)
    html_list.add_entry("sharp ratio", 24.5)

    app.layout = html.Div(children=html_list.get_html())
    app.run_server(debug=True)
