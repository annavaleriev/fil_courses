from celery import shared_task
from django.contrib.auth import get_user_model
from django.utils import timezone


@shared_task
def deactivate_users():
    """Деактивация пользователей"""

    one_month_ago = timezone.now() - timezone.timedelta(days=30)
    User = get_user_model()
    users = User.objects.filter(is_active=True)
    deactivate_count = 0

    for user in users:
        if user.last_login < one_month_ago:
            user.is_active = False
            user.save()
            deactivate_count += 1

    return f"Деактивировано {deactivate_count} пользователей"
