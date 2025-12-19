# Stock Monthly Aggregator (Pandas Only)

## What this does
- Reads daily stock OHLCV data (10 tickers, ~2 years)
- Aggregates to monthly OHLC per ticker:
  - **Open** = first trading day open in the month
  - **Close** = last trading day close in the month
  - **High** = maximum high in the month
  - **Low** = minimum low in the month
- Computes indicators from **monthly close**:
  - SMA 10, SMA 20
  - EMA 10, EMA 20
- Writes `output/result_{TICKER}.csv` for each ticker (24 rows each)

## Input schema
CSV columns:
`date,volume,open,high,low,close,adjclose,ticker`

Tickers:
`AAPL,AMD,AMZN,AVGO,CSCO,MSFT,NFLX,PEP,TMUS,TSLA`

## Assumptions
1. Dataset contains at least **24 monthly bars** per ticker.
2. Monthly bars are aligned to **month-end** timestamps (pandas resample rule `ME`).
3. If more than 24 months exist, the pipeline keeps the **last 24 months** per ticker.
4. SMA needs a full window:
   - SMA10 is NaN for first 9 months
   - SMA20 is NaN for first 19 months

## Setup
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run
Put your CSV at `data/input.csv` (or pass any path):
```bash
python -m src.main --input data/input.csv --output-dir output
```

Outputs:
- `output/result_AAPL.csv`
- ...
- `output/result_TSLA.csv`

## Notes
- Uses only Pandas (no TA libraries).
- OHLC logic uses first/last snapshots (not averages).
