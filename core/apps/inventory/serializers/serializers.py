from rest_framework import serializers

from core.apps.inventory.models import Category, Productstock


class CategorySerializer(serializers.ModelSerializer):
    # supliers_name = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            # "supliers",
            # "supliers_name",
            "is_expired_applicable",
        ]
        read_only_fields = ["id"]

    def validate(self, data):
        name = data.get("name")
        if (
            Category.objects.filter(name=name, is_deleted=False)
            .exclude(id=getattr(self.instance, "id", None))
            .exists()
        ):
            raise serializers.ValidationError(
                {"name": "This category name is already taken."}
            )
        return data

    def get_supliers_name(self, obj):
        return obj.supliers.name if obj.supliers and not obj.supliers.is_deleted else None


class ProductStockSerializer(serializers.ModelSerializer):
    category_name = serializers.SerializerMethodField()
    supliers_name = serializers.SerializerMethodField()
    is_expired = serializers.ReadOnlyField()

    class Meta:
        model = Productstock
        fields = [
            "id",
            "category",
            "category_name",
            "product_code",
            "name",
            "supliers",
            "supliers_name",
            "batch_number",
            "serial_number",
            "cost_price",
            "margin",
            "description",
            "stock",
            "expires_at",
            "is_expired",
        ]
        read_only_fields = ["id", "category_name", "supliers_name", "is_expired", "batch_number", "expires_at"]
        extra_kwargs = {
            "supliers": {"required": True},
            "cost_price": {"required": True},
            "margin": {"required": True},
            "stock": {"required": True},
            "category": {"required": True},
            "serial_number": {"required": False},
        }

    def validate(self, data):
        return data

    def get_category_name(self, obj):
        return obj.category.name if obj.category and not obj.category.is_deleted else None

    def get_supliers_name(self, obj):
        return obj.supliers.name if obj.supliers and not obj.supliers.is_deleted else None


# class DiscountConfigSerializer(serializers.ModelSerializer):
#     product_name = serializers.CharField(source="product.name", read_only=True)

#     class Meta:
#         model = DiscountConfig
#         fields = [
#             "id",
#             "product",
#             "product_name",
#             "percentage",
#             "maximum_quantity",
#             "minimum_quantity",
#         ]

#     def validate(self, data):
#         min_q = data.get("minimum_quantity")
#         max_q = data.get("maximum_quantity")

#         if min_q is not None and max_q is not None and min_q > max_q:
#             raise serializers.ValidationError(
#                 {
#                     "maximum_quantity": "Maximum quantity must be greater than or equal to minimum quantity."
#                 }
#             )
#         return data
#         model = DiscountConfig
#         fields = [
#             "id",
#             "product",
#             "product_name",
#             "percentage",
#             "maximum_quantity",
#             "minimum_quantity",
#         ]

#     def validate(self, data):
#         min_q = data.get("minimum_quantity")
#         max_q = data.get("maximum_quantity")

#         if min_q is not None and max_q is not None and min_q > max_q:
#             raise serializers.ValidationError(
#                 {
#                     "maximum_quantity": "Maximum quantity must be greater than or equal to minimum quantity."
#                 }
#             )
#         return data
