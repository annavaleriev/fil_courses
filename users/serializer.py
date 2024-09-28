from rest_framework import serializers
from decimal import Decimal
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

    user = serializers.PrimaryKeyRelatedField(read_only=True)
    payment_date = serializers.DateTimeField(read_only=True)
    paid_course = serializers.PrimaryKeyRelatedField(read_only=True)
    paid_lesson = serializers.PrimaryKeyRelatedField(read_only=True)
    payment_method = serializers.ChoiceField(
        choices=Payment.Method.choices, read_only=True
    )
    stripe_payment_url = serializers.URLField(read_only=True)
    amount = serializers.DecimalField(
        min_value=Decimal("0.01"), max_digits=10, decimal_places=2, read_only=True
    )

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


class UserSubscriptionSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = UserSubscription
        fields = ("user", "course")
