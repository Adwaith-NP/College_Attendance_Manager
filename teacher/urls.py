from django.urls import path
from . import views

app_name = 'teacher_app'

urlpatterns = [
    path('',views.home,name = 'home'),
    path('AddStudent/<str:sem_code>/',views.addStudentToTeacherDatabase,name='addStudent')
]