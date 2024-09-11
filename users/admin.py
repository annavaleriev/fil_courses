from django.contrib import admin

from users.models import User


@admin.register(User)  # Регистрируем модель User в админке
class UserAdmin(admin.ModelAdmin):
    list_display = ("email", "phone", "is_active")  # Поля для отображения в админке
    exclude = ("password",)
    filter_horizontal = ("groups", "user_permissions")
