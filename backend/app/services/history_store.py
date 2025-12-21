import os
import pandas as pd
from datetime import date
from pathlib import Path

from app.core.logger import logger
from app.services.run_pipeline import PipelineRunner
from app.storage import read_csv, write_csv

pipeline = PipelineRunner()

model_version = pipeline.get_model_version()
# for local version
# HISTORY_PATH = Path(__file__).resolve().parent.parent.parent / "data" / f"prediction_history_{model_version}.csv"


# Ensure directory exists
# os.makedirs("data", exist_ok=True)

# Define consistent columns
COLUMNS = ["ticker", "predicted_price", "actual_price"]

def save_history_record(ticker: list, prediction: list,
                        actual_price: list | None, timestamp
                        ):
    """Append a new prediction result into the CSV history file."""
    old_df = pd.read_csv(HISTORY_PATH)

    record = {
        "ticker": ticker,
        "prediction": prediction,
        "actual_price": actual_price,
        'timestamp': timestamp
    }

    logger.info(f"Saving new history record for tickers: {record['ticker']}")
    
    # If file doesn't exist, create it with header
    df = pd.DataFrame(record)
    
    df = pd.concat([old_df,df], axis=0,ignore_index=True)
    
    write_csv(df, f"prediction_history_{model_version}.csv")
   


def get_history(ticker: str | None = None):
    """Return prediction history filtered by ticker (if provided)."""

    df = read_csv(f"prediction_history_{model_version}.csv")

    if df.empty:
        return []

    if ticker.upper() in df["ticker"].to_list():
        df = df[df["ticker"] == ticker.upper()]

    # Clean return format
    return df
