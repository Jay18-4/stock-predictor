from fastapi import APIRouter, HTTPException # type: ignore

from app.services.history_store import get_history
from app.schemas.history import HistoryRecord
# from app.core.logger import logger
from app.utils.time_utils import utc_now
from app.services.run_pipeline import PipelineRunner
import logging
logger = logging.getLogger(__name__)

pipeline = PipelineRunner()
router = APIRouter()

@router.get("/history")
def prediction_history(ticker: str):
    try:
        model_version = pipeline.get_model_version()
        logger.info("Getting History...")
        df = get_history(ticker)
        
        
        if type(df) == type([]):
            return df
        
        
        ticker = df['ticker'].to_list()
        pred = df['prediction'].to_list()
        time = df['timestamp'].to_list()
        
        return HistoryRecord(
            timestamp=time,
            tickers= ticker,
            prediction=pred,
            model_version=model_version
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
