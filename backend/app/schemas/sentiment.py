from pydantic import BaseModel #type: ignore
from typing import Dict, Any, List

class LatestNewsData(BaseModel):
    news: List[Dict[str, Any]]
    timestamp: str