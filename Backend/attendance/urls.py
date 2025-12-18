from django.urls import path
from . import views
from .api_views import api_check_in, api_check_out

urlpatterns = [
    path('check-in/', views.check_in, name='check_in'),
    path('check-out/', views.check_out, name='check_out'),
    path('api/check-in/', api_check_in),
    path('api/check-out/', api_check_out),
]
