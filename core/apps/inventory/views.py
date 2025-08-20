import traceback
from rest_framework import viewsets
from core.apps.users.permissions.permissions import IsSuperAdmin, IsAdmin
from core.apps.inventory.models import Category, Productstock, DiscountConfig
from core.apps.inventory.serializers.serializers import CategoryCreateSerializer , ProductStockSerializer, DiscountConfigSerializer
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategoryCreateSerializer
    permission_classes = [IsSuperAdmin | IsAdmin]

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Productstock.objects.all()
    serializer_class = ProductStockSerializer
    permission_classes = [IsSuperAdmin | IsAdmin]

class DiscountViewSet(viewsets.ModelViewSet):
    queryset = DiscountConfig.objects.all()
    serializer_class = DiscountConfigSerializer
    permission_classes = [IsAdmin]