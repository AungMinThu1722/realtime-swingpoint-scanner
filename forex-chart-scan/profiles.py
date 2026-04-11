from __future__ import annotations

import pandas as pd


def _clean(df: pd.DataFrame) -> pd.DataFrame:
    renamed = df.copy()
    renamed.columns = [c.lower() for c in renamed.columns]
    return renamed


def detect_aim_for_range_low(df: pd.DataFrame, min_sweep: float = 0.0) -> pd.Series:
    if df is None or len(df) == 0:
        return pd.Series(dtype=bool)
    data = _clean(df)
    c2 = data
    c1 = data.shift(1)

    cond = (
        (c2["high"] > c1["high"])
        & c2["close"].between(c1["low"], c1["high"])
        & ((c2["high"] - c1["high"]) > min_sweep)
    )

    cond.iloc[0] = False
    return cond.fillna(False)


def detect_aim_for_range_high(df: pd.DataFrame, min_sweep: float = 0.0) -> pd.Series:
    if df is None or len(df) == 0:
        return pd.Series(dtype=bool)
    data = _clean(df)
    c2 = data
    c1 = data.shift(1)

    cond = (
        (c2["low"] < c1["low"])
        & c2["close"].between(c1["low"], c1["high"])
        & ((c1["low"] - c2["low"]) > min_sweep)
    )

    cond.iloc[0] = False
    return cond.fillna(False)
