from django.db import models
from django.contrib.auth.models import User


class StaffProfile(models.Model):

    STAFF_CATEGORY_CHOICES = [
        ('SECURITY', 'Security'),
        ('HOUSEKEEPING', 'Housekeeping'),
        ('CANTEEN', 'Canteen'),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="staffprofile"
    )

    mobile_number = models.CharField(
        max_length=10,
        help_text="Enter staff mobile number"
    )

    staff_category = models.CharField(
        max_length=20,
        choices=STAFF_CATEGORY_CHOICES
    )

    is_active_staff = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username} - {self.staff_category} - {self.mobile_number}"
