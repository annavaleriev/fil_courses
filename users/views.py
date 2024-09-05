from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics
from rest_framework.filters import OrderingFilter, SearchFilter

from users.filters import PaymentFilter
from users.models import User, Payment
from users.serializer import UserSerializer, PaymentSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class PaymentListView(generics.ListAPIView):
    """ViewSet для платежей"""

    queryset = Payment.objects.all()  # Получаем все платежи
    serializer_class = PaymentSerializer  # Используем сериализатор

    filter_backends = (
        OrderingFilter,
        DjangoFilterBackend,
        SearchFilter,
    )  # Добавляем фильтрацию и сортировку
    search_fields = ["paid_course__title", "paid_lesson__title", "payment_method"]
    filterset_class = PaymentFilter  # Используем фильтры
    ordering_fields = ("payment_date",)  # Сортируем по всем полям
    ordering = ["-payment_date"]  # Сортируем по убыванию даты платежа
