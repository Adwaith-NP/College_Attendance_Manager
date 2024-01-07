from django.shortcuts import render,redirect
from django.urls import reverse
from Authentication.models import teacher_Authentication,admin_Authentication
from . models import subject,Semester
from django.contrib import messages
from Authentication.views import encryption,get_client_ip
from django.http import HttpResponseRedirect


# Create your views here.

# collect all subject and save in database
def subject_collection(request):
    subject_name = request.POST.get('subject',None)
    co_admin = request.POST.get('userID',None)
    section = request.POST.get('sem_selected',None)
    if subject_name and co_admin:
        teacher_instance = teacher_Authentication.objects.get(user_ID = co_admin)
        subject_instance = Semester.objects.get(access_code = section)
        subject_save = subject(teacher = teacher_instance,subject = subject_name,semester_code = subject_instance)
        subject_save.save()
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
    
    if None or '' not in [sem,section_name]:
        access_code_ = (sem+section_name).upper()
        if Semester.objects.filter(access_code = access_code_).exists():
            messages.warning(request,'sem and section alrady exits')
        else:
            save_data = Semester(co_admin = co_admin_instance,semester = sem,section= section_name,access_code = access_code_)
            save_data.save()
            messages.warning(request,'Saved')
    return HttpResponseRedirect(request.path_info)

# home page logical view
def home(request):
    user_id = request.session.get('user_id')
    acsses_code = request.session.get('acsses_code')
    client_ip = get_client_ip(request)
    encrypted_ip = encryption(client_ip)
    
    #check the stored ip hash and client ip hash was same
    if acsses_code == encrypted_ip and admin_Authentication.objects.filter(user_ID = user_id,admin = False).exists():
            co_admin = admin_Authentication.objects.get(user_ID = user_id)
            if request.method == 'POST' :
                if "subject" in request.POST:
                    subject_collection(request)
                elif "semaster" in request.POST:
                    sections_save(request,co_admin)
                else:
                    teacher_data_collection(request,co_admin)
            
                    
            #collecting all stored teacher by the co_admin
            teachers = teacher_Authentication.objects.filter(co_admin = co_admin)
            subjects = subject.objects.filter(teacher__in = teachers)
            sections = Semester.objects.filter(co_admin = co_admin)
            
            
            data = {'subject':subjects,'teachers':teachers,'class_info':sections}
            
            
            return render(request,'co_admin_view.html',data)
    else:
        return redirect('Authentication:Login')
    
def addStudent(request):
    pass
