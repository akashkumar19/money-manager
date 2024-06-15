from django.urls import include, path
from rest_framework import routers

from .views import (CategoryViewset, TransactionAnalyticsView,
                    TransactionViewset)

router = routers.DefaultRouter()
router.register(r"transaction", TransactionViewset, basename="transaction")
router.register(r"category", CategoryViewset, basename="category")


urlpatterns = [
    path("", include(router.urls)),
    path(
        "transaction-analytics/",
        TransactionAnalyticsView.as_view(),
        name="transaction-analytics",
    ),
]
