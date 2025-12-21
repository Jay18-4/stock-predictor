from fastapi import APIRouter, HTTPException # type: ignore
from app.services.run_pipeline import PipelineRunner
from app.schemas.sentiment import LatestNewsData
from app.core.logger import logger
from app.utils.time_utils import utc_now

router = APIRouter()
pipeline = PipelineRunner()

@router.get("/news-sentiment")
def news_sentiment():
    try:
        logger.info("Loading News Sentiment..")
        df_APPL_new,df_TSLA_new,df_MSFT_new,df_NVDA_new, news_df = pipeline.fetch_latest()
        news_sent = pipeline.process_features(df_APPL_new,df_TSLA_new,df_MSFT_new,df_NVDA_new, news_df)
        sent = news_sent.tail(4)[['Ticker','pol_mean', 'pol_sum','pos_count', 'neg_count', 'neu_count']]
        # return sent.to_dict()
        return LatestNewsData(
            news=sent.to_dict(orient="records"),
            timestamp=utc_now()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
@router.get("/news")
def news():
    try:
        logger.info("Loading News..")
        _,_,_,_, news_df = pipeline.fetch_latest()
        
        return LatestNewsData(
            news=news_df.to_dict(orient="records"),
            timestamp=utc_now()
            
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
