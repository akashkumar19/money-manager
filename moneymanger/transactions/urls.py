from django.urls import path, include
from .views import TransactionViewset, CategoryViewset
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'transaction', TransactionViewset,basename="transaction")
router.register(r'category', CategoryViewset, basename='category')


urlpatterns = [
    path('', include(router.urls))
]
