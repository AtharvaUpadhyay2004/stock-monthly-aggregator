from dataclasses import dataclass

DEFAULT_TICKERS = ["AAPL", "AMD", "AMZN", "AVGO", "CSCO", "MSFT", "NFLX", "PEP", "TMUS", "TSLA"]

@dataclass(frozen=True)
class Config:
    input_csv: str
    output_dir: str = "output"
    tickers: list[str] | None = None  # if None, keep all tickers in input
    # Pandas is deprecating 'M' alias; use month-end 'ME'
    resample_rule: str = "M"
