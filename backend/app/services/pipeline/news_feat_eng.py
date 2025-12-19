import pandas as pd
from app.core.logger import logger

# import feature_engineering
# import sentiment_analysis 

# final_stocks_df = feature_engineering.feat_eng()
# news_sentiment = sentiment_analysis.tf_news_sentiment()

def compute_polarity(row):
    if row['sentiment'] == 'positive':
        return row['score'] * 1.0
    elif row['sentiment'] == 'neutral':
        return row['score'] * 0.5
    else:  # negative
        return row['score'] * 0.0

def news_feat_engine(final_stocks_df,news_sentiment):
    logger.info("Engeering News Features")
    news_sentiment['sentiment_polarity'] = news_sentiment.apply(compute_polarity, axis=1)
    df_dummies = pd.get_dummies(news_sentiment['sentiment'])

    df_news_sent = pd.concat([news_sentiment,df_dummies],axis=1)
    df_news_sent = df_news_sent.drop("sentiment",axis=1)
    df_news_sent.rename(columns={'negative':'sentiment_neg', 'neutral':'sentiment_neu','positive':'sentiment_pos'},inplace=True)
    df_news_sent = df_news_sent[['date','sentiment_polarity','sentiment_neg','sentiment_neu','sentiment_pos']]

    df_news_sent["datetime"] =  pd.to_datetime(df_news_sent['date'], format="mixed", utc=True)
    df_news_sent = df_news_sent.set_index('datetime').sort_index()

    df_news_sent['date'] = df_news_sent.index.date
    df_news_sent['date'] = pd.to_datetime(df_news_sent['date'])

    final_stocks_df['date'] = pd.to_datetime(final_stocks_df['date']) 
    stocks_df = final_stocks_df.set_index('date').sort_index()


    daily_sentiment = (
        df_news_sent.groupby('date')
        .agg({
            'sentiment_polarity': ['mean', 'sum'],  # overall sentiment per day
            'sentiment_pos': 'sum',
            'sentiment_neg': 'sum',
            'sentiment_neu': 'sum'
        })
    )
    daily_sentiment.columns = [
        'pol_mean', 'pol_sum',
        'pos_count', 'neg_count', 'neu_count'
    ]

    stock_with_sentiment = stocks_df.merge(
        daily_sentiment,
        left_index=True,
        right_index=True,
        how="left"
    )
    stock_with_sentiment['has_news'] = (~stock_with_sentiment['pol_mean'].isna()).astype(int)
    sentiment_cols = ['pol_mean','pol_sum','pos_count','neg_count','neu_count'] 
    stock_with_sentiment[sentiment_cols] = stock_with_sentiment[sentiment_cols].fillna(0)

    return stock_with_sentiment
