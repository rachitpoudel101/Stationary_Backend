from rest_framework import serializers
from core.apps.inventory.models import Category, Productstock, DiscountConfig

class CategoryCreateSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True)
    description = serializers.CharField(write_only=True)
    
    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "description"
        ]

    def validate(self, data):
        name = data.get('name')
        if Category.objects.filter(name = name).exists():
            raise serializers.ValidationError({"category": "This category is already taken."})
        return data

    def create(self, validated_data):
            category = Category.objects.create(
                name=validated_data["name"],
                description=validated_data['description']  
            )
            category.save()
            return category

class ProductStockSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    category_name = serializers.SerializerMethodField()

    class Meta:
        model = Productstock
        fields = [ 'id','category','name', 'cost_price', 'margin', 'description', 'stock', 'category_name']

    def create(self, validated_data):
        return Productstock.objects.create(**validated_data)

    def get_category_name(self, obj):
        return obj.category.name

class DiscountConfigSerializer(serializers.ModelSerializer):
    percentage = serializers.DecimalField(max_digits=3, decimal_places=2)
    maximum_quantity = serializers.IntegerField()
    minimum_quantity = serializers.IntegerField()
    class Meta:
        model = DiscountConfig
        fields = [
            "product",
            "percentage",
            "maximum_quantity", 
            "minimum_quantity",
        ]
    def create(self, validated_data):
        return DiscountConfig.objects.create(**validated_data)
    