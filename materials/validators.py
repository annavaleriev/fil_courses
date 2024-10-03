import re

from rest_framework.exceptions import ValidationError
from django.core.exceptions import ValidationError as AdminValidationError


def validate_youtube_link(value):
    if not re.match(r"^https://www.youtube.com/.+", value):
        raise ValidationError("Загружать можно только видео с YouTube")


def validate_admin_youtube_link(value):
    if not re.match(r"^https://www.youtube.com/.+", value):
        raise AdminValidationError("Загружать можно только видео с YouTube")
