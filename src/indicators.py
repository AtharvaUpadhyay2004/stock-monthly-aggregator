import pandas as pd

def add_indicators(monthly: pd.DataFrame) -> pd.DataFrame:
    """Add SMA10/SMA20 and EMA10/EMA20 computed from monthly close per ticker."""
    monthly = monthly.sort_values(["ticker", "date"]).copy()

    def _calc(g: pd.DataFrame) -> pd.DataFrame:
        c = g["close"]
        g["sma_10"] = c.rolling(window=10, min_periods=10).mean()
        g["sma_20"] = c.rolling(window=20, min_periods=20).mean()
        # Standard recursive EMA when adjust=False
        g["ema_10"] = c.ewm(span=10, adjust=False).mean()
        g["ema_20"] = c.ewm(span=20, adjust=False).mean()
        return g

    return monthly.groupby("ticker", group_keys=False).apply(_calc)
