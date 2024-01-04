from django.urls import path
from . import views

app_name = 'co_admin_app'

urlpatterns = [
    path('',views.home,name = 'home'),
]