# .\env\Scripts\Activate.ps1
# uvicorn main:app --reload

# http://127.0.0.1:8000/
# http://127.0.0.1:8000/docs

# for html -> http (from /frontend)
# python -m http.server 8080
# http://127.0.0.1:8080/index.html


# backend/main.py
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlmodel import Session
from database import init_db, get_session
from models import User, Prediction
from ml import predict_loan
from auth import (
    get_password_hash, authenticate_user,
    create_access_token, get_current_user
)
import os

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Startup event
@app.on_event("startup")
def on_startup():
    init_db()

# Serve frontend index
frontend_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'frontend')
@app.get("/", response_class=HTMLResponse)
def serve_index():
    return FileResponse(os.path.join(frontend_dir, 'index.html'))

# Auth schemas
class RegisterSchema(BaseModel):
    login: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

# Registration endpoint
@app.post("/register", status_code=201)
def register(data: RegisterSchema, session: Session = Depends(get_session)):
    # Check if login already exists
    existing = session.query(User).filter(User.login == data.login).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User with login '{data.login}' already exists"
        )
    hashed = get_password_hash(data.password)
    user = User(login=data.login, password_hash=hashed)
    session.add(user)
    session.commit()
    session.refresh(user)
    return {"user_id": user.user_id, "login": user.login}

# Login endpoint
@app.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    user = authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.login})
    return {"access_token": access_token, "token_type": "bearer"}

# Predict endpoint
class LoanData(BaseModel):
    dependents: float
    income_annum: float
    loan_amount: float
    loan_term: float
    cibil_score: float
    self_employed: bool
    education: bool

@app.post("/predict")
async def predict(
    data: LoanData,
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    features = [
        data.dependents,
        data.income_annum,
        data.loan_amount,
        data.loan_term,
        data.cibil_score,
        int(data.self_employed),
        int(data.education)
    ]
    status = await predict_loan(features)
    pred = Prediction(
        user_id=user.user_id,
        **data.dict(),
        loan_status=status
    )
    session.add(pred)
    session.commit()
    session.refresh(pred)
    return {"loan_status": status}
