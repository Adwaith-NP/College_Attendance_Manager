from django.shortcuts import render,redirect
from django.urls import reverse
from Authentication.models import teacher_Authentication,admin_Authentication
from . models import subject,Semester,attendanceDate
from django.contrib import messages
from Authentication.views import encryption
from django.http import HttpResponseRedirect
from student.models import student_Authentication
import verify_user



# Create your views here.

# collect all subject and save in database
def subject_collection(request):
    subject_name = request.POST.get('subject',None)
    co_admin = request.POST.get('userID',None)
    section = request.POST.get('sem_selected',None)
    if subject_name and co_admin and section:
        teacher_instance = teacher_Authentication.objects.get(user_ID = co_admin)
        subject_instance = Semester.objects.get(access_code = section)
        subject_save = subject(teacher = teacher_instance,subject = subject_name,semester_code = subject_instance)
        subject_save.save()
    else:
        messages.warning(request,'Fill the column')
    return HttpResponseRedirect(reverse('co_admin_app:home'))

# collect all data ebout teacher and save in database
def teacher_data_collection(request,co_admin):
    Name = request.POST.get('Name',None)
    UserID = request.POST.get('UserID',None)
    Email = request.POST.get('Email',None)
    password = request.POST.get('password',None)
    
    if None or '' in [Name, UserID, Email, password] :
        # Handle the case where required fields are missing
        messages.warning(request,'Fill all the column')
    
    elif teacher_Authentication.objects.filter(user_ID = UserID).exists():
        messages.warning(request,'User name alrady taken')

    else:
        hashed_password = encryption(password)
        data = teacher_Authentication(co_admin = co_admin,Name = Name,email = Email,user_ID = UserID,password = hashed_password)
        data.save()
        messages.warning(request,'Saved')
    return HttpResponseRedirect(request.path_info)
    

#creating sem and section base class
def sections_save(request,co_admin_instance):
    sem = request.POST.get('semaster',None)
    section_name = request.POST.get('section',None)
    access_code_ = request.POST.get('access_code',None)
    
    if None or '' not in [sem,section_name,access_code_]:
        if Semester.objects.filter(access_code = access_code_).exists():
            messages.warning(request,'sem and section alrady exits')
        else:
            save_data = Semester(co_admin = co_admin_instance,semester = sem,section= section_name,access_code = access_code_)
            save_data.save()
            messages.warning(request,'Saved')
    else:
        messages.warning(request,'Fill all column')
    return HttpResponseRedirect(request.path_info)

#To add additonal attendance date
def add_additional_attendance(request,co_admin):
    teacherID = request.POST.get('TeacherID',None)
    attendance_date_ = request.POST.get('date',None)
    Subject_ID = request.POST.get('Subject_ID',None)
    if None or '' in [teacherID,attendance_date_,Subject_ID] :
        # Handle the case where required fields are missing
        messages.warning(request,'Fill all the column')
    else:
        teacher_instance = teacher_Authentication.objects.get(user_ID = teacherID)
        subject_instance = subject.objects.get(id = Subject_ID)
        date_data = attendanceDate(co_admin = co_admin,teacherID = teacher_instance,attendance_date = attendance_date_,subject_code = subject_instance)
        date_data.save()
        messages.warning(request,'Saved')

# home page logical view
def home(request):
    #check the stored ip hash and client ip hash was same
    if verify_user.verify(request):
            user_id = request.COOKIES.get('user_id')
            co_admin = admin_Authentication.objects.get(user_ID = user_id)
            if request.method == 'POST' :
                if "subject" in request.POST:
                    subject_collection(request)
                elif "semaster" in request.POST:
                    sections_save(request,co_admin)
                elif "TeacherID" in request.POST:
                    add_additional_attendance(request,co_admin)
                else:
                    teacher_data_collection(request,co_admin)
            
                    
            #collecting all stored teacher by the co_admin
            teachers = teacher_Authentication.objects.filter(co_admin = co_admin)
            subjects = subject.objects.filter(teacher__in = teachers)
            sections = Semester.objects.filter(co_admin = co_admin)
            additional_attendance = attendanceDate.objects.filter(co_admin = co_admin)
            
            
            
            data = {'subject':subjects,
                    'teachers':teachers,
                    'class_info':sections,
                    'additional_attendance':additional_attendance,
                    }
            
            
            return render(request,'co_admin_view.html',data)
    else:
        messages.warning(request,'Invalid username or password')
        return redirect(reverse('Authentication:Login'))
   
#student registretion 
def addStudent(request,access_code):
    if verify_user.verify(request):
        user_id = request.COOKIES.get('user_id')
        co_admin_instance = admin_Authentication.objects.get(user_ID = user_id,)
        Semester_instance = Semester.objects.get(access_code = access_code)
        if request.method == 'POST':
            userID = request.POST.get('UserID',None)
            name = request.POST.get('Name',None)
            Parent_number = request.POST.get('Pnumber',None)
            Student_number = request.POST.get('Snumbre',None)
            email = request.POST.get('email',None)
            password = request.POST.get('password',None)
            if None or '' in [userID,name,password] :
                messages.warning(request,'Fill all column')
            else:
                if student_Authentication.objects.filter(user_ID = userID).exists():
                    messages.warning(request,'UserID alrady taken')
                else:
                    encrypted_password = encryption(password)
                    save_student_data = student_Authentication(
                        co_admin = co_admin_instance,
                        sem = Semester_instance,
                        user_ID = userID,
                        Name = name,
                        password = encrypted_password,
                        Parant_phone = Parent_number,
                        Student_phone = Student_number,
                        email = email)
                    save_student_data.save()
                    messages.warning(request,'Saved')
                return HttpResponseRedirect(request.path_info)
            
        addedStudents = student_Authentication.objects.filter(co_admin = co_admin_instance,sem = Semester_instance)
        
        data = {
            'student_info' : addedStudents
        }

        return render(request,'addStudent.html',data)
    else:
        return redirect(reverse('Authentication:Login'))
