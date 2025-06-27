# backend/Dockerfile
FROM python:3.11-slim

# переходим в папку /backend
WORKDIR /backend

# копируем зависимости
COPY backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# копируем весь код и модель
COPY backend/ ./

# модель в backend/model/log_reg.pkl, перенесём в корень контейнера
RUN mkdir -p /model && cp model/log_reg.pkl /model/log_reg.pkl

EXPOSE 8000

# запускаем, указав модуль main из backend
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]