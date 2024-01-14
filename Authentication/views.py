from django.shortcuts import render,redirect
from Authentication.models import *
from django.contrib import messages
from django.http import HttpResponseRedirect,HttpResponse
import hashlib
import datetime
from jwt import encode

# Create your views here.

def encryption(password):
    return hashlib.sha256(password.encode()).hexdigest() 

#Creating the JWT token for authentication
def auth_by_request(request,user_ID,redirect_url):
    
    
    payload = {
        'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
        'iat' : datetime.datetime.utcnow(),
    }
    
    token = encode(payload,'secret',algorithm = 'HS256')
    response = redirect(redirect_url)
    response.set_cookie(key='jwt',value=token,httponly=True)
    response.set_cookie(key='user_id',value=user_ID,httponly=True)
    print(response)
    return response


# collecting all login details and responding 
def login(request):
    if request.method == 'POST':
        User_position = request.POST.get('loginUser',None)
        user_ID = request.POST.get('userID',None)
        password = request.POST.get('password',None)
        hashed_password = encryption(password)
        
        if User_position == 'Admin':
            if admin_Authentication.objects.filter(user_ID = user_ID,password = hashed_password,admin = True).exists():
                redirect_url = 'admin_app:admin'
                return auth_by_request(request,user_ID,redirect_url)
            else:
                messages.warning(request,'invalid username or password')
                return HttpResponseRedirect(request.path_info)
            
        elif User_position == 'Co-Admin' :
            if admin_Authentication.objects.filter(user_ID = user_ID,password = hashed_password,admin = False).exists():
                redirect_url = 'co_admin_app:home'
                return auth_by_request(request,user_ID,redirect_url)
            else:
                messages.warning(request,'invalid username or password')
                return HttpResponseRedirect(request.path_info)
        
        elif User_position == 'Teacher' :
            if teacher_Authentication.objects.filter(user_ID = user_ID,password = hashed_password).exists():
                redirect_url = 'teacher_app:home'
                return auth_by_request(request,user_ID,redirect_url)
            else:
                messages.warning(request,'invalid username or password')
                return HttpResponseRedirect(request.path_info)
        else:
            messages.warning(request,'Selecte a option')
            return HttpResponseRedirect(request.path_info)
    return render(request,'Login.html')

def logout(request):
    
    response = redirect('Authentication:Login')
    response.delete_cookie('jwt')
    response.delete_cookie('user_id')
    return response
