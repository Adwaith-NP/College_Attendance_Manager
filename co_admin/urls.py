from django.urls import path
from . import views

app_name = 'co_admin_app'

urlpatterns = [
    path('',views.home,name = 'home'),
    path('faculty_registration/',views.faculty_registration,name="faculty_registration"),
    path('add_student/<str:access_code>/',views.addStudent,name='add_student'),
    path('alote_subject_to_teacher/<int:teacher_id>/',views.alote_subject_to_teacher,name='alote_subject_to_teacher'),
    path('sem_and_sec/',views.sem_and_sec,name="sem_and_sec"),
    path('aditional_attendance/',views.aditional_attendance,name='aditional_attendance'),
    path('return_all_subject/<str:teacherID>/',views.return_all_subject,name='return_all_subject'),
]