<<<<<<< HEAD
=======
from django.db import models
from django.contrib.auth.models import User


class Geofence(models.Model):
    name = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()
    radius_meters = models.IntegerField()

    def __str__(self):
        return self.name


class LocationLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    latitude = models.FloatField()
    longitude = models.FloatField()
    is_inside_geofence = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.timestamp}"
>>>>>>> 2dc89573c841f1102ffb688bc25c72cd014c329f
