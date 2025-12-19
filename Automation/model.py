import pandas as pd
from tensorflow.keras.models import load_model
# from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf
from datetime import datetime
import numpy as np
import joblib


from news_feat_eng import stock_with_sentiment




# --- LOAD HISTORICAL DATA & MODEL ---
df = stock_with_sentiment.copy()
df = df.drop_duplicates()
scaler = joblib.load('models/scaler_v3.1.save')
model = load_model('../Version 3/models/v3.2(sentiment)_lstm_stock_pediction.keras')

# --- PREDICTION FOR TODAY ---
live_df = df.tail(4).drop('Target',axis=1)
X_live_scaled = scaler.transform(live_df)

# # --- MODEL ARCHITECTRE ---
# time_stamp = 20
# features = len(live_df.columns)

# # Reconstructed architecture
# model = tf.keras.models.Sequential()
# model.add(tf.keras.Input(shape=(time_stamp, features)))
# model.add(tf.keras.layers.LSTM(128, batch_input_shape=(None, time_stamp, features), return_sequences=True))
# model.add(tf.keras.layers.Dropout(0.2))
# model.add(tf.keras.layers.LSTM(64, return_sequences=False))
# model.add(tf.keras.layers.Dense(32, activation="tanh"))
# model.add(tf.keras.layers.Dense(1, activation="sigmoid"))

# # Compile minimally
# optimizer = tf.keras.optimizers.Adam(learning_rate=0.004,  clipnorm=1.0)
# model.compile(
#     optimizer=optimizer, 
#     loss='binary_crossentropy', 
#     metrics=["accuracy"]
# )

# # Load weights
# model.load_weights("../Version 3/v3.2(sentiment)_lstm_stock_pediction.weights.h5")  # <-- now your model has learned weights

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
time_stamp =20
X_live_seq = build_multi_stock_sequences(X_live_scaled,time_stamp)


pred = model.predict(X_live_seq)
pred_value = y_pred_1 = (pred.ravel() >= 0.5).astype(int)
print(f"Predicted direction for next day: {pred_value}")



# --- STORING NEXT WEEK ---
next_week_path = 'data/new_week_data.csv'

new_week_data_df = pd.read_csv(next_week_path,index_col=0)
new_week_data_df = pd.concat([new_week_data_df,df.tail(4)],axis=0,ignore_index=True)
new_week_data_df.to_csv(next_week_path,index=False)

# --- SAVE UPDATED HISTORICAL DATA ---
df.to_csv('data/historical_data.csv',index=False)



# --- RETRAIN MODEL IF WEEK IS COMPLETE ---
if len(new_week_data_df) >= 28:
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
    
    def create_sequence(X, y, time_stamp=5):
        Xs, ys = [], []
        for i in range(len(X) - time_stamp):
            Xs.append(X[i:(i + time_stamp)])
            ys.append(y[i + time_stamp])
        return np.array(Xs), np.array(ys)
    
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
    
    # Save updated model
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    model.save(f"/models/v3.2(sentiment)_lstm_stock_pediction_{timestamp}.keras")
    
    # Reset weekly data
    pd.DataFrame(columns=new_week_data_df.columns).to_csv('data/new_week_data.csv', index=False)
    # clear_week =  pd.DataFrame(data=None, columns=new_week_data_df.columns,index=new_week_data_df.index)
    # clear_week = clear_week.dropna()
    # clear_week.to_csv('data/new_week_data.csv')