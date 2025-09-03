from decimal import Decimal

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone

from core.apps.Supliers.models import Supliers


class Category(models.Model):
    class Meta:
        db_table = "category"

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    supliers = models.ForeignKey(
        Supliers,
        on_delete=models.CASCADE,
        related_name="categories",
        null=True,
        blank=True,
    )
    is_expired_applicable = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Productstock(models.Model):
    class Meta:
        db_table = "product_stock"

    name = models.CharField(max_length=100)
    product_code = models.CharField(max_length=100, unique=True, null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    supliers = models.ForeignKey(
        Supliers,
        on_delete=models.CASCADE,
        related_name="products",
        null=True,
        blank=True,
    )
    batch_number = models.CharField(max_length=100, blank=True, null=True, unique=True)
    serial_number = models.CharField(max_length=100, blank=True, null=True, unique=True)
    cost_price = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal("0.00"))]
    )
    stock = models.PositiveIntegerField()
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="products"
    )
    margin = models.DecimalField(
        max_digits=5, decimal_places=2, validators=[MinValueValidator(Decimal("0.00"))]
    )
    expires_at = models.DateTimeField(null=True, blank=True)
    is_deleted = models.BooleanField(default=False)

    def soft_delete(self):
        self.is_deleted = True
        self.save()

    @property
    def is_expired(self):
        return self.expires_at and self.expires_at <= timezone.now()

    def clean(self):
        # Cost and margin validation
        if self.cost_price is not None and self.cost_price < 0:
            raise ValidationError("Cost price cannot be negative.")
        if self.margin is not None and self.margin < 0:
            raise ValidationError("Margin cannot be negative.")

        # Expiry validation based on category
        if (
            self.category
            and self.category.is_expired_applicable
            and not self.expires_at
        ):
            raise ValidationError(
                {
                    "expires_at": "This product must have an expiry date because its category is expired applicable."
                }
            )

        # If category is not expired applicable, clear product expiry
        if self.category and not self.category.is_expired_applicable:
            self.expires_at = None

    def __str__(self):
        return self.name


class DiscountConfig(models.Model):
    class Meta:
        db_table = "discount_config"

    product = models.ForeignKey(
        Productstock, on_delete=models.CASCADE, related_name="discounts"
    )
    percentage = models.DecimalField(max_digits=5, decimal_places=2)
    maximum_quantity = models.IntegerField()
    minimum_quantity = models.IntegerField()

    def __str__(self):
        return f"{self.percentage}% off on {self.product.name}"
