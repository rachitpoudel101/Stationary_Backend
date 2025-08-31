from rest_framework import serializers

class DashboardStatsSerializer(serializers.Serializer):
    total_sales = serializers.DecimalField(max_digits=12, decimal_places=2)
    total_profit = serializers.DecimalField(max_digits=12, decimal_places=2)
    total_stocks = serializers.IntegerField()
    products = serializers.ListField(child=serializers.DictField())
