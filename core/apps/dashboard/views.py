from django.http import JsonResponse
from django.views.decorators.http import require_GET
from core.apps.billing.models import Bill, BillingItem
from core.apps.inventory.models import Productstock
from django.db import models
from core.apps.dashboard.serializers import DashboardStatsSerializer

@require_GET
def dashboard_stats(request):
    # Total Sales: sum of all billing items' unit_total
    total_sales = BillingItem.objects.aggregate(
        total_sales_sum=models.Sum('unit_total')
    )['total_sales_sum'] or 0

    # Total Profit: sum of (unit_price - cost_price) * quantity for all billing items
    total_profit = BillingItem.objects.select_related('product_id').annotate(
        profit_per_item=models.F('unit_price') - models.F('product_id__cost_price'),
        total_profit=models.ExpressionWrapper(
            (models.F('unit_price') - models.F('product_id__cost_price')) * models.F('quantity'),
            output_field=models.DecimalField()
        )
    ).aggregate(
        total_profit_sum=models.Sum('total_profit')
    )['total_profit_sum'] or 0

    # Total Product Stocks: sum of all Productstock's stock
    total_stocks = Productstock.objects.aggregate(
        total_stock=models.Sum('stock')
    )['total_stock'] or 0

    # Product names and stocks
    products = Productstock.objects.values('name', 'stock')
    product_list = [
        {'product_name': p['name'], 'stock': p['stock']}
        for p in products
    ]
    print(product_list)

    data = {
        'total_sales': total_sales,
        'total_profit': total_profit,
        'total_stocks': total_stocks,
        'products': product_list,
    }
    serializer = DashboardStatsSerializer(data)
    return JsonResponse(serializer.data)