import django_filters

from users.models import Payment


class PaymentFilter(django_filters.FilterSet):
    """Фильтры для платежей"""

    course = django_filters.CharFilter(
        field_name="paid_course__title", lookup_expr="icontains"
    )  # Фильтр по названию курса
    lesson = django_filters.CharFilter(
        field_name="paid_lesson__title", lookup_expr="icontains"
    )  # Фильтр по названию урока
    payment_method = django_filters.ChoiceFilter(
        choices=Payment.Method.choices
    )  # Фильтр по способу оплаты

    class Meta:
        model = Payment
        fields = ("course", "lesson", "payment_method")
