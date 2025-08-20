from django.db import models
from core.apps.inventory.models import Productstock

class Bill(models.Model):
    class Meta:
        db_table = "bill"
    class PaymentChoices(models.TextChoices):
        CASH = "cash"
        ONLINE = "online"
    customer_Name = models.CharField(max_length=50, default=None)
    customer_address = models.CharField(max_length=100, default=None)
    date = models.DateField(auto_now_add=True)
    payment_method = models.CharField(max_length=50, choices=PaymentChoices.choices)
    actual_amount = models.IntegerField()
    recived_amount = models.IntegerField()
    grand_total = models.DecimalField(max_digits=12, decimal_places=2)
    
    def __str__(self):
        return self.customer_Name

class BillingItem(models.Model):
    class Meta:
        db_table = "billing_Items"
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE, related_name="bill")
    product_name = models.ForeignKey(Productstock, on_delete=models.CASCADE, related_name="products_bill")
    quantity = models.IntegerField()
    unit_price = models.IntegerField()
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    unit_total = models.DecimalField(max_digits=12, decimal_places=2)
