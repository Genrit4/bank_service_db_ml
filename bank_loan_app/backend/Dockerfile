FROM python:3.11-slim

WORKDIR /backend

COPY backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ ./

RUN mkdir -p /model && cp model/log_reg.pkl /model/log_reg.pkl

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]