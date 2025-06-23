# .\env\Scripts\Activate.ps1
# uvicorn main:app --reload

# http://127.0.0.1:8000/
# http://127.0.0.1:8000/docs

# for html -> http (from /frontend)
# python -m http.server 8080
# http://127.0.0.1:8080/index.html


from database import init_db
from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from sqlmodel import Session
from database import init_db, get_session
from models import User, Prediction
from ml import predict_loan
from auth import (
    get_password_hash, authenticate_user,
    create_access_token, get_current_user, oauth2_scheme
)
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:8080"],  # или ["*"] для любых источников
    allow_credentials=True,
    allow_methods=["*"],     # GET, POST, PUT и т.д.
    allow_headers=["*"],     # любые заголовки
)

@app.on_event("startup")
def on_startup():
    init_db()

class RegisterSchema(BaseModel):
    login: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

@app.post("/register", status_code=201)
def register(data: RegisterSchema, session: Session = Depends(get_session)):
    hashed = get_password_hash(data.password)
    user = User(login=data.login, password_hash=hashed)
    session.add(user)
    session.commit()
    session.refresh(user)
    return {"user_id": user.user_id, "login": user.login}

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

class LoanData(BaseModel):
    dependents: float
    income_annum: float
    loan_amount: float
    loan_term: float
    cibil_score: float
    self_employed: bool
    education: bool

@app.post("/predict")
async def predict(data: LoanData, user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    features = [
        data.dependents, data.income_annum, data.loan_amount,
        data.loan_term, data.cibil_score,
        int(data.self_employed), int(data.education)
    ]
    status = await predict_loan(features)
    pred = Prediction(
        user_id=user.user_id,
        dependents=data.dependents,
        income_annum=data.income_annum,
        loan_amount=data.loan_amount,
        loan_term=data.loan_term,
        cibil_score=data.cibil_score,
        self_employed=data.self_employed,
        education=data.education,
        loan_status=status
    )
    session.add(pred)
    session.commit()
    session.refresh(pred)
    return {"loan_status": status}
