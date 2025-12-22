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
<<<<<<< HEAD
    path('locations/', include('locations.urls')),  
]
=======
    path('locations/', include('locations.urls')),
    path('leaves/', include('leaves.urls')),
   
]

>>>>>>> 2d3a47b01e6dcc220f597c86fd72091ea67ed34d
