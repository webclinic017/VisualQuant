import dash
import dash_table
import pandas as pd
import dash_html_components as html
import dash_bootstrap_components as dbc

from visual_quant.web_components.component import Component


# hold a list (or table) of information and render using dash datatable
# consider splitting the 2 behaviors in subclasses
class List(Component):

    # constructors

    def __init__(self, app: dash.Dash, name: str, path: str, alignment="left", font_size=17, font_color="rgba(200, 200, 200, 255)", fill_color="rgba(0, 0, 0, 0)"):
        super().__init__(app, name, path)
        self.entries = pd.DataFrame()

        # TODO base color on theme directly
        self.alignment = alignment
        self.font_size = font_size
        self.font_color = font_color
        self.fill_color = fill_color

    @classmethod
    def from_json(cls, app: dash.Dash, name: str, path: str, data: dict):
        # create a list with only 2 columns from a dict
        list_obj = cls(app, name, path)
        list_obj.logger.debug(f"loading list {name} from dict")

        # reset index to column because the datatable does not use the index
        list_obj.add_entries(pd.DataFrame.from_dict(data, orient="index").reset_index(level=0))

        return list_obj

    @classmethod
    def from_save(cls, app: dash.Dash, save_json: dict, result_file_data):
        return cls.from_json(app, save_json["name"], save_json["path"], result_file_data)

    # properties

    @property
    def json(self) -> dict:
        json = {
            "type": "list",
            "name": self.name,
            "path": self.path,
        }

        return json

    # methods

    def add_entries(self, data: pd.DataFrame):
        self.entries = self.entries.append(data, ignore_index=True)

    # combine 2 lists
    def append(self, other: "List"):
        self.entries = self.entries.append(other.entries, ignore_index=True)

    def get_html(self):
        if not self.entries.empty:
            # self.logger.debug(f"list {self.name}, data\n{self.entries}")
            # TODO find a better way then this...
            # TODO add support for multi column
            table = dash_table.DataTable(data=self.entries.to_dict("records"),
                                         columns=[{"name": str(i), "id": str(i)} for i in self.entries.columns],
                                         style_as_list_view=True,
                                         style_cell={"textAlign": "right", "backgroundColor": self.fill_color,
                                                     "color": self.font_color, "font_size": f"{self.font_size}px"},
                                         style_cell_conditional=[
                                             {'if': {'column_id': self.entries.columns[0]}, 'textAlign': 'left'}],
                                         style_header={'display': 'none'},
                                         row_selectable=False)
        else:
            self.logger.warning(f"list {self.name}, is empty")
            table = html.P("No Data Available")
        return dbc.Col(
            [
                dbc.Card(
                    [
                        dbc.CardHeader(html.H4(self.name)),
                        dbc.CardBody(table, style={"width": "auto"})
                    ]
                )
            ],
            style={"padding": "10px", "min-width": "auto"}
        )
