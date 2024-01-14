from django.shortcuts import render,redirect
from django.urls import reverse
from verify_user import verify
from Authentication.models import teacher_Authentication
from co_admin.models import subject,Semester
from student.models import student_Authentication
# Create your views here.

def user_deails(request):
    user_id = request.COOKIES.get('user_id')
    teacher_instance = teacher_Authentication.objects.filter(user_ID = user_id)
    teacher_subject = subject.objects.filter(teacher__in = teacher_instance)
    return [user_id,teacher_instance,teacher_subject]
def home(request):
    if verify(request):
        teacher_subject = user_deails(request)[2]
        data = {
            'subjects' : teacher_subject
        }
        return render(request,'teacher_view.html',data)
    else:
        return redirect(reverse('Authentication:Login'))
    
    
def addStudentToTeacherDatabase(request,sem_code):
    if verify(request):
        Semester_instance = Semester.objects.filter(access_code = sem_code)
        studentsList = student_Authentication.objects.filter(sem__in = Semester_instance)
        data = {
            'sudentList' : studentsList
        }
        return render(request,'addStudentToSub.html',data)
    else:
        return redirect(reverse('Authentication:Login'))