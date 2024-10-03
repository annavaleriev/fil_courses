from http import HTTPMethod

from django.db.models import Q
from django.urls import reverse
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from stripe import StripeError

from materials.models import Course, Lesson
from materials.paginators import LessonAndCoursePagination
from materials.serializer import CourseSerializer, LessonSerializer
from users.models import UserSubscription, MODER_GROUP_NAME, Payment
from users.permissions import IsOwnerSuperUser, NotIsModer
from users.serializer import (
    UserSubscriptionSerializer,
    PaymentCreateSerializer,
    PaymentStatusSerializer,
    PaymentStatusDisplaySerializer,
)
from users.stripe_service import (
    create_stripe_product,
    create_stripe_price,
    create_stripe_sessions_payment,
    retrieve_stripe_payment_status,
)
from .tasks import send_course_update_email


class CourseLessonBasePermissionViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        if (
            self.request.user.is_superuser
            or self.request.user.groups.filter(name=MODER_GROUP_NAME).exists()
        ):
            return queryset
        course_subscriptions = UserSubscription.objects.filter(
            user=self.request.user
        ).values_list("course_id", flat=True)
        return queryset.filter(
            Q(owner=self.request.user) | Q(pk__in=course_subscriptions)
        )

    def get_permissions(self):
        if self.action in ["create"]:
            self.permission_classes = [IsAuthenticated, NotIsModer]
        elif self.action in ["destroy"]:
            self.permission_classes = [IsAuthenticated, IsOwnerSuperUser]
        return super().get_permissions()


class CourseViewSet(CourseLessonBasePermissionViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    pagination_class = LessonAndCoursePagination

    def update(self, request, *args, **kwargs):
        course = self.get_object()
        current_time = timezone.now()

        serializer = self.get_serializer(course, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        update_timedelta = current_time - course.last_update
        update_timedelta_hours = update_timedelta.total_seconds() // 3600
        if update_timedelta_hours >= 4:
            subscribers = UserSubscription.objects.filter(course=course)

            for subscriber in subscribers:
                user_email = subscriber.user.email
                host = f"http://{request.get_host()}"
                course_url = host + reverse(
                    "materials:course-detail", kwargs={"pk": course.id}
                )
                send_course_update_email.delay(user_email, course.title, course_url)

        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=True,
        methods=[HTTPMethod.POST],
        serializer_class=UserSubscriptionSerializer,
    )
    def subscription(self, request, pk=None):
        user = request.user

        user_subscription = UserSubscription.objects.filter(
            user=user, course_id=int(pk)
        )
        if user_subscription.exists():
            user_subscription.delete()
            return Response(
                data={"message": "подписка удалена"}, status=status.HTTP_204_NO_CONTENT
            )

        course = get_object_or_404(Course, pk=pk)
        UserSubscription.objects.create(
            user=user,
            course=course,
        )
        return Response(
            data={"message": "подписка добавлена"}, status=status.HTTP_201_CREATED
        )

    @action(
        detail=True,
        methods=[HTTPMethod.POST],
        serializer_class=PaymentCreateSerializer,
    )
    def pay(self, request, pk=None):
        course = get_object_or_404(Course, pk=pk)
        course_detail_url = reverse("materials:course-detail", kwargs={"pk": pk})
        host = f"http://{request.get_host()}"
        cancel_url = success_url = host + course_detail_url

        product = create_stripe_product(course.title)
        price = create_stripe_price(product.id, float(course.price))
        session = create_stripe_sessions_payment(price.id, success_url, cancel_url)

        data = {
            "user": request.user,
            "paid_course": course,
            "amount": float(course.price),
            "stripe_session_id": session.id,
            "payment_method": Payment.Method.CARD,
            "stripe_payment_url": session.url,
        }

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        Payment.objects.get_or_create(**data)
        headers = self.get_success_headers(serializer.data)
        return Response(
            {"url": session.url}, status=status.HTTP_201_CREATED, headers=headers
        )

    @action(
        detail=True,
        methods=[HTTPMethod.GET],
        serializer_class=PaymentStatusDisplaySerializer,
    )
    def payment_status(self, request, pk=None):
        course = get_object_or_404(Course, pk=pk)
        payment = course.payment_set.filter(
            paid_course=course, user=request.user
        ).first()

        if not payment:
            return Response({"status_display": Payment.PaymentStatus.UNPAID.label})
        try:
            session = retrieve_stripe_payment_status(
                payment.stripe_session_id
            )  # Получаем статус платежа
        except StripeError as e:
            return Response(
                {"message": str(e)}, status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

        payment_status = session.payment_status
        serializer = PaymentStatusSerializer(
            data={"stripe_payment_status": payment_status}
        )
        serializer.is_valid(raise_exception=True)

        payment.update_payment_status(payment_status)  # Обновляем статус платежа
        model_serializer = self.get_serializer(payment)
        return Response(model_serializer.data)


class LessonViewSet(CourseLessonBasePermissionViewSet):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    pagination_class = LessonAndCoursePagination
