from django.urls import include, path
from rest_framework import routers

from .views import CategoryViewSet, AnalyticsViewSet, TransactionViewSet

router = routers.DefaultRouter()
router.register(r"transaction", TransactionViewSet, basename="transaction")
router.register(r"category", CategoryViewSet, basename="category")
router.register(r"analytics", AnalyticsViewSet, basename="analytics")


urlpatterns = [
    path("", include(router.urls)),
]
