# app/finbert.py
import os
import tensorflow as tf
from transformers import AutoTokenizer, TFAutoModelForSequenceClassification
from app.core.logger import logger

MODEL_ID = "ProsusAI/finbert"
MODEL_CACHE_DIR = os.path.join(os.path.expanduser("~"), ".finbert_cache")

_tokenizer = None
_model = None


def load_finbert():
    global _tokenizer, _model

    if _tokenizer is not None and _model is not None:
        return _tokenizer, _model

    logger.info("Loading FinBERT...")

    os.makedirs(MODEL_CACHE_DIR, exist_ok=True)

    _tokenizer = AutoTokenizer.from_pretrained(
        MODEL_ID, cache_dir=MODEL_CACHE_DIR
    )
    _model = TFAutoModelForSequenceClassification.from_pretrained(
        MODEL_ID, from_pt=True, cache_dir=MODEL_CACHE_DIR
    )

    logger.info("FinBERT ready")
    return _tokenizer, _model
