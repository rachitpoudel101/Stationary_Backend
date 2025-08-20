from rest_framework import serializers
from django.core.exceptions import ValidationError
from core.apps.billing.models import Bill, BillingItem
from core.apps.inventory.serializers.serializers import ProductStockSerializer

class BillingItemSerializer(serializers.ModelSerializer):
    product_name = serializers.PrimaryKeyRelatedField(queryset=ProductStockSerializer.Meta.model.objects.all())
    bill = serializers.PrimaryKeyRelatedField(queryset=Bill.objects.all(), required=False)

    class Meta:
        model = BillingItem
        fields = [
            "bill",
            "product_name",
            "quantity",
            "unit_price",
            "selling_price",
            "discount_amount",
            "unit_total",
        ]

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['product_name'] = ProductStockSerializer(instance.product_name).data
        return rep

class BillSerializer(serializers.ModelSerializer):
    items = BillingItemSerializer(many=True, source='bill')

    class Meta:
        model = Bill
        fields = [
            "id",
            "customer_Name",
            "customer_address",
            "date",
            "payment_method",
            "actual_amount",
            "recived_amount",
            "grand_total",
            "items",
        ]

    def create(self, validated_data):
        items_data = validated_data.pop('bill', [])
        bill = Bill.objects.create(**validated_data)
        for item_data in items_data:
            product = item_data['product_name']
            quantity = item_data['quantity']
            if quantity < 0:
                raise ValidationError("Quantity cannot be negative.")
            if product.stock < quantity:
                raise ValidationError(f"Not enough stock for product '{product.name}'. Available: {product.stock}, Requested: {quantity}")
            product.stock -= quantity
            if product.stock < 0:
                raise ValidationError(f"Stock for product '{product.name}' cannot be negative after billing.")
            product.save()
            if item_data.get('unit_price', 0) < 0 or item_data.get('selling_price', 0) < 0 or item_data.get('discount_amount', 0) < 0 or item_data.get('unit_total', 0) < 0:
                raise ValidationError("Amounts cannot be negative.")
            BillingItem.objects.create(bill=bill, **item_data)
        return bill

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['items'] = BillingItemSerializer(instance.bill.all(), many=True).data
        return rep