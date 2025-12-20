# app/finbert.py
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

MODEL_NAME = "ProsusAI/finbert"

_tokenizer = None
_model = None

def load_finbert():
    global _tokenizer, _model

    if _tokenizer is None or _model is None:
        print("Loading FinBERT model (one-time)...")

        _tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
        _model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)

        _model.eval()

    return _tokenizer, _model
