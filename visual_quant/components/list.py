import plotly.graph_objects as go
import dash_core_components as dcc
import dash

from visual_quant.components.component import Component


class List(Component):

    def __init__(self, app: dash.Dash, name: str, column_count: int, alignment="left", line_color="rgba(150, 150, 150, 255)", font_color="rgba(200, 200, 200, 255)", fill_color="rgba(0, 0, 0, 0)"):
        super().__init__(app, name)
        self.column_count = column_count
        self.header = ["<b>Name</b>", "<b>Value</b>"] * column_count
        self.entries = {}

        self.alignment = alignment
        self.line_color = line_color
        self.font_color = font_color
        self.fill_color = fill_color

    def add_entry(self, name: str, value):
        self.entries[name] = value

    @property
    def cells(self):
        entries_per_column = max(len(self.entries) // self.column_count, 1)
        extra_entries = len(self.entries) % self.column_count if len(self.entries) > self.column_count else 0
        keys = list(self.entries.keys())
        values = list(self.entries.values())
        columns = []
        for i in range(0, len(self.entries) - extra_entries, entries_per_column):
            l_column = keys[i:i + entries_per_column]
            r_column = values[i:i + entries_per_column]
            columns.append(l_column)
            columns.append(r_column)
        for i in range(0, extra_entries, 2):
            columns[i].append(keys[-extra_entries - i])
            columns[i + 1].append(values[-extra_entries - i])
        return {"values": columns, "align": self.alignment, "line.color": self.line_color, "fill.color": self.fill_color, "font.color": self.font_color}

    def get_html(self):
        fig = go.Figure(layout={"paper_bgcolor": self.fill_color, "plot_bgcolor": self.fill_color, "font.color": self.font_color, "title.text": self.name},
                        data=[go.Table(cells=self.cells,
                                       header={"values": self.header, "align": self.alignment, "line.color": self.line_color, "fill.color": self.fill_color, "font.color": self.font_color})])
        return dcc.Graph(figure=fig)
