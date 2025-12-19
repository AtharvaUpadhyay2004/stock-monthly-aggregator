import pandas as pd

REQUIRED_COLS = {"date", "volume", "open", "high", "low", "close", "adjclose", "ticker"}

def load_prices(path: str) -> pd.DataFrame:
    """Load the input CSV and ensure required columns and ordering."""
    df = pd.read_csv(path)
    missing = REQUIRED_COLS - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    df["date"] = pd.to_datetime(df["date"], errors="raise")
    df = df.sort_values(["ticker", "date"]).reset_index(drop=True)
    return df
