
from rest_framework import viewsets

from core.apps.inventory.models import Category, DiscountConfig, Productstock
from core.apps.inventory.serializers.serializers import (
    CategorySerializer,
    DiscountConfigSerializer,
    ProductStockSerializer,
)
from core.apps.users.permissions.permissions import IsAdmin, IsSuperAdmin


class CategoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing product categories.
    Only SuperAdmin and Admin can create/update/delete.
    """

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsSuperAdmin | IsAdmin]

    def get_queryset(self):
        """
        Optionally filter categories by supliers or expired_applicable flag.
        Example: /api/categories/?is_expired_applicable=true
        """
        queryset = super().get_queryset()
        is_expired_applicable = self.request.query_params.get("is_expired_applicable")
        if is_expired_applicable is not None:
            queryset = queryset.filter(
                is_expired_applicable=is_expired_applicable.lower() == "true"
            )
        return queryset


class ProductViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing products.
    SuperAdmin, Admin, and Staff can access.
    """

    queryset = Productstock.objects.all()
    serializer_class = ProductStockSerializer
    permission_classes = [IsSuperAdmin | IsAdmin]

    def get_queryset(self):
        """
        Optionally filter products by category or supliers.
        Example: /api/products/?category=1&supliers=2
        """
        queryset = super().get_queryset()
        category = self.request.query_params.get("category")
        supliers = self.request.query_params.get("supliers")

        if category:
            queryset = queryset.filter(category_id=category)
        if supliers:
            queryset = queryset.filter(supliers_id=supliers)

        return queryset


class DiscountViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing discount configurations.
    Only Admins allowed.
    """

    queryset = DiscountConfig.objects.all()
    serializer_class = DiscountConfigSerializer
    permission_classes = [IsAdmin | IsSuperAdmin]

    def get_queryset(self):
        """
        Optionally filter discounts by product.
        Example: /api/discounts/?product=5
        """
        queryset = super().get_queryset()
        product = self.request.query_params.get("product")
        if product:
            queryset = queryset.filter(product_id=product)
        return queryset
