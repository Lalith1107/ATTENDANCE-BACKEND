from django.contrib.auth.models import User
from django.db import models

class StaffProfile(models.Model):

    STAFF_CATEGORY_CHOICES = [
        ('SECURITY', 'Security'),
        ('HOUSEKEEPING', 'Housekeeping'),
        ('CANTEEN', 'Canteen'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    staff_category = models.CharField(
        max_length=20,
        choices=STAFF_CATEGORY_CHOICES
    )
    is_active_staff = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username} - {self.staff_category}"
