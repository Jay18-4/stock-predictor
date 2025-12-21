import os
import pandas as pd
from datetime import date
from app.core.logger import logger
from app.services.run_pipeline import PipelineRunner
from pathlib import Path

pipeline = PipelineRunner()

model_version = pipeline.get_model_version()
# HISTORY_PATH = rf"app/services/pipeline/data/prediction_history{model_version}_by_{date.today()}.csv"
HISTORY_PATH = Path(__file__).resolve().parent.parent.parent / "data" / f"prediction_history_{model_version}.csv"


# Ensure directory exists
os.makedirs("data", exist_ok=True)

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
    
    df.to_csv(HISTORY_PATH, index=False)
    # if not os.path.exists(HISTORY_PATH):
    #     df = pd.DataFrame([record])
    #     df.to_csv(HISTORY_PATH, index=False)
    # else:
    #     df = pd.DataFrame([record])
    #     df.to_csv(HISTORY_PATH, mode="a", header=False, index=False)


def get_history(ticker: str | None = None):
    """Return prediction history filtered by ticker (if provided)."""

    if not os.path.exists(HISTORY_PATH):
        return []

    df = pd.read_csv(HISTORY_PATH)

    if ticker.upper() in df["ticker"].to_list():
        df = df[df["ticker"] == ticker.upper()]

    # Clean return format
    return df
