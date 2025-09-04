from django.urls import include, path
from rest_framework.routers import DefaultRouter

from core.apps.inventory.views import CategoryViewSet, ProductViewSet, UnitCreateViewSet

router = DefaultRouter()
router.register(r"unit", UnitCreateViewSet, basename="unit")
router.register(r"category", CategoryViewSet, basename="category")
router.register(r"product", ProductViewSet, basename="product")
# router.register(r"discount-config",DiscountViewSet, basename="discount-config")


urlpatterns = [
    path("", include(router.urls)),
]
