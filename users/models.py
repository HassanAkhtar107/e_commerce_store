from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

USER_TYPE = (
    ("USER", "USER"),
    ("ADMIN", "ADMIN"),
)


class User(AbstractUser):
    """
    Custom User Model for E-Commerce Store
    """
    name = models.CharField(_("Name of User"), blank=True, max_length=255)
    first_name = None  # type: ignore
    last_name = None  # type: ignore
    is_verified = models.BooleanField(default=False)
    otp_counter = models.IntegerField(default=0)
    user_type = models.CharField(choices=USER_TYPE, max_length=10, null=True, blank=True, default="USER")
    stripe_customer_id = models.CharField(max_length=255, null=True, blank=True)

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile", null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    profile_photo = models.FileField(upload_to="profiles/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Profile of {self.user.username}"


class ShippingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="shipping_addresses")
    full_name = models.CharField(max_length=255)
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100, default="USA")
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - {self.city}, {self.country}"
