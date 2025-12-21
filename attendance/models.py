from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Attendance(models.Model):

    STATUS_CHOICES = [
        ('PRESENT', 'Present'),
        ('ABSENT', 'Absent'),
        ('AUTO_CHECKOUT', 'Auto Checked Out'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)

    check_in_time = models.DateTimeField(default=timezone.now)
    check_out_time = models.DateTimeField(null=True, blank=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='PRESENT'
    )

    auto_checked_out = models.BooleanField(default=False)
    admin_override = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'date')
        ordering = ['-date', '-check_in_time']

    def is_checked_out(self):
        return self.check_out_time is not None

    def __str__(self):
        return f"{self.user.username} - {self.date}"
