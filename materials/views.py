from http import HTTPMethod

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from materials.models import Course, Lesson
from materials.paginators import LessonAndCoursePagination
from materials.serializer import CourseSerializer, LessonSerializer
from users.models import UserSubscription, MODER_GROUP_NAME
from users.permissions import IsModer, IsOwner, IsSuperUser
from users.serializer import UserSubscriptionSerializer


class CourseLessonBasePermissionViewSet(viewsets.ModelViewSet):
    # permission_classes = [IsOwner | IsSuperUser]
    permission_classes = [IsOwner | IsModer | IsSuperUser]

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
            self.permission_classes = [IsAuthenticated & ~IsModer]
        elif self.action in ["destroy"]:
            self.permission_classes = [IsOwner | IsSuperUser]
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

        user_subscription = UserSubscription.objects.filter(user=user, course_id=pk)
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


class LessonViewSet(CourseLessonBasePermissionViewSet):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    pagination_class = LessonAndCoursePagination
