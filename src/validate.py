import pandas as pd

def enforce_exact_months(monthly: pd.DataFrame, months: int = 24) -> pd.DataFrame:
    """
    Ensure each ticker has at least N months, then keep the last N months.
    Raises if any ticker has fewer than N.
    """
    monthly = monthly.sort_values(["ticker", "date"]).copy()

    def _last_n(g: pd.DataFrame) -> pd.DataFrame:
        t = g["ticker"].iloc[0]
        if len(g) < months:
            raise ValueError(f"Ticker {t} has only {len(g)} monthly rows; expected at least {months}.")
        return g.tail(months)

    return monthly.groupby("ticker", group_keys=False).apply(_last_n)


def assert_output_shape(monthly_exact: pd.DataFrame, months: int = 24) -> None:
    counts = monthly_exact.groupby("ticker").size()
    bad = counts[counts != months]
    if not bad.empty:
        raise AssertionError(f"Bad month counts:\n{bad}")
