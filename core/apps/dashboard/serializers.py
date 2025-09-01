from rest_framework import serializers

class ProductStockSoldSerializer(serializers.Serializer):
    product_name = serializers.CharField()
    stock = serializers.IntegerField()
    sold = serializers.IntegerField()

class WeeklyProfitDaySerializer(serializers.Serializer):
    date = serializers.CharField()
    weekday = serializers.CharField()
    profit = serializers.CharField()

class MonthlyProfitDateSerializer(serializers.Serializer):
    date = serializers.CharField()
    profit = serializers.CharField()

class YearlyProfitMonthSerializer(serializers.Serializer):
    month = serializers.CharField()
    profit = serializers.CharField()

class WeeklySalesDaySerializer(serializers.Serializer):
    date = serializers.CharField()
    weekday = serializers.CharField()
    sales = serializers.CharField()

class MonthlySalesDateSerializer(serializers.Serializer):
    date = serializers.CharField()
    sales = serializers.CharField()

class YearlySalesMonthSerializer(serializers.Serializer):
    month = serializers.CharField()
    sales = serializers.CharField()

class DashboardStatsSerializer(serializers.Serializer):
    total_sales = serializers.DecimalField(max_digits=10, decimal_places=2)
    total_profit = serializers.DecimalField(max_digits=10, decimal_places=2)
    total_stocks = serializers.IntegerField()
    products = ProductStockSoldSerializer(many=True)
    profit_daily = serializers.DecimalField(max_digits=10, decimal_places=2)
    profit_weekly = serializers.DecimalField(max_digits=10, decimal_places=2)
    profit_monthly = serializers.DecimalField(max_digits=10, decimal_places=2)
    weekly_profit_by_day = WeeklyProfitDaySerializer(many=True)
    monthly_profit_by_date = MonthlyProfitDateSerializer(many=True)
    yearly_profit_by_month = YearlyProfitMonthSerializer(many=True)
    profit_yearly = serializers.DecimalField(max_digits=10, decimal_places=2)
    sales_daily = serializers.DecimalField(max_digits=10, decimal_places=2)
    sales_weekly = serializers.DecimalField(max_digits=10, decimal_places=2)
    sales_monthly = serializers.DecimalField(max_digits=10, decimal_places=2)
    sales_yearly = serializers.DecimalField(max_digits=10, decimal_places=2)
    weekly_sales_by_day = WeeklySalesDaySerializer(many=True)
    monthly_sales_by_date = MonthlySalesDateSerializer(many=True)
    yearly_sales_by_month = YearlySalesMonthSerializer(many=True)
