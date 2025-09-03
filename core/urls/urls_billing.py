from django.urls import include, path
from rest_framework.routers import DefaultRouter

from core.apps.billing.views import BillViewSet

router = DefaultRouter()
router.register(r"bill", BillViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
