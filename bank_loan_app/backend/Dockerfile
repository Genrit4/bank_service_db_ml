FROM python:3.11-slim

# Рабочая директория внутри контейнера
WORKDIR /app

# Копируем backend requirements
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь backend
COPY . .

# Копируем frontend в контейнер
COPY ../../frontend ./frontend

# Копируем модель
RUN mkdir -p /model && cp model/log_reg.pkl /model/log_reg.pkl

# Экспонируем порт FastAPI
EXPOSE 8000

# Запуск FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

# FROM python:3.11-slim

# WORKDIR /backend

# COPY backend/requirements.txt ./
# RUN pip install --no-cache-dir -r requirements.txt

# COPY backend/ ./

# RUN mkdir -p /model && cp model/log_reg.pkl /model/log_reg.pkl

# EXPOSE 8000

# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
