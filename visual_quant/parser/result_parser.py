import json
import logging
import pandas as pd

from visual_quant.data_objects.series import Series, UnitType
from visual_quant.data_objects.chart import Chart

to_unit = {
    "#": UnitType.COUNT,
    "$": UnitType.DOLLAR,
    "%": UnitType.PERCENT
}


def get_series():
    pass


def get_chart(result_path: str, chart_name: str):

    logger = logging.getLogger(__name__)

    with open(result_path, "r") as f:
        config = json.load(f)

    try:
        plot_json = config["Charts"][chart_name]
    except KeyError as e:
        logger.error(f"did not find chart named: {chart_name}\n{e}")
        return

    if plot_json["Name"] != chart_name:
        logger.error(f"The plot name requested did not match the plot name from the file. ({chart_name})")
        return

    try:
        series_json = plot_json["Series"]
    except KeyError as e:
        logger.error(f"No Files named Series found in Chart {chart_name}")

    series = []
    for s in series_json:
        s = series_json[s]
        df = pd.DataFrame.from_dict(s["Values"])
        df.set_index(pd.to_datetime(df["x"], unit="s"), inplace=True)
        df.drop("x", axis=1, inplace=True)
        series.append(Series.from_data(s["Name"], to_unit[s["Unit"]], s["SeriesType"], df))

    return Chart.from_series(chart_name, series)

