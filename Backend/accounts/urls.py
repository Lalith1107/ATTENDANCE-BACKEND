from django.urls import path
from .views import login_view, staff_dashboard

urlpatterns = [
    path('login/', login_view, name='login'),
    path('staff/dashboard/', staff_dashboard, name='staff_dashboard'),
]
