from django.shortcuts import render,redirect
from Authentication.models import *
from django.contrib import messages
from django.http import HttpResponseRedirect
import hashlib

# Create your views here.

def encryption(password):
    return hashlib.sha256(password.encode()).hexdigest() 

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def auth_by_request(request,user_ID):
    client_ip = get_client_ip(request)
    haship = encryption(client_ip)
    request.session['user_id'] = user_ID
    request.session['acsses_code'] = haship


# collecting all login details and responding 
def login(request):
    if request.method == 'POST':
        User_position = request.POST.get('loginUser',None)
        user_ID = request.POST.get('userID',None)
        password = request.POST.get('password',None)
        hashed_password = encryption(password)
        
        if User_position == 'Admin':
            if admin_Authentication.objects.filter(user_ID = user_ID,password = hashed_password,admin = True).exists():
                auth_by_request(request,user_ID)
                return redirect('admin_app:admin')
            else:
                messages.warning(request,'invalid username or password')
                return HttpResponseRedirect(request.path_info)
            
        if User_position == 'Co-Admin' :
            if admin_Authentication.objects.filter(user_ID = user_ID,password = hashed_password,admin = False).exists():
                auth_by_request(request,user_ID)
                return redirect('co_admin_app:home')
            else:
                messages.warning(request,'invalid username or password')
                return HttpResponseRedirect(request.path_info)
    return render(request,'Login.html')

