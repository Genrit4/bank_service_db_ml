# bd_view.py
# python bd_view.py

from sqlmodel import Session, select
from models import User, Prediction
from database import engine
import pandas as pd
import os

# Путь до папки
output_dir = r"D:\summer_practice\bank_service_db_ml\bank_loan_app\backend\data_from_db"
os.makedirs(output_dir, exist_ok=True)  # Создаст папку, если нет

# Получаем сессию
with Session(engine) as session:
    users = session.exec(select(User)).all()
    preds = session.exec(select(Prediction)).all()

# Преобразуем в DataFrame
df_users = pd.DataFrame([u.dict() for u in users])
df_preds = pd.DataFrame([p.dict() for p in preds])

# Сохраняем в указанный путь
df_users.to_csv(os.path.join(output_dir, "users.csv"), index=False)
df_preds.to_csv(os.path.join(output_dir, "predictions.csv"), index=False)
