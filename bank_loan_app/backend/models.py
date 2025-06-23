# backend/models.py
from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field
from sqlalchemy import Column, String

class User(SQLModel, table=True):
    user_id: Optional[int] = Field(default=None, primary_key=True)
    login: str = Field(sa_column=Column(String(100), unique=True, nullable=False))
    password_hash: str

class Prediction(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int
    dependents: float
    income_annum: float
    loan_amount: float
    loan_term: float
    cibil_score: float
    self_employed: bool
    education: bool
    loan_status: bool
    timestamp: datetime = Field(default_factory=datetime.utcnow)
