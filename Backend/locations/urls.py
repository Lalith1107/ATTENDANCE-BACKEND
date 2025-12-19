from django.urls import path
from .views import location_ping

urlpatterns = [
    path('ping/', location_ping),
]
