# backend/ml.py
import os
import joblib
from sklearn.base import BaseEstimator

# Determine path to model relative to this file
def _get_model_path():
    # ml.py at backend/, project root likely one level up (bank_loan_app)
    # but model is located at parent of bank_loan_app (bank_analys/model)
    # so go up three levels: ml.py -> backend -> bank_loan_app -> bank_analys
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    return os.path.join(base_dir, 'model', 'log_reg.pkl')

# Load model once
try:
    MODEL_PATH = _get_model_path()
    model: BaseEstimator = joblib.load(MODEL_PATH)
except Exception as e:
    raise RuntimeError(f"Failed to load model at {MODEL_PATH}: {e}")

async def predict_loan(features: list[float]) -> bool:
    """
    Predict loan approval based on features list.
    Features order: [dependents, income_annum, loan_amount, loan_term, cibil_score, self_employed, education]
    Returns True if approved, False otherwise.
    """
    result = model.predict([features])
    return bool(result[0])
