from rest_framework import serializers

from core.apps.inventory.models import Category, DiscountConfig, Productstock


class CategorySerializer(serializers.ModelSerializer):
    supliers_name = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "description",
            "supliers",
            "supliers_name",
            "is_expired_applicable",
        ]
        read_only_fields = ["id", "supliers_name"]

    def validate(self, data):
        name = data.get("name")
        if (
            Category.objects.filter(name=name)
            .exclude(id=getattr(self.instance, "id", None))
            .exists()
        ):
            raise serializers.ValidationError(
                {"name": "This category name is already taken."}
            )
        return data

    def get_supliers_name(self, obj):
        return obj.supliers.name if obj.supliers else None


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
        extra_kwargs = {
            "supliers": {"required": True},
            "batch_number": {"required": True},
            "serial_number": {"required": True},
            "cost_price": {"required": True},
            "margin": {"required": True},
            "stock": {"required": True},
            "category": {"required": True},
        }

    def validate(self, data):
        category = data.get("category") or getattr(self.instance, "category", None)
        expires_at = data.get("expires_at") or getattr(
            self.instance, "expires_at", None
        )

        # If category requires expiry, product must have expiry date
        if category and category.is_expired_applicable and not expires_at:
            raise serializers.ValidationError(
                {
                    "expires_at": "This product must have an expiry date because its category is expiry applicable."
                }
            )

        # If category does NOT require expiry, product must not have expiry date
        if category and not category.is_expired_applicable and expires_at:
            raise serializers.ValidationError(
                {
                    "expires_at": "Expiry date should not be set since this category is not expiry applicable."
                }
            )

        return data

    def get_category_name(self, obj):
        return obj.category.name if obj.category else None

    def get_supliers_name(self, obj):
        return obj.supliers.name if obj.supliers else None


class DiscountConfigSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.name", read_only=True)

    class Meta:
        model = DiscountConfig
        fields = [
            "id",
            "product",
            "product_name",
            "percentage",
            "maximum_quantity",
            "minimum_quantity",
        ]

    def validate(self, data):
        min_q = data.get("minimum_quantity")
        max_q = data.get("maximum_quantity")

        if min_q is not None and max_q is not None and min_q > max_q:
            raise serializers.ValidationError(
                {
                    "maximum_quantity": "Maximum quantity must be greater than or equal to minimum quantity."
                }
            )
        return data
