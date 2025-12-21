import json
from datetime import date
from pathlib import Path

from app.core.logger import logger
from app.storage import read_json, write_json

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

    def retrain_weekly(self):
        df = model.get_historical_data()
        new_week_df = model.get_new_week_daata()
        model.retrain(df, new_week_df)

    def get_model_version(self):
        #LOCAL VERSION
        # path = Path(__file__).resolve().parent.parent.parent / "data" / "model_version.json"
        # path = "app/services/pipeline/data/model_version.json"
        # with open(path) as f:
        #     data = json.load(f)
        data = read_json("model_version.json")
        return data["version"]
