from django.urls import path
from . import views
<<<<<<< HEAD
from .api_views import api_check_in, api_check_out

urlpatterns = [
    # -----------------
    # Web views
=======
from .api_views import (
    api_check_in,
    api_check_out,
    my_attendance,
)

urlpatterns = [
    # -----------------
    # Web views (HTML)
>>>>>>> 2d3a47b01e6dcc220f597c86fd72091ea67ed34d
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
<<<<<<< HEAD
=======
    path('my-attendance/', my_attendance, name='my_attendance'),
>>>>>>> 2d3a47b01e6dcc220f597c86fd72091ea67ed34d
]
