from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

def home_redirect(request):
    return redirect('/accounts/login/')


urlpatterns = [
    path('', home_redirect),

    # Admin
    path('admin/', admin.site.urls),

    # App URLs
    path('accounts/', include('accounts.urls')),
    path('attendance/', include('attendance.urls')),
    path('locations/', include('locations.urls')),
    path('leaves/', include('leaves.urls')),
   
]

