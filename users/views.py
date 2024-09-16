from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics, status
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from materials.models import Course
from users.filters import PaymentFilter
from users.models import User, Payment, UserSubscription
from users.serializer import UserSerializer, PaymentSerializer


class UserViewSet(viewsets.ModelViewSet):  # Создаем ViewSet для пользователей
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


class SubscriptionView(APIView):
    """Подписка на курс"""
    permission_classes = [IsAuthenticated]  # Устанавливаем права доступа только для авторизованных пользователей

    @staticmethod
    def post(request, course_id):
        user = request.user  # Получаем пользователя
        course = get_object_or_404(Course, id=course_id)  # Получаем курс
        if UserSubscription.objects.filter(user=user,
                                           course=course).exists():  # Проверяем, подписан ли пользователь на курс
            return Response({"message": "Вы уже подписаны на курс"},
                            status=status.HTTP_400_BAD_REQUEST)  # Выводим ошибку
        UserSubscription.objects.create(user=user, course=course)  # Создаем подписку
        return Response({"message": "Вы успешно подписались на курс"},
                        status=status.HTTP_201_CREATED)  # Выводим сообщение об успешной подписке

    @staticmethod
    def delete(request, course_id):
        user = request.user
        course = get_object_or_404(Course, id=course_id)

        subscription = UserSubscription.objects.filter(user=user, course=course)
        if subscription.exists():
            subscription.delete()
            return Response({"message": "Ваша подписка на курс успешно отменена"},
                            status=status.HTTP_204_NO_CONTENT)
        return Response({"message": "Вы не подписаны на курс"})
