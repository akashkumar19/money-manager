from django.urls import path, include
from .views import TransactionViewset, CategoryViewset, TransactionAnalyticsView
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'transaction', TransactionViewset,basename="transaction")
router.register(r'category', CategoryViewset, basename='category')


urlpatterns = [
    path('', include(router.urls)),
    path('transaction-analytics/', TransactionAnalyticsView.as_view(), name="transaction-analytics")
]
