# src/transform.py
from __future__ import annotations

import pandas as pd
from pandas.tseries.frequencies import to_offset


def _normalize_rule(rule: str) -> str:
    """
    Pandas compatibility:
    - Some versions accept "ME" (month-end), some don't.
    - If "ME" isn't supported, fall back to "M".
    """
    try:
        to_offset(rule)
        return rule
    except ValueError:
        if rule == "ME":
            return "M"
        raise


def daily_to_monthly_ohlc(df: pd.DataFrame, rule: str = "ME") -> pd.DataFrame:
    """
    Converts daily data to monthly OHLCV per ticker.

    Monthly aggregation:
      - open     = first open in month
      - close    = last close in month
      - high     = max high in month
      - low      = min low in month
      - volume   = sum volume in month
      - adjclose = last adjclose in month
    """
    rule = _normalize_rule(rule)

    dfx = df.copy()

    # Ensure datetime
    dfx["date"] = pd.to_datetime(dfx["date"], errors="coerce")
    if dfx["date"].isna().any():
        bad = dfx[dfx["date"].isna()].head(5)
        raise ValueError(f"Some 'date' values could not be parsed. Example rows:\n{bad}")

    # Important: DO NOT use group_keys=False here, it can drop 'ticker' in the result
    monthly = (
        dfx.set_index("date")
           .sort_values(["ticker"])  # stable grouping (optional but fine)
           .groupby("ticker")
           .resample(rule)
           .agg(
               open=("open", "first"),
               high=("high", "max"),
               low=("low", "min"),
               close=("close", "last"),
               adjclose=("adjclose", "last"),
               volume=("volume", "sum"),
           )
           .reset_index()
    )

    # Remove empty months (if any)
    monthly = monthly.dropna(subset=["open", "high", "low", "close"], how="any")

    # Consistent ordering
    monthly = monthly.sort_values(["ticker", "date"]).reset_index(drop=True)

    return monthly
