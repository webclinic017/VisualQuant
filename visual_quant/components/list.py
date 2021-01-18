import plotly.graph_objects as go
import dash_core_components as dcc
import dash
import dash_table
import pandas as pd

from visual_quant.components.component import Component


class List(Component):

    def __init__(self, app: dash.Dash, name: str, column_count: int, alignment="left", font_size=17, font_color="rgba(200, 200, 200, 255)", fill_color="rgba(0, 0, 0, 0)"):
        super().__init__(app, name)
        self.column_count = column_count
        self.header = ["<b>Name</b>", "<b>Value</b>"] * column_count
        self.entries = pd.DataFrame()

        self.alignment = alignment
        self.font_size = font_size
        self.font_color = font_color
        self.fill_color = fill_color

    def add_entry(self, data: pd.DataFrame):
        self.logger.debug(f"adding data\n{data}")
        self.entries.append(data, ignore_index=True)

    def get_html(self):
        self.logger.debug(f"getting html list data {self.entries}")
        table = dash_table.DataTable(data=self.entries.to_dict("records"),
                                     columns=[{"name": i, "id": i} for i in self.entries.columns],
                                     style_as_list_view=True,
                                     style_cell={'textAlign': 'left', 'backgroundColor': self.fill_color, "color": self.font_color, "font_size": f"{self.font_size}px"},
                                     style_cell_conditional=[{'if': {'column_id': "value"}, 'textAlign': 'right'}],
                                     style_header={'display': 'none'})
        return table
