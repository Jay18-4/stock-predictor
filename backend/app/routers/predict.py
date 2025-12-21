from fastapi import APIRouter, HTTPException # type: ignore

from app.services.run_pipeline import PipelineRunner
from app.schemas.predict import PredictionResponse
from app.services.history_store import save_history_record
from app.core.logger import logger
from app.utils.time_utils import utc_now

router = APIRouter()
pipeline = PipelineRunner()

@router.get("/predict", response_model=PredictionResponse)
def predict_endpoint():
    try:
        print('STARTING...')
        logger.info("Predicting Target...")
        df_APPL_new,df_TSLA_new,df_MSFT_new,df_NVDA_new, news_df = pipeline.fetch_latest()
        print("DONE WITH DATA FETCHING!!")
        news_feat = pipeline.process_features( df_APPL_new,df_TSLA_new,df_MSFT_new,df_NVDA_new, news_df)
        print("DONE WITH news_feat!!")
        tickers = news_feat.tail(4)['Ticker'].to_list()
        print("DONE WITH TICKERS!!")
        pred = pipeline.predict(news_feat)
        print("DONE WITH PREDICTION!!")
        version = pipeline.get_model_version()
        print("DONE WITH VERSION!!")
        
        
        # Save to history
        save_history_record(
            ticker=tickers,
            prediction=pred,
            actual_price=None,  # you can fill this later when actual price arrives
            timestamp=utc_now()
        )
        print(f'Predictions: {pred}')
        return PredictionResponse(
            ticker=tickers,
            prediction=pred,
            model_version=version,
            timestamp=utc_now()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/model_version", response_model=PredictionResponse)
def model_version_endpoint():
    try:
        return pipeline.get_model_version()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
