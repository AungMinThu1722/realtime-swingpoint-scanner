from __future__ import annotations

import pandas as pd


def _clean(df: pd.DataFrame) -> pd.DataFrame:
    renamed = df.copy()
    renamed.columns = [c.lower() for c in renamed.columns]
    return renamed


def detect_seek_and_destroy(df: pd.DataFrame, tolerance: float = 0.0, min_sweep: float = 0.0) -> pd.Series:
    """
    Vectorized Seek and Destroy detection.

    Rules (c2 vs c1):
    - c2.high > c1.high + tolerance
    - c2.low < c1.low - tolerance
    - (c2.high - c1.high) > min_sweep
    - (c1.low - c2.low) > min_sweep
    - c2.close inside c1 range
    """
    if df is None or len(df) == 0:
        return pd.Series(dtype=bool)

    data = _clean(df)
    c2 = data
    c1 = data.shift(1)

    cond = (
        (c2["high"] > c1["high"] + tolerance)
        & (c2["low"] < c1["low"] - tolerance)
        & ((c2["high"] - c1["high"]) > min_sweep)
        & ((c1["low"] - c2["low"]) > min_sweep)
        & c2["close"].between(c1["low"], c1["high"])
    )

    cond.iloc[0] = False
    return cond.fillna(False)
