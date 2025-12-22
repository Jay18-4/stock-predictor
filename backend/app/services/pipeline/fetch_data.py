import yfinance as yf
import pandas as pd
import requests, time
from datetime import datetime, timedelta
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
# from app.core.logger import logger
import logging
logger = logging.getLogger(__name__)

#STOCK
def fetch_stock():
    ticker = ["AAPL","TSLA","MSFT","NVDA"] 
    stock_price = []
    for i in ticker:
        logger.info(f"Fetching stock data for {i}")
        data = yf.download(i, period="1d", auto_adjust=True,multi_level_index=False)
        data["Ticker"] = i
        stock_price.append(data)

    df_APPL_new = stock_price[0]
    df_TSLA_new = stock_price[1]
    df_MSFT_new = stock_price[2]
    df_NVDA_new = stock_price[3]

    for df in [df_APPL_new,df_TSLA_new,df_MSFT_new,df_NVDA_new]:
        df['date'] = df.index.date
        
    return df_APPL_new,df_TSLA_new,df_MSFT_new,df_NVDA_new

def latest_stock():
    df_APPL_new,df_TSLA_new,df_MSFT_new,df_NVDA_new = fetch_stock()
    latest_stock_df = pd.concat([df_APPL_new,df_TSLA_new,df_MSFT_new,df_NVDA_new], axis=1,ignore_index=True)
    
    return latest_stock_df


#NEWS 
def translate(text):
    model_path = "C:/huggingface_cache/opus-mt-mul-en"
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_path)
    
    inputs = tokenizer(text, return_tensors="pt")
    outputs = model.generate(**inputs)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

 
def get_news_data(company,ticker):
    logger.info(f"Fetching stock data for {ticker}")
    url = "https://api.gdeltproject.org/api/v2/doc/doc"
    
                
    # Get the current UTC time (GDELT uses UTC)
    now = datetime.now()

    # 24 hours ago
    yesterday = now - timedelta(days=1)

    params = {
        "query": company,
        "mode": "ArtList",
        "maxrecords": "200",
        "format": "json",
        "startdatetime": yesterday.strftime("%Y%m%d%H%M%S"),
        "enddatetime": now.strftime("%Y%m%d%H%M%S")
    }
    
    headers = {"User-Agent": "Mozilla/5.0"}
    time.sleep(2)
    
    response = requests.get(url, params=params, headers=headers)
    print(response.status_code)
    data = response.json().get('articles', [])
    df = pd.DataFrame(data)[['seendate','title','language']]
    df['date'] = pd.to_datetime(df['seendate'], errors='coerce')
    df['Ticker'] = ticker
    df.drop('seendate', axis=1,inplace=True)
    df.sort_values(by='date',inplace=True)
    return df
    
def translate_news(df,company):
    english_df = df[df['language'] == 'English']
    non_english_df = df[df['language'] != 'English']
    
    percentage = (len(non_english_df)/len(df)) * 100
    print(f'Number of Non English for {company}: {len(non_english_df)} Which Is {percentage}% of the df')
    # if len(non_english_df) > (len(df) * 0.25):
    #     amount_to_trans = int(((percentage - 25)/100) * len(df))
    #     print(f'New Number of Non English for {company}: {amount_to_trans} and len of df is {len(df)}')
    #     non_english_df = non_english_df.sample(amount_to_trans)
    #     non_english_df["title"] = non_english_df["title"].apply(translate)
        
    df = pd.concat([english_df,non_english_df],axis=0,ignore_index=True)
    return english_df[['date','title','Ticker']]


def news_arrange():  
    df_AAPL_news = get_news_data('apple','APPL') 
    df_MSFT_news = get_news_data('microsoft','MSFT')    
    df_TSLA_news = get_news_data('tesla','TSLA')
    df_NVDA_news = get_news_data('nvidia','NVDA')
    
    df_APPL_news_trans = translate_news(df_AAPL_news,'apple') 
    df_MSFT_news_trans = translate_news(df_MSFT_news,'microsoft')    
    df_TSLA_news_trans = translate_news(df_TSLA_news,'tesla')
    df_NVDA_news_trans = translate_news(df_NVDA_news,'nvidia')

    datasets = [df_APPL_news_trans,df_MSFT_news_trans,df_TSLA_news_trans,df_NVDA_news_trans]  

    news_df_stage_1 = pd.concat(datasets,axis=0,ignore_index=True)
    df_dummies = pd.get_dummies(data=news_df_stage_1['Ticker'])
    news_df = pd.concat([news_df_stage_1,df_dummies],axis=1)
    
    return news_df

