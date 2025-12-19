from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

<<<<<<< HEAD
=======
from rest_framework_simplejwt.views import TokenRefreshView
from accounts.jwt_views import CustomTokenObtainPairView


>>>>>>> 5b42ec600abca25bd70067555f40506ef26bf8fd
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
=======
    path('leaves/', include('leaves.urls')),
     path('locations/', include('locations.urls')), 

    # JWT Authentication (CUSTOM)
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
>>>>>>> 5b42ec600abca25bd70067555f40506ef26bf8fd
]
