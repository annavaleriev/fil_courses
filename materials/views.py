from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from materials.models import Course, Lesson
from materials.serializer import CourseSerializer, LessonSerializer
from users.permissions import IsModer, IsOwner, IsSuperUser


class CourseLessonBasePermissionViewSet(viewsets.ModelViewSet):
    # permission_classes = [IsOwner | IsSuperUser]
    permission_classes = [IsOwner | IsModer | IsSuperUser]

    def get_queryset(self):
        queryset = super().get_queryset()
        if (
            self.request.user.is_superuser
            or self.request.user.groups.filter(name="moders").exists()
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


class LessonViewSet(CourseLessonBasePermissionViewSet):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
