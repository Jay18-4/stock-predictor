import tensorflow as tf
import pandas as pd
import keras
from tensorflow.keras.models import load_model
import joblib
import numpy as np

print("TF version:", tf.__version__)
print("Keras version:", keras.__version__)

model = load_model('../Version 3/models/v3.2(sentiment)_lstm_stock_pediction.keras')
scaler = joblib.load('models/scaler_v3.1.save')

df = pd.read_csv('data/historical_data.csv',index_col='date')

print(f'model: {model}')

live_df = df.tail(4).drop('Target',axis=1)
X_live_scaled = scaler.transform(live_df)


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

time_stamp =20
X_live_seq = build_multi_stock_sequences(X_live_scaled, time_stamp)

# y_live_seq = create_sequence_safe(X_live_scaled, y,time_stamp)[1]

print(X_live_seq.shape)

# print(f'df: {X_live_seq}')

# evalu = model.evaluate(X_live_seq,y_live_seq
pred = model.predict(X_live_seq)
pred_value = y_pred_1 = (pred.ravel() >= 0.5).astype(int)
print(f"Predicted direction for next day: {pred_value}")


# python scripts_testing.py