from django.shortcuts import render,redirect
from Authentication.models import admin_Authentication
from django.contrib import messages
from django.http import HttpResponseRedirect
from Authentication.views import encryption,get_client_ip
import hashlib


# Create your views here.

# admin page logical code
def admin(request):
    user_id = request.session.get('user_id')
    acsses_code = request.session.get('acsses_code')
    client_ip = get_client_ip(request)
    encrypted_ip = encryption(client_ip)
    
    #check the stored ip hash and client ip hash was same
    if acsses_code == encrypted_ip:
        #check that the stored user id is exists
        if admin_Authentication.objects.filter(user_ID = user_id,admin = True).exists():
            if request.method == 'POST':
                course_name = request.POST.get('course_name',None)
                HOD_name = request.POST.get('HOD_name',None)
                email = request.POST.get('email',None)
                register_ID = request.POST.get('register_ID',None)
                password = request.POST.get('password',None)
                
                if course_name is None or HOD_name is None or email is None or register_ID is None or password is None:
                    # Handle the case where required fields are missing
                    messages.warning(request,'Fill all the column')
                    return HttpResponseRedirect(request.path_info)
                elif course_name == '' or HOD_name == '' or email == '' or register_ID == '' or password == '':
                    # Handle the case where required fields are missing
                    messages.warning(request,'Fill all the column')
                    return HttpResponseRedirect(request.path_info)
                elif admin_Authentication.objects.filter(user_ID = register_ID).exists():
                    messages.warning(request,'User name alrady taken')
                    return HttpResponseRedirect(request.path_info)
                else:
                    hashed_password = encryption(password)
                    data = admin_Authentication(Name = HOD_name,email = email,user_ID = register_ID,password = hashed_password,course = course_name)
                    data.save()
                    messages.success(request,'Saved')
                    return HttpResponseRedirect(request.path_info)
            
            saved_co_admin = admin_Authentication.objects.filter(admin = False)
            
                
            return render(request,'admin.html',{'co_admin':saved_co_admin})
        else:
            return redirect('Authentication:Login')
    else:
        return redirect('Authentication:Login')
    
def logout(request):
    request.session.pop('user_id', None)
    return redirect('Authentication:Login')
    
    