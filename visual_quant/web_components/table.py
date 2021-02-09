import dash
import dash_table
import pandas as pd
import dash_html_components as html
import dash_bootstrap_components as dbc

from visual_quant.web_components.component import Component


# hold a list (or table) of information and render using dash datatable
# consider splitting the 2 behaviors in subclasses
class Table(Component):

    # constructors

    def __init__(self, app: dash.Dash, name: str, path: str, direction: str = "vertical", alignment="left", font_size=17, font_color="rgba(200, 200, 200, 255)", fill_color="rgba(0, 0, 0, 0)"):
        super().__init__(app, name, path)
        self.entries = pd.DataFrame()

        # TODO base color on theme directly
        self.direction = direction
        self.alignment = alignment
        self.font_size = font_size
        self.font_color = font_color
        self.fill_color = fill_color

    @classmethod
    def from_json(cls, app: dash.Dash, name: str, path: str, data: list, collapse: dict = None):
        # horizontal dict with n columns from list
        list_obj = cls(app, name, path, direction="horizontal")
        list_obj.logger.debug(f"loading list {name} from list")

        # if there are entries that a dicts themselves like the Symbol field
        # provide the option to collapse them and use one of their values in the list
        if collapse is not None:
            for entry in data:
                for key in collapse:
                    if key in entry:
                        data[data.index(entry)][key] = entry[key][collapse[key]]

            if any([type(x) is dict for x in entry.values()]):
                list_obj.logger.warning(
                    f"a dict in the list {name} contains another dict. The dicts in the list should only contain int, float or str, you can collapse dicts to one entry.")

        list_obj.add_entries(pd.DataFrame.from_records(data))

        return list_obj

    @classmethod
    def from_save(cls, app: dash.Dash, save_json: dict, result_file_data):
        return cls.from_json(app, save_json["name"], save_json["path"], result_file_data)

    # properties

    @property
    def json(self) -> dict:
        json = {
            "type": "table",
            "name": self.name,
            "path": self.path,
        }

        return json

    # methods

    def add_entries(self, data: pd.DataFrame):
        self.entries = self.entries.append(data, ignore_index=True)

    # combine 2 lists
    def append(self, other: "Table"):
        self.entries = self.entries.append(other.entries, ignore_index=True)

    def get_html(self):
        if not self.entries.empty:
            # self.logger.debug(f"list {self.name}, data\n{self.entries}")
            # TODO find a better way then this...
            # TODO add support for multi column
            table = dash_table.DataTable(data=self.entries.to_dict("records"),
                                         columns=[{"name": str(i), "id": str(i)} for i in self.entries.columns],
                                         style_as_list_view=False,
                                         style_cell={"textAlign": "right", "backgroundColor": self.fill_color,
                                                     "color": self.font_color, "font_size": f"{self.font_size}px"},
                                         style_cell_conditional=[
                                             {'if': {'column_id': self.entries.columns[0]}, 'textAlign': 'left'}],
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
