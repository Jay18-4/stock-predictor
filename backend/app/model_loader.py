import tensorflow as tf
import joblib
from app.storage import download_file

MODEL_KEY = "models/v3.2(sentiment)_lstm_stock_pediction.keras"
LOCAL_MODEL_PATH = "/tmp/v3.2(sentiment)_lstm_stock_pediction.keras"
SCALER_KEY = 'scaler_v3.1.save'
LOCAL_SCALER_PATH = "/tmp/scaler_v3.1.save"

_model = None
_scaler = None

def get_model():
    global _model

    if _model is None:
        download_file(MODEL_KEY, LOCAL_MODEL_PATH)

        _model = tf.keras.models.load_model(
            LOCAL_MODEL_PATH,
            compile=False  # IMPORTANT: avoids unnecessary memory usage
        )

    return _model

def get_scaler():
    global _scaler

    if _scaler is None:
        download_file(SCALER_KEY, LOCAL_MODEL_PATH)

        _scaler = joblib.load(LOCAL_SCALER_PATH)

    return _scaler
