import logging
import pandas as pd
import dash
import plotly.graph_objects as go
from enum import Enum

from visual_quant.web_components.component import Component


# TODO this enum and reverse dict is ugly
class UnitType(Enum):
    DOLLAR = "$"
    PERCENT = "%"
    COUNT = "#"


to_unit = {
    "#": UnitType.COUNT,
    "$": UnitType.DOLLAR,
    "%": UnitType.PERCENT
}


# hold data for one series, a data line in a chart
class Series(Component):

    # constructors

    def __init__(self, app: dash.Dash, name: str, unit: UnitType, series_type: int, values: pd.DataFrame):
        # TODO create the path
        super().__init__(app, name, "")
        self.unit = unit
        self.series_type = series_type
        self.values = values  # the dataframe should contain the columns specified when calling get_figure

    # create the figure from the figure filed fount inside a chart field in the results json file
    @classmethod
    def from_json(cls, app: dash.Dash, series_json: dict):
        logger = logging.getLogger(__name__)
        name = series_json["Name"]

        try:
            df = pd.DataFrame.from_dict(series_json["Values"])
        except Exception as e:
            logger.error(f"no values found for series {name}. A series should contain a values field\n{e}")
            return None

        try:
            df["x"] = pd.to_datetime(df["x"], unit="s")
        except KeyError as e:
            logger.error(f"column x not found in the dataframe. columns are {df.columns}. {e}")

        return cls(app, name, to_unit[series_json["Unit"]], series_json["SeriesType"], df)

    # magic

    def __str__(self):
        return f"Series: {self.name}\n{self.values}\n"

    # properties

    @property
    def draw_mode(self) -> str:
        type_to_draw_mode = {
            0: "lines",
            1: "markers"
        }
        return type_to_draw_mode.get(self.series_type, "lines")  # the default drawing mode is lines

    # methods

    def get_figure(self, x_column_name: str = "x", y_column_name: str = "y") -> go.Scatter:

        # TODO change the color selection to be more flexible
        # for now make buy things green and sell things red...
        color = None
        if self.draw_mode == "markers":
            if "buy" in self.name.lower():
                color = "rgba(0, 255, 0, 255)"
            elif "sell" in self.name.lower():
                color = "rgba(255, 0, 0, 255)"

        try:
            x = self.values[x_column_name]
            y = self.values[y_column_name]
        except KeyError as e:
            self.logger.error(f"the columns x: {x_column_name} and/or y: {y_column_name} were not fount in the series data\n{e}")
            return None

        return go.Scatter(x=x, y=y, mode=self.draw_mode, name=self.name, marker_color=color)
