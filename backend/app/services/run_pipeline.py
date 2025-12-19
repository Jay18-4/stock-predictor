import json
from datetime import date
from app.core.logger import logger
from pathlib import Path

from .pipeline import (
    fetch_data,
    feature_engineering,
    sentiment_analysis,
    news_feat_eng,
    model
)

class PipelineRunner:
    logger.info("Preparing features for prediction...")
    def fetch_latest(self):
        df_APPL_new,df_TSLA_new,df_MSFT_new,df_NVDA_new = fetch_data.fetch_stock()
        news_df = fetch_data.news_arrange()
        # news_df = {'1':'yes','2':'NO','3':'OH','4':'YIPP'}
        return df_APPL_new,df_TSLA_new,df_MSFT_new,df_NVDA_new, news_df

    def process_features(self, df_APPL_new,df_TSLA_new,df_MSFT_new,df_NVDA_new, news_df):
        stock_feat = feature_engineering.feat_eng(df_APPL_new,df_TSLA_new,df_MSFT_new,df_NVDA_new)
        news_sent = sentiment_analysis.tf_news_sentiment(news_df)
        news_feat = news_feat_eng.news_feat_engine(stock_feat, news_sent)
        return news_feat

    def predict(self, news_feat):
        pred = model.predict(news_feat)
        model.store_next_week(news_feat)
        return pred

    def retrain_weekly(self, news_feat):
        model.retrain(news_feat)

    def get_model_version(self):
        path = Path(__file__).resolve().parent.parent.parent / "data" / "model_version.json"
        # path = "app/services/pipeline/data/model_version.json"
        with open(path) as f:
            data = json.load(f)
        return data["version"]