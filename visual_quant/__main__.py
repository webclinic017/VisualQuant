import dash
import dash_html_components as html
import logging

from visual_quant.data_objects.page import Page


if __name__ == "__main__":
    app = dash.Dash(__name__)

    logging.getLogger("visual_quant").setLevel(logging.DEBUG)
    page = Page(app, "data/results.json")
    page.load_all_charts()

    app.layout = html.Div(children=page.get_all_dives())
    app.run_server(debug=True)
