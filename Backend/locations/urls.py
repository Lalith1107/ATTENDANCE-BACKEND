<<<<<<< HEAD
# leaves/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # path('', views.some_view),
=======
from django.urls import path
from .views import location_ping

urlpatterns = [
    path('ping/', location_ping, name='location_ping'),
>>>>>>> 34bf1fd343805b80f1646b3c53481642cb0acd9e
]
