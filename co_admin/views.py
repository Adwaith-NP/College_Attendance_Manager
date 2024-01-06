from django.shortcuts import render,redirect
from django.urls import reverse
from Authentication.models import teacher_Authentication,admin_Authentication
from . models import subject
from django.contrib import messages
from Authentication.views import encryption,get_client_ip
from django.http import HttpResponseRedirect
from django.http import QueryDict

# Create your views here.

# collect all subject and save in database
def subject_collection(request):
    subject_name = request.POST.get('subject',None)
    co_admin = request.POST.get('userID',None)
    if subject_name and co_admin:
        teacher_instance = teacher_Authentication.objects.get(user_ID = co_admin)
        subject_save = subject(teacher = teacher_instance,subject = subject_name)
        subject_save.save()
    return HttpResponseRedirect(reverse('co_admin_app:home'))

# collect all data ebout teacher and save in database
def teacher_data_collection(request,co_admin):
    Name = request.POST.get('Name',None)
    UserID = request.POST.get('UserID',None)
    Email = request.POST.get('Email',None)
    password = request.POST.get('password',None)
    
    if None in [Name, UserID, Email, password] or '' in [Name, UserID, Email, password]:
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
                else:
                    teacher_data_collection(request,co_admin)
            
                    
            #collecting all stored teacher by the co_admin
            teachers = teacher_Authentication.objects.filter(co_admin = co_admin)
            subjects = subject.objects.filter(teacher__in = teachers)
            
            data = {'subject':subjects,'teachers':teachers}
            
            
            return render(request,'co_admin_view.html',data)
    else:
        return redirect('Authentication:Login')
