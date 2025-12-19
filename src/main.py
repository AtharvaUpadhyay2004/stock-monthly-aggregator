import argparse
import os

from .config import Config, DEFAULT_TICKERS
from .io_utils import load_prices
from .transform import daily_to_monthly_ohlc
from .indicators import add_indicators
from .validate import enforce_exact_months, assert_output_shape


def write_partitioned_csvs(monthly: 'os.PathLike | str', output_dir: str) -> None:
    os.makedirs(output_dir, exist_ok=True)

    cols = [
        "date", "ticker",
        "open", "high", "low", "close",
        "sma_10", "sma_20", "ema_10", "ema_20",
        "volume", "adjclose",
    ]

    for ticker, g in monthly.groupby("ticker"):
        out_path = os.path.join(output_dir, f"result_{ticker}.csv")
        g[cols].to_csv(out_path, index=False)


def run(cfg: Config) -> None:
    df = load_prices(cfg.input_csv)

    if cfg.tickers is not None:
        df = df[df["ticker"].isin(cfg.tickers)].copy()

    monthly = daily_to_monthly_ohlc(df, rule=cfg.resample_rule)
    monthly = add_indicators(monthly)
    monthly = enforce_exact_months(monthly, months=24)
    assert_output_shape(monthly, months=24)

    write_partitioned_csvs(monthly, cfg.output_dir)
    print(f"✅ Done. Wrote {monthly['ticker'].nunique()} files to: {cfg.output_dir}/")


def parse_args():
    p = argparse.ArgumentParser(description="Daily → Monthly OHLC + SMA/EMA (Pandas only)")
    p.add_argument("--input", required=True, help="Path to input CSV")
    p.add_argument("--output-dir", default="output", help="Folder to store result_{TICKER}.csv")
    p.add_argument(
        "--tickers",
        default=",".join(DEFAULT_TICKERS),
        help="Comma-separated tickers (default = assignment tickers)",
    )
    return p.parse_args()


def main():
    args = parse_args()
    tickers = [t.strip() for t in args.tickers.split(",") if t.strip()]
    cfg = Config(input_csv=args.input, output_dir=args.output_dir, tickers=tickers)
    run(cfg)


if __name__ == "__main__":
    main()
