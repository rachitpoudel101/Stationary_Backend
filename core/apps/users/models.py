from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.crypto import get_random_string
class Users(AbstractUser):
    class RolesChoices(models.TextChoices):
        ADMIN = "admin"
        STAFF = "staff"
        CUSTOMER = "customer"
    
    role = models.CharField(max_length=50, choices=RolesChoices.choices)
    is_super = models.BooleanField(default=False)
    created_by = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_users",
    )
    is_deleted = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username