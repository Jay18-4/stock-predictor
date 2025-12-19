import pandas as pd
import tensorflow as tf
from transformers import AutoTokenizer, TFAutoModelForSequenceClassification
from tqdm import tqdm

from fetch_data import news_df

news_df = news_df.drop_duplicates(subset=['title'])

def tf_news_sentiment(df):
    text_column = "title"            # change if different
    
    # Clean NaN
    df[text_column] = df[text_column].astype(str)
    df[text_column] = df[text_column].fillna("")
    df = df.reset_index(drop=True)
    
    # ============================
    # 2. Load Model
    # ============================
    model_name = "ProsusAI/finbert"
    model_path = r"C:\Users\dalu\Desktop\finbert"
    tokenizer = AutoTokenizer.from_pretrained(model_path, local_files_only = True)
    model = TFAutoModelForSequenceClassification.from_pretrained(
        model_path,
        from_pt=True,
        local_files_only=True# convert from PyTorch
    )
    
    print("GPU available:", tf.config.list_physical_devices('GPU'))
    
    # ============================
    # 3. Parameters
    # ============================
    labels = ["negative", "neutral", "positive"]
    
    # GPU memory safe batch size
    batch_size = 32 if tf.config.list_physical_devices('GPU') else 8
    
    sentiments = []
    scores = []
    
    # ============================
    # 4. Batch Inference Loop
    # ============================
    for i in tqdm(range(0, len(df), batch_size), desc="Processing"):
        batch_texts = df[text_column].iloc[i:i+batch_size].tolist()
    
        inputs = tokenizer(
            batch_texts,
            return_tensors="tf",
            truncation=True,
            padding=True,
            max_length=128
        )
    
        # IMPORTANT: unpack dict
        outputs = model(**inputs)
    
        probs = tf.nn.softmax(outputs.logits, axis=1)
    
        for p in probs:
            idx = int(tf.argmax(p).numpy())
            score = float(tf.reduce_max(p).numpy())
            sentiments.append(labels[idx])
            scores.append(score)
    
    # ============================
    # 5. Add to DataFrame
    # ============================
    df["sentiment"] = sentiments
    df["score"] = scores
    
    return df

news_sentiment = tf_news_sentiment(news_df)
