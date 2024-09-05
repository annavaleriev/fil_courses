from django.urls import path
from rest_framework.routers import DefaultRouter

from users.views import UserViewSet, PaymentListView
from users.apps import UsersConfig

app_name = UsersConfig.name

router = DefaultRouter()
router.register(r"", UserViewSet)

urlpatterns = [
    path("payments/", PaymentListView.as_view(), name="payment-list"),
] + router.urls
