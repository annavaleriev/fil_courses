from celery import shared_task
from django.core.mail import send_mail

from config import settings


@shared_task
def send_course_update_email(user_email, course_title, course_url):
    """Отправка email об обновлении курса"""
    subject = f"Обновление курса: {course_title}"
    message = f"Курс {course_title} был обновлен - url = {course_url}"
    send_mail(subject, message, settings.EMAIL_HOST_USER, [user_email])
