import numpy as np
from pandas import DataFrame

from buffett.common.pendelum import DateTime, Duration
from buffett.constants.meta import META_COLS


def tuple_to_array(tup: tuple) -> np.array:
    arr = np.array(tup)
    arr = np.reshape(arr, (-1, len(tup)))
    return arr


def get_now_shift(du: Duration, minus=False) -> DateTime:
    now = DateTime.now()
    if minus:
        return now - du
    return now + du


def create_meta(meta_list: list) -> DataFrame:
    return DataFrame(data=meta_list, columns=META_COLS)


def dataframe_is_valid(df: DataFrame) -> bool:
    return isinstance(df, DataFrame) and not df.empty


def dataframe_not_valid(df: DataFrame) -> bool:
    return not isinstance(df, DataFrame) or df.empty