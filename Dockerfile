FROM python:3.11-slim

#Устанавливаем рабоучую директорию
WORKDIR /app

#Копируем файлы зависимостей
COPY poetry.lock pyproject.toml ./


# Устанавливаем Poetry и зависимости без dev-пакетов
RUN python -m pip install --no-cache-dir poetry==1.8.3 \
    && poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi \
    && rm -rf $(poetry config cache-dir)/{cache,artifacts}

#Копируеем все файлы проекта другие
COPY . .

#Миграции и запуск сервера
CMD ["sh", "-c",
    "python manage.py migrate && \
     python manage.py runserver 0.0.0.0:8000"
]
