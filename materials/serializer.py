from rest_framework import serializers

from materials.models import Course, Lesson


class LessonSerializer(serializers.ModelSerializer):
    """Сериализатор для уроков"""

    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    """Сериализатор для курсов"""

    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    lesson_count = (
        serializers.SerializerMethodField()
    )  # Добавляем поле с количеством уроков
    lessons = LessonSerializer(many=True, read_only=True)  # Добавляем поле с уроками

    class Meta:
        model = Course
        fields = "__all__"

    @staticmethod
    def get_lesson_count(obj):
        return obj.lessons.count()
