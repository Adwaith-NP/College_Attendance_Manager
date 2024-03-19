from django.shortcuts import render,redirect
from django.urls import reverse
from Authentication.models import teacher_Authentication,admin_Authentication
from . models import subject,Semester,attendanceDate
from django.contrib import messages
from Authentication.views import encryption
from django.http import HttpResponseRedirect
from student.models import student_Authentication
import verify_user
import json
from django.http import JsonResponse



# Create your views here.

# collect all subject and save in database
def subject_collection(request):
    subject_name = request.POST.get('subject',None)
    co_admin = request.POST.get('userID',None)
    section = request.POST.get('cource',None)
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
    
    if None in [Name, UserID, Email, password] or '' in [Name, UserID, Email, password] :
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
    hour_count = 0
    teacherID = request.POST.get('TeacherID',None)
    attendance_date_ = request.POST.get('date',None)
    Subject_ID = request.POST.get('Subject_ID',None)
    if None in [teacherID, attendance_date_, Subject_ID] or '' in [teacherID, attendance_date_, Subject_ID]:
        # Handle the case where required fields are missing
        messages.warning(request,'Fill all the column')
    else:
        teacher_instance = teacher_Authentication.objects.get(user_ID = teacherID)
        subject_instance = subject.objects.get(id = Subject_ID)
        
        while True:
            hour_count += 1
            if attendanceDate.objects.filter(co_admin = co_admin,teacherID = teacher_instance,
                                attendance_date = attendance_date_,
                                subject_code = subject_instance,
                                hour=hour_count).exists():
                continue
            else:
                break
                
        date_data = attendanceDate(co_admin = co_admin,teacherID = teacher_instance,
                                   attendance_date = attendance_date_,
                                   subject_code = subject_instance,
                                   hour=hour_count)
        date_data.save()
        messages.warning(request,'Saved')

   
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
            Student_number = request.POST.get('Snumber',None)
            email = request.POST.get('email',None)
            password = request.POST.get('password',None)
            print(Student_number)
            if None in [userID, name, password] or '' in [userID, name, password] :
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
            'student_info' : addedStudents,
            'batch' : Semester_instance,
        }

        return render(request,'addStudent.html',data)
    else:
        return redirect(reverse('Authentication:Login'))
    
## new set up
    
def home(request):
    if verify_user.verify(request):
        return render(request,'co_admin_home.html')
    
    else:
        messages.warning(request,'Invalid username or password')
        return redirect(reverse('Authentication:Login'))
    
def faculty_registration(request):
    if verify_user.verify(request):
        user_id = request.COOKIES.get('user_id')
        co_admin = admin_Authentication.objects.get(user_ID = user_id)
        if request.method == 'POST':
            teacher_data_collection(request,co_admin)
        teachers = teacher_Authentication.objects.filter(co_admin = co_admin)
        data = {
            'teacher' : teachers,
        }
        return render(request,'faculty_registration.html',data)
    else:
        messages.warning(request,'Invalid username or password')
        return redirect(reverse('Authentication:Login'))
    
def alote_subject_to_teacher(request,teacher_id):
    if verify_user.verify(request):
        user_id = request.COOKIES.get('user_id')
        co_admin = admin_Authentication.objects.get(user_ID = user_id)
        teacher_instance = teacher_Authentication.objects.get(id = teacher_id)
        sections = Semester.objects.filter(co_admin = co_admin)
        subjects = subject.objects.filter(teacher = teacher_instance)
        
        if request.method == 'POST':
            subject_collection(request)
        
        data = {
            'teacher' : teacher_instance,
            'sections' : sections,
            'subjects' : subjects,
            }
        
        return render(request,'alote_subject_to_teacher.html',data)
    else:
        messages.warning(request,'Invalid username or password')
        return redirect(reverse('Authentication:Login'))
        
        
def sem_and_sec(request):
    if verify_user.verify(request):
        user_id = request.COOKIES.get('user_id')
        co_admin_instance = admin_Authentication.objects.get(user_ID = user_id)
        if request.method == 'POST':
            sections_save(request,co_admin_instance)
        #collect all saved subject
        batch = Semester.objects.filter(co_admin = co_admin_instance)
        
        data = {
            'batch' : batch,
        }
        
        return render(request,'sem_and_sec.html',data)
    else:
        messages.warning(request,'Invalid username or password')
        return redirect(reverse('Authentication:Login'))
    
def aditional_attendance(request):
    if verify_user.verify(request):
        user_id = request.COOKIES.get('user_id')
        co_admin_instance = admin_Authentication.objects.get(user_ID = user_id)
        teachers = teacher_Authentication.objects.filter(co_admin=co_admin_instance)
        saved_aditional_dats = attendanceDate.objects.filter(co_admin = co_admin_instance)
        
        if request.method == 'POST':
            add_additional_attendance(request,co_admin_instance)
        
        data = {
            'teachers':teachers,
            'subjects':saved_aditional_dats,
        }
        return render(request,'aditional_attendance.html',data)
    else:
        messages.warning(request,'Invalid username or password')
        return redirect(reverse('Authentication:Login'))
    
def return_all_subject(request,teacherID):
    if verify_user.verify(request):
        if request.method == 'GET':
            teacher_instance = teacher_Authentication.objects.get(user_ID=teacherID)
            subjects = subject.objects.filter(teacher = teacher_instance)
            subjects_list = [(subj.id,subj.subject) for subj in subjects]
            return JsonResponse({'subjects': subjects_list}, safe=False)
        else:
            # Handle other HTTP methods if needed
            return JsonResponse({'error': 'Same error'}, status=405)
