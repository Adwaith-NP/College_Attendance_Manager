from django.urls import path
from . import views

app_name = 'co_admin_app'

urlpatterns = [
    path('',views.home,name = 'home'),
    path('add_student/<str:access_code>/',views.addStudent,name='add_student'),
]