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
    # email = models.EmailField(unique=True, blank=False, null=False)
    # is_email_verified = models.BooleanField(default=False)
    # is_approved = models.BooleanField(default=False)
    # is_verified = models.BooleanField(default=False)
    # verification_token = models.CharField(max_length=100, blank=True, null=True)
    is_staff = models.BooleanField(default=False)
    created_by = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_users",
    )
    # reset_password_token = models.CharField(max_length=32, null=True, blank=True)
    # reset_password_expires = models.DateTimeField(null=True, blank=True)
    is_deleted = models.BooleanField(default=False)
    
    # def generate_verification_token(self):
    #     """Generate a new unique verification token."""
    #     self.verification_token = get_random_string(length=32)
    #     self.save()

    def save(self, *args, **kwargs):
        # Debug log to verify role before saving
        print(f"DEBUG: Saving user with username={self.username}, role={self.role}")
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username

#     @property
#     def unread_notifications_count(self):
#         return self.notifications.filter(is_read=False).count()

#     def is_allowed_to_login(self):
#         return self.is_active and not self.is_delete

# class UserProfile(models.Model):
#     user = models.OneToOneField(Users, on_delete=models.CASCADE)
#     avatar = models.ImageField(upload_to="avatars/", default="avatars/default.png")
#     phone = models.CharField(max_length=15, blank=True)
#     address = models.TextField(blank=True)

#     def __str__(self):
#         return f"{self.user.username}'s profile"

# class ActivityLog(models.Model):
#     admin = models.ForeignKey(
#         Users, on_delete=models.CASCADE, related_name="activities"
#     )
#     action = models.CharField(max_length=255)
#     timestamp = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.admin.username} - {self.action} at {self.timestamp}"