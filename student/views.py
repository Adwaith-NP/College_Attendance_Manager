from django.shortcuts import render,redirect
from django.urls import reverse
from verify_user import verify
from . models import student_Authentication
from co_admin.models import subject,Semester
from teacher.models import added_student_To_sub,attendance_date,attendance
# Create your views here.


def home(request):
    if verify(request):
        user_id = request.COOKIES.get('user_id')
        student = student_Authentication.objects.get(user_ID = user_id)
        co_admin_instance = student.co_admin
        semesters = Semester.objects.filter(co_admin = co_admin_instance)
        subjects = subject.objects.filter(semester_code__in=semesters.values_list('access_code', flat=True))
        ##collected all subject
        subject_of_student = added_student_To_sub.objects.filter(subject_ForeignKey__in = subjects,student_ForeignKry = student)
        
        ##tottal percentage
        subject_foreign_keys = subject_of_student.values_list('subject_ForeignKey', flat=True)
        sub_list = list()
        for pk in subject_foreign_keys:
            subject_instance = subject.objects.get(id = pk)
            subject_name = subject_instance.subject
            dates = attendance_date.objects.filter(subject_ForeignKey = pk)
            total_class = attendance.objects.filter(attendance_date_ForeignKey__in = dates,student_ForeignKry = student).count()
            percented_class = attendance.objects.filter(attendance_date_ForeignKey__in = dates,student_ForeignKry = student,attendance_boolean = True).count()
            attendance_percentage = (percented_class/total_class)*100
            sub_list.append((pk,attendance_percentage,total_class,percented_class,subject_name))
        
        total_percentage = 0
        total_sub_pr = len(sub_list)*100
        for sub in sub_list:
            total_percentage+= sub[1]
            
        total_attendance_percentage = (total_percentage/total_sub_pr)*100
        
        #passing data
        data = {
            "percentage":total_attendance_percentage,
            "student_info":student,
            "subjects":sub_list,
            
        }
        
        return render(request,'student_home.html',data)
    else:
        return redirect(reverse('Authentication:Login'))