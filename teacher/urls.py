from django.urls import path
from . import views

app_name = 'teacher_app'

urlpatterns = [
    path('',views.home,name = 'home'),
    path('AddStudent/<str:sem_code>/<int:pk_sub>/',views.addStudentToTeacherDatabase,name='addStudent'),
    path('delete_student/<str:userID>/<str:sem_code>/<int:pk_sub>/',views.delete_student_from_teacher_database,name = 'delete_student'),
    path('addAttendance/<int:pk_sub>/',views.add_students_attandace,name='addAttendance')
]