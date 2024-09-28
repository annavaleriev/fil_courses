from http import HTTPMethod

from django.urls import reverse
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from materials.models import Course, Lesson
from materials.paginators import LessonAndCoursePagination
from materials.serializer import CourseSerializer, LessonSerializer
from users.models import UserSubscription, MODER_GROUP_NAME, Payment
from users.permissions import IsOwnerSuperUser, NotIsModer
from users.serializer import UserSubscriptionSerializer, PaymentCreateSerializer
from users.stripe_service import (
    create_stripe_product,
    create_stripe_price,
    create_stripe_sessions_payment,
)


class CourseLessonBasePermissionViewSet(viewsets.ModelViewSet):
    # permission_classes = [IsOwner | IsSuperUser]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        if (
            self.request.user.is_superuser
            or self.request.user.groups.filter(name=MODER_GROUP_NAME).exists()
        ):
            return queryset
        return queryset.filter(owner=self.request.user)

    def get_permissions(self):
        # if self.action in ["create"]:
        #     self.permission_classes = [IsAuthenticated & ~IsModer]
        # elif self.action in ["update", "partial_update", "retrieve", "list"]:
        #     self.permission_classes = [IsOwner | IsModer | IsSuperUser]
        if self.action in ["create"]:
            self.permission_classes = [IsAuthenticated, NotIsModer]
        elif self.action in ["destroy"]:
            self.permission_classes = [IsAuthenticated, IsOwnerSuperUser]
        return super().get_permissions()


class CourseViewSet(CourseLessonBasePermissionViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    pagination_class = LessonAndCoursePagination

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

        request.data.update({"course": pk})
        response = self.create(request)
        if response.status_code == status.HTTP_201_CREATED:
            response.data = {"message": "подписка добавлена"}
        return response

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

        request.data.update(
            {
                "user": request.user,
                "paid_course": pk,
                "amount": float(course.price),
                "stripe_session_id": session.id,
                "payment_method": Payment.Method.CARD,
                "stripe_payment_url": session.url,
            }
        )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        Payment.objects.get_or_create(
            user=request.user,
            paid_course=course,
            amount=float(course.price),
            payment_method=Payment.Method.CARD,
            stripe_session_id=session.id,
            stripe_payment_url=session.url,
        )
        headers = self.get_success_headers(serializer.data)
        return Response(
            {"url": session.url}, status=status.HTTP_201_CREATED, headers=headers
        )

        # return self.create(request.data)


class LessonViewSet(CourseLessonBasePermissionViewSet):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    pagination_class = LessonAndCoursePagination
