from pydantic import BaseModel # type: ignore
from typing import List

class HistoryRecord(BaseModel):
    timestamp: str | list[str]
    tickers: str | list[str]
    prediction: int | List[int]
    model_version: str

