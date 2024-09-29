from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics, status
from rest_framework.filters import OrderingFilter, SearchFilter

from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from users.filters import PaymentFilter
from users.models import User, Payment
from users.serializer import UserSerializer, PaymentSerializer
from users.stripe_service import retrieve_stripe_payment_status


class UserViewSet(viewsets.ReadOnlyModelViewSet):  # Создаем ViewSet для пользователей
    queryset = User.objects.all()  # Получаем всех пользователей
    serializer_class = UserSerializer  # Используем сериализатор
    permission_classes = [
        IsAuthenticated
    ]  # Устанавливаем права доступа только для авторизованных пользователей


class UserCreateView(generics.CreateAPIView):  # Создаем View для создания пользователя
    queryset = User.objects.all()  # Получаем всех пользователей
    serializer_class = UserSerializer  # Используем сериализатор
    # permission_classes = [AllowAny] # Устанавливаем права доступа для всех пользователей
    permission_classes = (
        AllowAny,
    )  # Устанавливаем права доступа для всех пользователей

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)  # Создаем пользователя
        user.set_password(user.password)  # Хешируем пароль
        user.save()


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
