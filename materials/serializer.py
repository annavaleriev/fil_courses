from rest_framework import serializers

from materials.models import Course


class CourseSerializer(serializers.ModelSerializer):
    """Сериализатор для курсов"""

    class Meta:
        model = Course
        fields = "__all__"


class LessonSerializer(serializers.ModelSerializer):
    """Сериализатор для уроков"""

    class Meta:
        model = Course
        fields = "__all__"
