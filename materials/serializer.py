from rest_framework import serializers

from materials.models import Course, Lesson
from materials.validators import validate_youtube_link
from users.models import UserSubscription


class LessonSerializer(serializers.ModelSerializer):
    """Сериализатор для уроков"""

    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    video = serializers.URLField(validators=[validate_youtube_link])

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
    def get_lesson_count(obj) -> int:
        return obj.lessons.count()

    def get_is_subscribed(self, obj):
        user = self.context["request"].user  # Получаем пользователя
        if user.is_authenticated:  # Проверяем, аутентифицирован ли пользователь
            return UserSubscription.objects.filter(
                user=user, course=obj
            ).exists()  # Проверяем, подписан ли пользователь на курс
