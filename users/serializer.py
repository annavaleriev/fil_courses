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


class PaymentCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для платежей"""

    class Meta:
        model = Payment
        fields = (
            "user",
            "payment_date",
            "paid_course",
            "paid_lesson",
            "amount",
            "payment_method",
            "stripe_payment_url",
        )
        read_only_fields = (
            "user",
            "payment_date",
            "paid_course",
            "paid_lesson",
            "payment_method",
            "stripe_payment_url",
            "amount",
        )


class UserSubscriptionSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = UserSubscription
        fields = ("user",)


class PaymentStatusSerializer(serializers.ModelSerializer):
    """Сериализатор для статуса платежей"""

    class Meta:
        model = Payment
        fields = ("stripe_payment_status",)


class PaymentStatusDisplaySerializer(serializers.ModelSerializer):
    status_display = serializers.SerializerMethodField()

    @staticmethod
    def get_status_display(obj) -> str:
        return obj.get_stripe_payment_status_display()

    class Meta:
        model = Payment
        fields = ("status_display",)
