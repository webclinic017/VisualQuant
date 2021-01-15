import logging
import pandas as pd
import dash_core_components as dcc

from enum import Enum


class UnitType(Enum):
    DOLLAR = "$"
    PERCENT = "%"
    COUNT = "#"


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

    def __str__(self):
        return f"Series: {self.name}\n{self.values}\n"
