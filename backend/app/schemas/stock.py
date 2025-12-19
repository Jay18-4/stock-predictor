from pydantic import BaseModel # type: ignore
from typing import Dict, Any, List

class LatestRawData(BaseModel):
    appl_stock: Dict[str, Any]
    tsla_stock: Dict[str, Any]
    msft_stock: Dict[str, Any]
    nvda_stock: Dict[str, Any]
    timestamp: str 

class LatestDataResponse(BaseModel):
    stocks: List[Dict[str, Any]]
    timestamp: str    # raw news items with ticker field
