from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework.routers import DefaultRouter

from users.views import UserViewSet, PaymentListView, UserCreateView
from users.apps import UsersConfig

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

app_name = UsersConfig.name

router = DefaultRouter()
router.register(r"", UserViewSet)

urlpatterns = [
    path("payments/", PaymentListView.as_view(), name="payment-list"),
    path(
        "token/",
        TokenObtainPairView.as_view(permission_classes=(AllowAny,)),
        name="token_obtain_pair",
    ),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("register/", UserCreateView.as_view(), name="register"),
] + router.urls
