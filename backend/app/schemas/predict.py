from pydantic import BaseModel #type: ignore
from typing import List, Any

class PredictionResponse(BaseModel):
    ticker: List[str]
    prediction: List[Any]
    model_version: str
    timestamp: str
