from django.urls import path
from . import views
from .api_views import api_check_in, api_check_out

urlpatterns = [
    # -----------------
    # Web views
    # -----------------
    path('check-in/', views.check_in, name='check_in'),
    path('check-out/', views.check_out, name='check_out'),

    # Monthly reports
    path(
        'report/monthly/',
        views.staff_monthly_report,
        name='staff_monthly_report'
    ),
    path(
        'report/monthly/<int:user_id>/',
        views.admin_monthly_report,
        name='admin_monthly_report'
    ),

    # -----------------
    # API endpoints
    # -----------------
    path('api/check-in/', api_check_in, name='api_check_in'),
    path('api/check-out/', api_check_out, name='api_check_out'),
]
