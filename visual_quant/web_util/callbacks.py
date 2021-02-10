import dash
from dash.dependencies import Input, Output, State, MATCH

import visual_quant.web_components.page as page
import visual_quant.web_components.component as component
import visual_quant.web_components.container as container
import visual_quant.web_components.modal as modal
import visual_quant.web_components.chart as chart
import visual_quant.web_components.list as dash_list
import visual_quant.web_components.series as series
import visual_quant.web_components.table as table
import visual_quant.data.config_loader as cfg


def type_id(element_type: str) -> dict:
    return {"type": element_type, "uid": MATCH}


# modal callbacks

def register_callbacks(app: dash.Dash, page_obj: page.Page):
    app.callback(
        [
            Output(type_id(page.PAGE_LAYOUT), "children"),
            Output(type_id(modal.MODAL_ADD_CONTAINER), "is_open")
        ],
        Input(type_id(page.PAGE_ADD_CONTAINER_BUTTON), "n_clicks"),  # open
        Input(type_id(modal.MODAL_BUTTON + modal.MODAL_ADD_CONTAINER), "n_clicks"),  # close
        Input(type_id(modal.MODAL_INPUT + modal.MODAL_ADD_CONTAINER), "value"),  # container name

        State(type_id(page.PAGE_LAYOUT), "children"),
        State(type_id(modal.MODAL_ADD_CONTAINER), "is_open"),
    )(page_obj.add_container_modal_handler)

    app.callback(
        [
            Output(type_id(page.PAGE_NAME), "children"),
            Output(type_id(modal.MODAL_LOAD_LAYOUT), "is_open")
        ],
        Input(type_id(page.PAGE_LOAD_BUTTON), "n_clicks"),  # open
        Input(type_id(modal.MODAL_BUTTON + modal.MODAL_LOAD_LAYOUT), "n_clicks"),  # close
        Input(type_id(modal.MODAL_DROPDOWN + modal.MODAL_LOAD_LAYOUT), "value"),  # file to be loaded

        State(type_id(page.PAGE_NAME), "children"),
        State(type_id(modal.MODAL_LOAD_LAYOUT), "is_open")
    )(page_obj.load_modal_handler)

    app.callback(
        Output(type_id(modal.MODAL_SAVE_LAYOUT), "is_open"),
        Output(type_id(modal.MODAL_DROPDOWN + modal.MODAL_LOAD_LAYOUT), "options"),

        Input(type_id(page.PAGE_SAVE_BUTTON), "n_clicks"),  # open
        Input(type_id(modal.MODAL_BUTTON + modal.MODAL_SAVE_LAYOUT), "n_clicks"),  # close
        Input(type_id(modal.MODAL_INPUT + modal.MODAL_SAVE_LAYOUT), "value"),

        State(type_id(modal.MODAL_SAVE_LAYOUT), "is_open"),
    )(page_obj.save_modal_handler)

    app.callback(
        [
            Output(type_id(container.CONTAINER_LAYOUT), "children"),
            Output(type_id(modal.MODAL_ADD_ELEMENT), "is_open")
        ],
        Input(type_id(container.CONTAINER_ADD_ELEMENT_BUTTON), "n_clicks"),  # open
        Input(type_id(modal.MODAL_BUTTON + modal.MODAL_ADD_ELEMENT), "n_clicks"),  # close
        Input(type_id(modal.MODAL_DROPDOWN + modal.MODAL_ADD_ELEMENT), "value"),
        Input(type_id(modal.MODAL_INPUT + modal.MODAL_ADD_ELEMENT), "value"),

        State(type_id(container.CONTAINER_LAYOUT), "children"),
        State(type_id(modal.MODAL_ADD_ELEMENT), "is_open"),
        State(type_id(container.CONTAINER_PATH), "className")
    )(page_obj.add_element_modal_handler)

    # remove container callback

    app.callback(
        Output(type_id(container.CONTAINER_ROOT), "style"),

        Input(type_id(container.CONTAINER_REMOVE_BUTTON), "n_clicks"),

        State(type_id(container.CONTAINER_ROOT), "style"),
        State(type_id(container.CONTAINER_PATH), "className")
    )(page_obj.remove_container)

    app.callback(
        Output("root", "children"),

        Input(page.PAGE_RESET_BUTTON, "n_clicks"),

        State("root", "children")
    )(page_obj.reset_page)

    # graph callback
    app.callback(
        Output(type_id(chart.CHART_GRAPH), "figure"),

        Input(type_id(chart.CHART_DROPDOWN), "value"),

        State(type_id(chart.CHART_NAME), "className")
    )(chart.Chart.graph_dropdown)
