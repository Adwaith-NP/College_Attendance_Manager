from django.urls import path
from . import views

app_name = 'Authentication'

urlpatterns = [
    path('',views.login,name = 'Login'),
    path('Logout/',views.logout,name = 'logout'),
]