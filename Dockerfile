# базовый образ (Python)
FROM python:3.11

# рабочая папка внутри контейнера
WORKDIR /app

# копируем requirements
COPY requirements.txt .

# устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# копируем весь проект
COPY . .

# команда запуска
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]