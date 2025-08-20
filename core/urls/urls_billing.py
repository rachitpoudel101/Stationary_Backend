from rest_framework.routers import DefaultRouter
from core.apps.billing.views import BillViewSet
from django.urls import path, include

router = DefaultRouter()
router.register(r'bill', BillViewSet)

urlpatterns = [
    path('', include(router.urls)),
]