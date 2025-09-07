from decimal import Decimal
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone

from core.apps.Supliers.models import Supliers


class UnitType(models.Model):
    unit = models.CharField(max_length=15)
    description = models.TextField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        # If a deleted unit with the same name exists, reactivate it
        if self.pk is None:
            existing = UnitType.objects.filter(unit=self.unit, is_deleted=True).first()
            if existing:
                existing.is_deleted = False
                existing.save()
                self.pk = existing.pk  # Use the reactivated unit's pk
                self.is_deleted = False
                return  # Do not create a new row, just update the old one
            self.is_deleted = False
        super().save(*args, **kwargs)

    def soft_delete(self):
        self.is_deleted = True
        self.save()

    def __str__(self):
        return self.unit

    class Meta:
        db_table = "unit_type"


class Category(models.Model):
    class Meta:
        db_table = "category"

    name = models.CharField(max_length=100)
    is_expired_applicable = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)

    def soft_delete(self):
        self.is_deleted = True
        self.save()

    def __str__(self):
        return self.name


class Productstock(models.Model):
    class Meta:
        db_table = "product_stock"
    unit = models.ForeignKey(UnitType, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    product_code = models.CharField(max_length=100, unique=True, null=True, blank=True)
    supliers = models.ForeignKey(
        Supliers,
        on_delete=models.CASCADE,
        related_name="products",
        null=True,
        blank=True,
    )
    batch_number = models.CharField(max_length=100, blank=True, null=True)
    serial_number = models.CharField(max_length=100, blank=True, null=True)
    cost_price = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal("0.00"))]
    )
    stock = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0)])
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="products"
    )
    margin = models.DecimalField(
        max_digits=5, decimal_places=2, validators=[MinValueValidator(Decimal("0.00"))]
    )
    expires_at = models.DateTimeField(null=True, blank=True)
    is_deleted = models.BooleanField(default=False)
    base_unit = models.ForeignKey(UnitType, on_delete=models.CASCADE, related_name="products_base_unit", null=True, blank=True)

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

        # Serial number uniqueness validation (when provided)
        if self.serial_number:
            existing_serial = Productstock.objects.filter(
                serial_number=self.serial_number,
                is_deleted=False
            ).exclude(pk=self.pk if self.pk else None)
            
            if existing_serial.exists():
                raise ValidationError(
                    {"serial_number": "This serial number already exists."}
                )

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

    def generate_batch_number(self):
        """Generate batch number in format YYYYMMDD-XXX where XXX is sequential counter"""
        from datetime import datetime
        
        today = datetime.now()
        date_prefix = today.strftime("%Y%m%d")
        
        # Find existing batch numbers for today
        existing_batches = Productstock.objects.filter(
            batch_number__startswith=date_prefix,
            is_deleted=False
        ).exclude(pk=self.pk if self.pk else None)
        
        # Generate next sequential number
        if existing_batches.exists():
            # Extract the highest counter for today
            counters = []
            for batch in existing_batches:
                try:
                    counter_part = batch.batch_number.split('-')[-1]
                    counters.append(int(counter_part))
                except (ValueError, IndexError):
                    continue
            
            next_counter = max(counters) + 1 if counters else 1
        else:
            next_counter = 1
        
        return f"{date_prefix}-{next_counter:03d}"

    def save(self, *args, **kwargs):
        if not self.batch_number:
            self.batch_number = self.generate_batch_number()
        super().save(*args, **kwargs)
    def __str__(self):
        return self.name

class UnitTypeConfigurations(models.Model):
    class Meta:
        db_table = "unit_configurations"
    product = models.ForeignKey(Productstock, on_delete=models.CASCADE, null=True, blank=True)
    unit_type = models.ForeignKey(UnitType, on_delete=models.CASCADE, null=True, blank=True, related_name="configUnit_type")  

    # Example: if unit_type = Carton and conversion_per_unit = 24 → 1 Carton = 24 Pieces
    conversion_per_unit = models.DecimalField(max_digits=10, decimal_places=2, default=1)
    conversion_unit_name = models.ForeignKey(UnitType, on_delete=models.CASCADE, null=True, blank=True, related_name='conversion_unit_configurations')  # e.g., "pieces", "boxes"
    is_deleted = models.BooleanField(default=False)

    def soft_delete(self):
        self.is_deleted = True
        self.save()

    def __str__(self):
        return f"{self.conversion_per_unit} {self.unit_type.unit if self.unit_type else 'Unknown'}"
