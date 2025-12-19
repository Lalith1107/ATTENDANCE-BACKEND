from django.contrib import admin
from django.urls import path , include
from django.shortcuts import redirect
from .views import login_view, staff_dashboard
from .api_views import api_login
def home_redirect(request):
    return redirect('/accounts/login/')


urlpatterns = [
    path('', home_redirect),
    path('login/', login_view, name='login'),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('staff/dashboard/', staff_dashboard, name='staff_dashboard'),
    path('api/login/', api_login),
    
]
