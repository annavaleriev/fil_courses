from rest_framework import serializers

from materials.serializer import CourseSerializer, LessonSerializer
from users.models import User, Payment, UserSubscription


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class PaymentSerializer(serializers.ModelSerializer):
    """Сериализатор для платежей"""

    paid_course = CourseSerializer(read_only=True)
    paid_lesson = LessonSerializer(read_only=True)

    class Meta:
        model = Payment
        fields = "__all__"


class UserSubscriptionSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = UserSubscription
        fields = ("user", "course")
