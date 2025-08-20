from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from decimal import Decimal

class Category(models.Model):
    class Meta:
        db_table = "category"
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Productstock(models.Model):
    class Meta:
        db_table = "product_stock"

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    cost_price = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))]  
    )
    stock = models.PositiveIntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
    margin = models.DecimalField(
        max_digits=5, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))]  
    )

    def clean(self):
        if self.cost_price is not None and self.cost_price < 0:
            raise ValidationError("Cost price cannot be negative.")
        if self.margin is not None and self.margin < 0:
            raise ValidationError("Margin cannot be negative.")

    def __str__(self):
        return self.name

class DiscountConfig(models.Model):
    class Meta:
        db_table = "discount_config"

    product = models.ForeignKey(Productstock, on_delete=models.CASCADE, related_name="discounts")
    percentage = models.DecimalField(max_digits=5, decimal_places=2)
    maximum_quantity = models.IntegerField()
    minimum_quantity = models.IntegerField()

    def __str__(self):
        return f"{self.percentage}% off on {self.product.name}"
