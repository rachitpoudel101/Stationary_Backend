from rest_framework import viewsets, status
from rest_framework.response import Response

from core.apps.inventory.models import Category, Productstock, UnitCreate
from core.apps.inventory.serializers.serializers import (
    CategorySerializer,
    # DiscountConfigSerializer,
    ProductStockSerializer,
    UnitCreateSerializer,
)
from core.apps.users.permissions.permissions import IsAdmin, IsSuperAdmin


class UnitCreateViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing product units.
    Only SuperAdmin and Admin can create/update/delete.
    """

    queryset = UnitCreate.objects.filter(is_deleted=False)
    serializer_class = UnitCreateSerializer
    permission_classes = [IsSuperAdmin | IsAdmin]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.soft_delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_queryset(self):
        """
        Optionally filter units by unit name.
        Example: /units/?unit=kg
        """
        queryset = super().get_queryset()
        unit = self.request.query_params.get("unit")
        if unit:
            queryset = queryset.filter(unit__icontains=unit)
        return queryset


class CategoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing product categories.
    Only SuperAdmin and Admin can create/update/delete.
    """

    queryset = Category.objects.filter(is_deleted=False)
    serializer_class = CategorySerializer
    permission_classes = [IsSuperAdmin | IsAdmin]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.soft_delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

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

    queryset = Productstock.objects.filter(is_deleted=False)
    serializer_class = ProductStockSerializer
    permission_classes = [IsSuperAdmin | IsAdmin]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.soft_delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

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


# class DiscountViewSet(viewsets.ModelViewSet):
#     """
#     ViewSet for managing discount configurations.
#     Only Admins allowed.
#     """

#     queryset = DiscountConfig.objects.filter(is_deleted=False)
#     serializer_class = DiscountConfigSerializer
#     permission_classes = [IsAdmin | IsSuperAdmin]

#     def destroy(self, request, *args, **kwargs):
#         instance = self.get_object()
#         instance.soft_delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

#     def get_queryset(self):
#         """
#         Optionally filter discounts by product.
#         Example: /api/discounts/?product=5
#         """
#         queryset = super().get_queryset()
#         product = self.request.query_params.get("product")
#         if product:
#             queryset = queryset.filter(product_id=product)
#         return queryset
