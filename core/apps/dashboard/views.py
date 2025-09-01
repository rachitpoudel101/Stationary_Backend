from django.http import JsonResponse
from django.views.decorators.http import require_GET
from core.apps.billing.models import Bill, BillingItem
from core.apps.inventory.models import Productstock
from django.db import models
from core.apps.dashboard.serializers import DashboardStatsSerializer
from django.utils import timezone
from datetime import timedelta
from calendar import monthrange
import calendar

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

    # Profit by period
    now = timezone.now().date()
    # Daily
    daily_profit = BillingItem.objects.filter(
        bill_id__date=now
    ).select_related('product_id').annotate(
        total_profit=models.ExpressionWrapper(
            (models.F('unit_price') - models.F('product_id__cost_price')) * models.F('quantity'),
            output_field=models.DecimalField()
        )
    ).aggregate(
        profit=models.Sum('total_profit')
    )['profit'] or 0

    # Weekly (current week: Monday to Sunday)
    week_start = now - timedelta(days=now.weekday())
    week_end = week_start + timedelta(days=6)
    weekly_profit = BillingItem.objects.filter(
        bill_id__date__range=[week_start, week_end]
    ).select_related('product_id').annotate(
        total_profit=models.ExpressionWrapper(
            (models.F('unit_price') - models.F('product_id__cost_price')) * models.F('quantity'),
            output_field=models.DecimalField()
        )
    ).aggregate(
        profit=models.Sum('total_profit')
    )['profit'] or 0

    # Weekly breakdown by day with weekday name and formatted profit
    weekly_profit_by_day = []
    for i in range(7):
        day = week_start + timedelta(days=i)
        day_profit = BillingItem.objects.filter(
            bill_id__date=day
        ).select_related('product_id').annotate(
            total_profit=models.ExpressionWrapper(
                (models.F('unit_price') - models.F('product_id__cost_price')) * models.F('quantity'),
                output_field=models.DecimalField()
            )
        ).aggregate(
            profit=models.Sum('total_profit')
        )['profit'] or 0
        # Format profit as string with 2 decimal places
        profit_str = f"{day_profit:.2f}"
        weekly_profit_by_day.append({
            'date': day.isoformat(),
            'weekday': day.strftime('%A'),
            'profit': profit_str
        })

    # Monthly (current month)
    monthly_profit = BillingItem.objects.filter(
        bill_id__date__year=now.year,
        bill_id__date__month=now.month
    ).select_related('product_id').annotate(
        total_profit=models.ExpressionWrapper(
            (models.F('unit_price') - models.F('product_id__cost_price')) * models.F('quantity'),
            output_field=models.DecimalField()
        )
    ).aggregate(
        profit=models.Sum('total_profit')
    )['profit'] or 0

    # Monthly breakdown by date
    days_in_month = monthrange(now.year, now.month)[1]
    monthly_profit_by_date = []
    for day_num in range(1, days_in_month + 1):
        day = now.replace(day=day_num)
        day_profit = BillingItem.objects.filter(
            bill_id__date=day
        ).select_related('product_id').annotate(
            total_profit=models.ExpressionWrapper(
                (models.F('unit_price') - models.F('product_id__cost_price')) * models.F('quantity'),
                output_field=models.DecimalField()
            )
        ).aggregate(
            profit=models.Sum('total_profit')
        )['profit'] or 0
        profit_str = f"{day_profit:.2f}"
        monthly_profit_by_date.append({
            'date': day.isoformat(),
            'profit': profit_str
        })

    # Yearly (current year)
    yearly_profit = BillingItem.objects.filter(
        bill_id__date__year=now.year
    ).select_related('product_id').annotate(
        total_profit=models.ExpressionWrapper(
            (models.F('unit_price') - models.F('product_id__cost_price')) * models.F('quantity'),
            output_field=models.DecimalField()
        )
    ).aggregate(
        profit=models.Sum('total_profit')
    )['profit'] or 0

    # Yearly breakdown by month
    yearly_profit_by_month = []
    for month_num in range(1, 13):
        month_profit = BillingItem.objects.filter(
            bill_id__date__year=now.year,
            bill_id__date__month=month_num
        ).select_related('product_id').annotate(
            total_profit=models.ExpressionWrapper(
                (models.F('unit_price') - models.F('product_id__cost_price')) * models.F('quantity'),
                output_field=models.DecimalField()
            )
        ).aggregate(
            profit=models.Sum('total_profit')
        )['profit'] or 0
        profit_str = f"{month_profit:.2f}"
        yearly_profit_by_month.append({
            'month': calendar.month_name[month_num],
            'profit': profit_str
        })

    # Total Sales breakdowns
    # Daily
    daily_sales = BillingItem.objects.filter(
        bill_id__date=now
    ).aggregate(
        sales=models.Sum('unit_total')
    )['sales'] or 0

    # Weekly (current week: Monday to Sunday)
    weekly_sales = BillingItem.objects.filter(
        bill_id__date__range=[week_start, week_end]
    ).aggregate(
        sales=models.Sum('unit_total')
    )['sales'] or 0

    # Weekly breakdown by day
    weekly_sales_by_day = []
    for i in range(7):
        day = week_start + timedelta(days=i)
        day_sales = BillingItem.objects.filter(
            bill_id__date=day
        ).aggregate(
            sales=models.Sum('unit_total')
        )['sales'] or 0
        sales_str = f"{day_sales:.2f}"
        weekly_sales_by_day.append({
            'date': day.isoformat(),
            'weekday': day.strftime('%A'),
            'sales': sales_str
        })

    # Monthly (current month)
    monthly_sales = BillingItem.objects.filter(
        bill_id__date__year=now.year,
        bill_id__date__month=now.month
    ).aggregate(
        sales=models.Sum('unit_total')
    )['sales'] or 0

    # Monthly breakdown by date
    monthly_sales_by_date = []
    for day_num in range(1, days_in_month + 1):
        day = now.replace(day=day_num)
        day_sales = BillingItem.objects.filter(
            bill_id__date=day
        ).aggregate(
            sales=models.Sum('unit_total')
        )['sales'] or 0
        sales_str = f"{day_sales:.2f}"
        monthly_sales_by_date.append({
            'date': day.isoformat(),
            'sales': sales_str
        })

    # Yearly (current year)
    yearly_sales = BillingItem.objects.filter(
        bill_id__date__year=now.year
    ).aggregate(
        sales=models.Sum('unit_total')
    )['sales'] or 0

    # Yearly breakdown by month
    yearly_sales_by_month = []
    for month_num in range(1, 13):
        month_sales = BillingItem.objects.filter(
            bill_id__date__year=now.year,
            bill_id__date__month=month_num
        ).aggregate(
            sales=models.Sum('unit_total')
        )['sales'] or 0
        sales_str = f"{month_sales:.2f}"
        yearly_sales_by_month.append({
            'month': calendar.month_name[month_num],
            'sales': sales_str
        })

    # Total Product Stocks: sum of all Productstock's stock
    total_stocks = Productstock.objects.aggregate(
        total_stock=models.Sum('stock')
    )['total_stock'] or 0

    # Product names and stocks
    products = Productstock.objects.values('id', 'name', 'stock')
    product_ids = [p['id'] for p in products]

    # Calculate total sold quantity per product
    sold_qty_map = {
        item['product_id']: item['total_sold']
        for item in BillingItem.objects.filter(product_id__in=product_ids)
        .values('product_id')
        .annotate(total_sold=models.Sum('quantity'))
    }

    product_list = [
        {
            'product_name': p['name'],
            'stock': p['stock'],
            'sold': sold_qty_map.get(p['id'], 0)
        }
        for p in products
    ]

    # Top-selling product for the week
    week_top = (
        BillingItem.objects
        .filter(bill_id__date__range=[week_start, week_end])
        .values('product_id')
        .annotate(total_sold=models.Sum('quantity'))
        .order_by('-total_sold')
        .first()
    )
    week_top_product = None
    if week_top:
        product = Productstock.objects.filter(id=week_top['product_id']).first()
        if product:
            week_top_product = {
                'product_name': product.name,
                'sold_quantity': week_top['total_sold'],
                'stock': product.stock
            }

    # Top-selling product for the month
    month_top = (
        BillingItem.objects
        .filter(bill_id__date__year=now.year, bill_id__date__month=now.month)
        .values('product_id')
        .annotate(total_sold=models.Sum('quantity'))
        .order_by('-total_sold')
        .first()
    )
    month_top_product = None
    if month_top:
        product = Productstock.objects.filter(id=month_top['product_id']).first()
        if product:
            month_top_product = {
                'product_name': product.name,
                'sold_quantity': month_top['total_sold'],
                'stock': product.stock
            }

    # Top-selling product for the year
    year_top = (
        BillingItem.objects
        .filter(bill_id__date__year=now.year)
        .values('product_id')
        .annotate(total_sold=models.Sum('quantity'))
        .order_by('-total_sold')
        .first()
    )
    year_top_product = None
    if year_top:
        product = Productstock.objects.filter(id=year_top['product_id']).first()
        if product:
            year_top_product = {
                'product_name': product.name,
                'sold_quantity': year_top['total_sold'],
                'stock': product.stock
            }

    data = {
        'total_sales': total_sales,
        'total_profit': total_profit,
        'total_stocks': total_stocks,
        'products': product_list,
        'profit_daily': daily_profit,
        'profit_weekly': weekly_profit,
        'profit_monthly': monthly_profit,
        'weekly_profit_by_day': weekly_profit_by_day,
        'monthly_profit_by_date': monthly_profit_by_date,
        'yearly_profit_by_month': yearly_profit_by_month,
        'profit_yearly': yearly_profit,
        'sales_daily': daily_sales,
        'sales_weekly': weekly_sales,
        'sales_monthly': monthly_sales,
        'sales_yearly': yearly_sales,
        'weekly_sales_by_day': weekly_sales_by_day,
        'monthly_sales_by_date': monthly_sales_by_date,
        'yearly_sales_by_month': yearly_sales_by_month,
        'week_top_product': week_top_product,
        'month_top_product': month_top_product,
        'year_top_product': year_top_product,
    }
    serializer = DashboardStatsSerializer(data)
    return JsonResponse(serializer.data)

@require_GET
def product_sales_list(request):
    # Get all products with stock
    products = Productstock.objects.values('id', 'name', 'stock')
    product_ids = [p['id'] for p in products]

    # Aggregate sold quantity per product
    sold_qty_map = {
        item['product_id']: item['total_sold']
        for item in BillingItem.objects.filter(product_id__in=product_ids)
        .values('product_id')
        .annotate(total_sold=models.Sum('quantity'))
    }

    result = [
        {
            'product_name': p['name'],
            'stock': p['stock'],
            'sold_quantity': sold_qty_map.get(p['id'], 0)
        }
        for p in products
    ]

    return JsonResponse({'products': result})