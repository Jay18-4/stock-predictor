import pandas as pd
from tensorflow.keras.models import load_model # type: ignore
from sklearn.preprocessing import MinMaxScaler
import numpy as np
import joblib
import json
from datetime import date
from pathlib import Path

from app.core.logger import logger
from app.utils.time_utils import utc_now
from app.storage import read_csv, write_csv, read_json, write_json
from app.model_loader import get_model, get_scaler


# --- RESHAPE X_INPUT ---
def build_multi_stock_sequences(X, timesteps, num_stocks=4):
    """
    X: numpy array shaped (N, features), sorted by date,
       repeating order for each company per day.
    Returns:
        array shaped (num_stocks, timesteps, features)
    """

    X = np.array(X)
    n, f = X.shape

    sequences = []

    # Extract each company's historical series:
    for stock_index in range(num_stocks):

        stock_series = X[stock_index::num_stocks]  # pull this stock's entire history

        last_window = stock_series[-timesteps:]

        if last_window.shape[0] < timesteps:
            padded = np.zeros((timesteps, f))
            padded[-last_window.shape[0]:] = last_window
            last_window = padded

        sequences.append(last_window)

    return np.array(sequences)  # (4, timesteps, features)

def predict(df):
    logger.info("Loading LSTM model...")
    # --- LOAD HISTORICAL DATA & MODEL ---
    df = df.drop_duplicates()
    df.drop(['Ticker',"High","Low","Open"],axis="columns",inplace=True)
    
    
    # scaler_path = Path(__file__).resolve().parent.parent.parent.parent / "models" / "scaler_v3.1.save"
    # model_path = Path(__file__).resolve().parent.parent.parent.parent / "models" / "v3.2(sentiment)_lstm_stock_pediction.keras"
    
    scaler = get_scaler()
    model = get_model()

    
# --- PREDICTION FOR TODAY ---

    time_stamp =20
    live_df = df.tail(4).drop('Target',axis=1)
    X_live_scaled = scaler.transform(live_df)
    X_live_seq = build_multi_stock_sequences(X_live_scaled,time_stamp)


    pred = model.predict(X_live_seq)
    pred_value = (pred.ravel() >= 0.5).astype(int).tolist()
    
# --- SAVE UPDATED HISTORICAL DATA ---
    # data_history_path = Path(__file__).resolve().parent.parent.parent.parent / "data" / "historical_data.csv"
    
    write_csv(df, "historical_data.csv")
    
    return pred_value



# --- STORING NEXT WEEK ---
def store_next_week(df):
    # next_week_path = Path(__file__).resolve().parent.parent.parent.parent / "data" / "new_week_data.csv"

    new_week_data_df = read_csv("new_week_data.csv")
    new_week_data_df = pd.concat([new_week_data_df,df.tail(4)],axis=0,ignore_index=True)
    write_csv(df, "new_week_data.csv")
    
    
def get_new_week_daata():
    new_week_data_df = read_csv("new_week_data.csv")
    new_week_data_df = new_week_data_df.drop_duplicates()
    return new_week_data_df

def get_historical_data():
    df = read_csv("historical_data.csv")
    df = df.drop_duplicates()
    return df

# --- RETRAIN MODEL IF WEEK IS COMPLETE ---
# if len(new_week_data_df) >= 28:
def create_sequence(X, y, time_stamp=5):
    Xs, ys = [], []
    for i in range(len(X) - time_stamp):
        Xs.append(X[i:(i + time_stamp)])
        ys.append(y[i + time_stamp])
    return np.array(Xs), np.array(ys)
    
def retrain(df,new_week_df):
    df = df.drop_duplicates()
    df.drop(['Ticker',"High","Low","Open"],axis="columns",inplace=True)
    df.set_index("data", inplace = True)
    
    scaler_path = Path(__file__).resolve().parent.parent.parent.parent / "models" / "scaler_v3.1.save"
    model_path = Path(__file__).resolve().parent.parent.parent.parent / "models" / "v3.2(sentiment)_lstm_stock_pediction.keras"
    
    scaler = joblib.load(scaler_path)
    model = load_model(model_path)
    time_stamp = 20
    
    # Prepare full training data (historical + new week)
    X = df.drop(['Target'], axis="columns")
    y = np.array(df['Target'])
    
    train_size = int(len(X) * 0.70)
    val_size = int(len(X) * 0.85)
    X_train, X_val, X_test = X[0:train_size], X[train_size:val_size], X[val_size:len(X)]
    y_train, y_val, y_test = y[0:train_size], y[train_size:val_size], y[val_size:len(y)]

    X_train_scaled = scaler.transform(X_train)
    X_test_scaled  = scaler.transform(X_test)
    X_val_scaled  = scaler.transform(X_val)
    
    
    X_train_seq, y_train_seq = create_sequence(X_train_scaled, y_train, time_stamp)
    X_val_seq, y_val_seq = create_sequence(X_val_scaled, y_val, time_stamp)
    X_test_seq, y_test_seq = create_sequence(X_test_scaled, y_test, time_stamp)
    

    # --- Retrain model ---
    model.fit(
    X_train_seq,
    y_train_seq,
    validation_data=(X_val_seq, y_val_seq),
    batch_size=64,
    epochs=50,
    shuffle=False,
    verbose = 1
    # callbacks=[early_stop]
    )
    
    model.evaluate(X_test_seq, y_test_seq)
    
    # Save updated model
    timestamp = date.today()
    model_path = Path(__file__).resolve().parent.parent.parent.parent / "models" / f"v3.2(sentiment)_lstm_stock_pediction_{timestamp}.keras"
    model.save(model_path)
    
    model_version = {
    "version": f"v3.2(sentiment)_lstm_stock_pediction_{timestamp}",
    "trained_on": timestamp
    }
    # model_version_path = Path(__file__).resolve().parent.parent.parent.parent / "data" / f"model_version_{timestamp}.json"
    # with open("data/model_version.json", "w") as json_file:
    #     json.dump(model_version, json_file, indent=4)
    write_json(model_version, f"model_version_{timestamp}.json")
    
    
    # Reset weekly data
    # next_week_path = Path(__file__).resolve().parent.parent.parent.parent / "data" / "new_week_data.csv"
    clear_week = pd.DataFrame(columns=new_week_data_df.columns)
    write_csv(clear_week, "new_week_data.csv")
    
    
    return model_version
