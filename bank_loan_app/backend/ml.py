# backend/ml.py
import os
import joblib
from sklearn.base import BaseEstimator

def _get_model_path():
    # ml.py находится в backend/, а модель — в backend/model/log_reg.pkl
    base_dir = os.path.dirname(__file__)  # это backend/
    return os.path.join(base_dir, 'model', 'log_reg.pkl')

# Загружаем модель один раз при старте
try:
    MODEL_PATH = _get_model_path()
    model: BaseEstimator = joblib.load(MODEL_PATH)
except Exception as e:
    raise RuntimeError(f"Failed to load model at {MODEL_PATH}: {e}")

async def predict_loan(features: list[float]) -> bool:
    """
    Predict loan approval based on features list.
    Returns True if approved, False otherwise.
    """
    result = model.predict([features])
    return bool(result[0])
