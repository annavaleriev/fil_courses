from rest_framework.routers import DefaultRouter

from materials.apps import MaterialsConfig
from materials.views import (
    CourseViewSet,
    LessonViewSet,
)

app_name = MaterialsConfig.name

router = DefaultRouter()
router.register("courses", CourseViewSet)
router.register("lessons", LessonViewSet)

urlpatterns = router.urls
