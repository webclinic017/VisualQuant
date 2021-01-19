import logging
import pandas as pd
import dash
import plotly.graph_objects as go
from enum import Enum

from visual_quant.components.component import Component


class UnitType(Enum):
    DOLLAR = "$"
    PERCENT = "%"
    COUNT = "#"


to_unit = {
    "#": UnitType.COUNT,
    "$": UnitType.DOLLAR,
    "%": UnitType.PERCENT
}


class Series(Component):

    def __init__(self, app: dash.Dash, name: str, unit: UnitType, series_type: int, values: pd.DataFrame):
        super().__init__(app, name, class_names=["series", name])
        self.unit = unit
        self.series_type = series_type
        self.values = values

    @classmethod
    def from_json(cls, app, series_json: dict):
        logger = logging.getLogger(__name__)
        name = series_json["Name"]

        try:
            df = pd.DataFrame.from_dict(series_json["Values"])
        except Exception as e:
            logger.error(f"Values not found in Chart {name}")
            return None

        df["x"] = pd.to_datetime(df["x"], unit="s")

        return cls(app, name, to_unit[series_json["Unit"]], series_json["SeriesType"], df)

    @property
    def draw_mode(self):
        type_to_draw_mode = {
            0: "lines",
            1: "markers"
        }
        return type_to_draw_mode.get(self.series_type, "lines")

    def __str__(self):
        return f"Series: {self.name}\n{self.values}\n"

    def get_figure(self, x="x", y="y"):
        color = None
        if self.draw_mode == "markers":
            if "buy" in self.name.lower():
                color = "rgba(0, 255, 0, 255)"
            elif "sell" in self.name.lower():
                color = "rgba(255, 0, 0, 255)"
        return go.Scatter(x=self.values[x], y=self.values[y], mode=self.draw_mode, name=self.name, marker_color=color)
