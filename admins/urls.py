from django.urls import path
from . import views

app_name = 'admin_app'

urlpatterns = [
    path('Admin/',views.admin,name = 'admin'),
    
]