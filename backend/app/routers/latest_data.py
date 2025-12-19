from fastapi import APIRouter, HTTPException # type: ignore
from ..services.run_pipeline import PipelineRunner
from ..schemas.stock import LatestDataResponse, LatestRawData
from app.core.logger import logger
from app.utils.time_utils import utc_now

router = APIRouter()
pipeline = PipelineRunner()

@router.get("/latest-data-snapshot")
def latest_data_snapshot():
    try:
        logger.info("Getting Engineered Data")
        df_APPL_new,df_TSLA_new,df_MSFT_new,df_NVDA_new, news_df = pipeline.fetch_latest()
        news_feat = pipeline.process_features( df_APPL_new,df_TSLA_new,df_MSFT_new,df_NVDA_new, news_df)
        news_feat = news_feat.tail(4)
        return LatestDataResponse(
            stocks=news_feat[["Close","Volume","Ticker","pol_mean","pol_sum","pos_count","neg_count","neu_count","has_news"]].to_dict(orient="records"),
            timestamp=utc_now()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/latest-data-feat")
def latest_data_feat():
    try:
        logger.info("Getting Engineered Data")
        df_APPL_new,df_TSLA_new,df_MSFT_new,df_NVDA_new, news_df = pipeline.fetch_latest()
        news_feat = pipeline.process_features( df_APPL_new,df_TSLA_new,df_MSFT_new,df_NVDA_new, news_df)
        news_feat = news_feat.tail(4)
        return LatestDataResponse(
            stocks=news_feat.to_dict(orient="records"),
            timestamp=utc_now()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/latest-data-raw")
def latest_data():
    try:
        logger.info("Getting Raw Data")
        df_APPL_new,df_TSLA_new,df_MSFT_new,df_NVDA_new, news_df = pipeline.fetch_latest()
        
        return LatestRawData(
            appl_stock=df_APPL_new.to_dict(orient="records")[-1],
            tsla_stock=df_TSLA_new.to_dict(orient="records")[-1],
            msft_stock=df_MSFT_new.to_dict(orient="records")[-1],
            nvda_stock=df_NVDA_new.to_dict(orient="records")[-1],
            news=news_df.to_dict(orient="records"),
            timestamp=utc_now()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))