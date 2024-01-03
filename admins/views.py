from django.shortcuts import render,redirect
from Authentication.models import admin_Authentication
from django.contrib import messages
from django.http import HttpResponseRedirect,HttpResponseBadRequest
import hashlib


# Create your views here.

def admin(request):
    user_id = request.session.get('user_id')
    if admin_Authentication.objects.filter(user_ID = user_id).exists():
        if request.method == 'POST':
            course_name = request.POST('course_name',None)
            HOD_name = request.POST.get('HOD_name',None)
            email = request.POST.get('email',None)
            register_ID = request.POST.get('register_ID',None)
            password = request.POST.get('password',None)
            
            print(course_name,HOD_name,email,register_ID,password)
            if course_name is None or HOD_name is None or email is None or register_ID is None or password is None:
                # Handle the case where required fields are missing
                messages.warning(request,'Fill all the column')
                return HttpResponseRedirect(request.path_info)
            elif admin_Authentication.objects.filter(user_ID = register_ID).exists():
                messages.warning(request,'User name alrady taken')
                return HttpResponseRedirect(request.path_info)
            else:
                hashed_password = hashlib.sha256(password.encode()).hexdigest()
                data = admin_Authentication(Name = HOD_name,email = email,user_ID = register_ID,password = hashed_password,course = course_name)
                data.save()
                messages.success(request,'Saved')
                return HttpResponseRedirect(request.path_info)
            
        return render(request,'admin.html')
    else:
        return redirect('Authentication:Login')
    
def logout(request):
    request.session.pop('user_id', None)
    return redirect('Authentication:Login')
    
    