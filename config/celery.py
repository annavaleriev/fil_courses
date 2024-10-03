import os
from celery import Celery

# Установка переменной окружения для настроек проекта
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

# Создание экземпляра объекта Celery
app = Celery("config")

# Загрузка настроек из файла Django
app.config_from_object("django.conf:settings", namespace="CELERY")

# Автоматическое обнаружение и регистрация задач из файлов tasks.py в приложениях Django
app.autodiscover_tasks()

app.conf.update(
    worker_concurrency=4,  # Установите число рабочих процессов
    worker_pool="eventlet",  # Используйте eventlet как пул процессов
)

app.conf.broker_connection_retry_on_startup = True
