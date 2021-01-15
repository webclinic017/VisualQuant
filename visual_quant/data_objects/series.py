import logging
import pandas as pd
import dash_core_components as dcc
import plotly.graph_objects as go

from enum import Enum


class UnitType(Enum):
    DOLLAR = "$"
    PERCENT = "%"
    COUNT = "#"


to_unit = {
    "#": UnitType.COUNT,
    "$": UnitType.DOLLAR,
    "%": UnitType.PERCENT
}


class Series:
    name = ""
    values = None
    unit = None
    type = -1
    color = None

    def __init__(self):
        pass

    @classmethod
    def from_data(cls, name: str, unit: UnitType, type: int, values: pd.DataFrame):
        obj = cls()
        obj.name = name
        obj.values = values
        obj.unit = unit
        obj.type = type
        return obj

    @classmethod
    def from_json(cls, series_json: dict):
        logger = logging.getLogger(__name__)
        name = series_json["Name"]

        try:
            df = pd.DataFrame.from_dict(series_json["Values"])
        except Exception as e:
            logger.error(f"Values not found in Chart {name}")
            return None

        df["x"] = pd.to_datetime(df["x"], unit="s")

        return cls.from_data(name, to_unit[series_json["Unit"]], series_json["SeriesType"], df)

    @property
    def draw_mode(self):
        type_to_draw_mode = {
            0: "lines",
            1: "markers"
        }
        return type_to_draw_mode.get(self.type, "lines")

    def __str__(self):
        return f"Series: {self.name}\n{self.values}\n"

    def get_figure(self, x="x", y="y"):
        return go.Scatter(x=self.values[x], y=self.values[y], mode=self.draw_mode, name=self.name)
