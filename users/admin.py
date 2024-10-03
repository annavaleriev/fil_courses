from django.contrib import admin

from users.models import User, Payment


@admin.register(User)  # Регистрируем модель User в админке
class UserAdmin(admin.ModelAdmin):
    list_display = ("email", "phone", "is_active")  # Поля для отображения в админке
    exclude = ("password",)
    filter_horizontal = ("groups", "user_permissions")


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    exclude = ()
    list_display = (
        "user",
        "payment_date",
        "paid_course",
        "paid_lesson",
        "payment_method",
        "amount",
        "stripe_payment_status",
    )
    list_filter = (
        "user",
        "payment_date",
        "paid_course",
        "paid_lesson",
        "payment_method",
        "amount",
        "stripe_payment_status",
    )
