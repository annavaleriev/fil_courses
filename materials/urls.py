from django.urls import path
from rest_framework.routers import DefaultRouter

from materials.apps import MaterialsConfig
from materials.views import (
    LessonCreateAPIView,
    LessonListAPIView,
    LessonRetrieveAPIView,
    LessonUpdateAPIView,
    CourseViewSet,
    LessonDestroyAPIView,
)

app_name = MaterialsConfig.name

router = DefaultRouter()
router.register("courses", CourseViewSet)

urlpatterns = [
    path("lessons/create/", LessonCreateAPIView.as_view(), name="lesson create"),
    path("lessons/", LessonListAPIView.as_view(), name="lesson list"),
    path("lessons/<int:pk>/", LessonRetrieveAPIView.as_view(), name="lesson retrieve"),
    path(
        "lessons/<int:pk>/update/", LessonUpdateAPIView.as_view(), name="lesson update"
    ),
    path(
        "lessons/<int:pk>/delete/", LessonDestroyAPIView.as_view(), name="lesson delete"
    ),
] + router.urls
