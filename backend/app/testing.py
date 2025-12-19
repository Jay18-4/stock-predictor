import yfinance as yf
import pandas as pd
from datetime import date, timedelta
from pydantic import BaseModel # type: ignore
from typing import Dict, Any, List
import requests, time
from datetime import datetime, timedelta, date
from pathlib import Path

MODEL_PATH = Path(__file__).resolve().parent.parent.parent.parent / "models" / "lstm.h5"

# today = date.today()
# yesterday = today - timedelta(days=1)
# ticker = ["AAPL","TSLA","MSFT","NVDA"] 
# stock_price = []
# for i in ticker:
#     data = yf.download(i, period="1d", auto_adjust=True,multi_level_index=False)
#     # data = data.head(1)
#     data["Ticker"] = i
#     stock_price.append(data)

print(MODEL_PATH)