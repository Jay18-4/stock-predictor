import pandas as pd
import numpy as np
from app.core.logger import logger
from pathlib import Path

from sklearn.preprocessing import MinMaxScaler
import joblib
# import fetch_data
# df_APPL_new, df_TSLA_new, df_MSFT_new, df_NVDA_new = fetch_data.fetch_stock()

def feat_eng(df_APPL_new, df_TSLA_new, df_MSFT_new, df_NVDA_new):
    logger.info("Engineering Features")
    
    data_folder = Path(__file__).resolve().parent.parent.parent.parent / "data" 
    df_APPL_old = pd.read_csv(f'{data_folder}/clean_AAPL_stock_data.csv')
    df_TSLA_old = pd.read_csv(f'{data_folder}/clean_TSLA_stock_data.csv')
    df_MSFT_old = pd.read_csv(f'{data_folder}/clean_MSFT_stock_data.csv')
    df_NVDA_old = pd.read_csv(f'{data_folder}/clean_NVDA_stock_data.csv')

    df_APPL = pd.concat([df_APPL_old,df_APPL_new], axis=0, ignore_index=True)
    df_TSLA = pd.concat([df_TSLA_old,df_TSLA_new], axis=0, ignore_index=True)
    df_MSFT = pd.concat([df_MSFT_old,df_MSFT_new], axis=0, ignore_index=True)
    df_NVDA = pd.concat([df_NVDA_old,df_NVDA_new], axis=0, ignore_index=True)
    stock_datasets = [df_APPL,df_TSLA,df_MSFT,df_NVDA]
    for df in stock_datasets:
        df['Target'] = (df['Close'].shift(-1) > df['Close']).astype(int)

    for df in stock_datasets:
        df['RAV'] = df.groupby('Ticker')['Volume'].transform(lambda x: x.rolling(7).mean())
        df['volatility'] = df.groupby('Ticker')['Close'].transform(lambda x: x.rolling(20).std())
        df["Buy_Sell_Strength"] = (df["Close"]-df["Low"]) / (df["High"] - df["Low"])
        df["Weighted_Strength"] = (df["Buy_Sell_Strength"] - 0.5) * (df["Volume"]/ df["RAV"])
        df["Trend"] = (df["Buy_Sell_Strength"] - 0.5).rolling(25).mean()
        df["Returns"] = df["Close"].pct_change()
        df["Log_returns"] = (df["Close"] / df["Close"].shift(1).apply(np.log))
        df.dropna(inplace=True)
        
    interleaved_df = pd.concat(stock_datasets).sort_index(kind='merge').reset_index(drop=True)
    
    df_dummies = pd.get_dummies(data=interleaved_df["Ticker"])

    final_stocks_df =  pd.concat([interleaved_df,df_dummies],axis=1)

    final_stocks_df['market_return'] = final_stocks_df.groupby('date')['Returns'].transform('mean')
    final_stocks_df['rel_return'] = final_stocks_df['Returns'] - final_stocks_df['market_return']
    final_stocks_df['mean_return_others'] = final_stocks_df.groupby('date')['Returns'].transform(lambda x: x.mean())
    final_stocks_df['divergence'] = (final_stocks_df['Returns'] - final_stocks_df['mean_return_others']).abs()
    final_stocks_df['volume_rank'] = final_stocks_df.groupby('date')['Volume'].rank(pct=True)
    final_stocks_df['return_rank'] = final_stocks_df.groupby('date')['Returns'].rank(pct=True)
    final_stocks_df['market_std'] = final_stocks_df.groupby('date')['Returns'].transform('std')
    final_stocks_df['zscore_vs_market'] = (final_stocks_df['Returns'] - final_stocks_df['market_return']) / final_stocks_df['market_std']


    
    
    return final_stocks_df



print('DONE!!')


#change df structure get them individually hte do the interlevened data again