from django.urls import path
from .api_views import location_ping

urlpatterns = [
    path('api/ping/', location_ping),
]
