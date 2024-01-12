from django.shortcuts import render,redirect
from Authentication.models import admin_Authentication
from django.contrib import messages
from django.http import HttpResponseRedirect
from Authentication.views import encryption
import verify_user


# Create your views here.

# admin page logical code
def admin(request):
    user_id = request.session.get('user_id')
    # acsses_code = request.session.get('acsses_code')
    # client_ip = get_client_ip(request)
    # encrypted_ip = encryption(client_ip)
    
    #check the stored ip hash and client ip hash was same
    if verify_user.verify(request):
        #check that the stored user id is exists
            if request.method == 'POST':
                course_name = request.POST.get('course_name',None)
                HOD_name = request.POST.get('HOD_name',None)
                email = request.POST.get('email',None)
                register_ID = request.POST.get('register_ID',None)
                password = request.POST.get('password',None)
                
                if None in [course_name, HOD_name, email, password,register_ID] or '' in [course_name, HOD_name, email, password,register_ID]:
                    # Handle the case where required fields are missing
                    messages.warning(request,'Fill all the column')
                elif admin_Authentication.objects.filter(user_ID = register_ID).exists():
                    messages.warning(request,'User name alrady taken')
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
    

    
    