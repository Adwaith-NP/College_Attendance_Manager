from django.shortcuts import render,redirect
from Authentication.models import *
from django.contrib import messages
from django.http import HttpResponseRedirect
import hashlib

# Create your views here.

def encryption(password):
    return hashlib.sha256(password.encode()).hexdigest() 


# collecting all login details and responding 
def login(request):
    if request.method == 'POST':
        User_position = request.POST.get('loginUser',None)
        user_ID = request.POST.get('userID',None)
        password = request.POST.get('password',None)
        hashed_password = encryption(password)
        
        if User_position == 'Admin':
            if admin_Authentication.objects.filter(user_ID = user_ID,password = hashed_password,admin = True).exists():
                request.session['user_id'] = user_ID
                return redirect('admin_app:admin')
            else:
                messages.warning(request,'invalid username or password')
                return HttpResponseRedirect(request.path_info) 
        
    return render(request,'Login.html')

