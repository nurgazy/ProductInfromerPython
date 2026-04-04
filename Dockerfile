# Используем официальный легкий образ Python
FROM python:3.11-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Запрещаем Python писать файлы .pyc на диск и обеспечиваем вывод логов без буферизации
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Устанавливаем системные зависимости (если понадобятся для сборки некоторых библиотек)
RUN apt-get update && apt-get install -y --no-install-recommends gcc && rm -rf /var/lib/apt/lists/*

# Копируем файл зависимостей
COPY requirements.txt .

# Устанавливаем зависимости из вашего списка
RUN pip install --no-cache-dir -r requirements.txt

# Копируем исходный код (main.py)
COPY . .

# Открываем порт 8000
EXPOSE 8000

# Запускаем приложение с помощью uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]