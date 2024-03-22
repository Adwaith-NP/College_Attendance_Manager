from jwt import decode
import bcrypt
from Authentication.models import admin_Authentication,teacher_Authentication
from student.models import student_Authentication

# global hashpass


def verify(request):
    def is_true(request,psw):
        path_info = request.path
        id = request.COOKIES.get('user_id')
        if path_info.find('superpage') != -1:
            return admin_Authentication.objects.filter(user_ID=id,password = psw).exists()
        elif path_info.find('co_admin') != -1 or path_info.find('total_sub_view') != -1:
            if admin_Authentication.objects.filter(user_ID=id,password = psw).exists():
                return True
            elif path_info.find('total_sub_view') != -1:
                return teacher_Authentication.objects.filter(user_ID=id,password = psw).exists()
        elif path_info.find('teacher') != -1:
            return teacher_Authentication.objects.filter(user_ID=id,password = psw).exists()
        elif path_info.find('student') != -1:
            return student_Authentication.objects.filter(user_ID=id,password = psw).exists()
        else:
            return False
    
    token = request.COOKIES.get('jwt')
    if not token:
        return False
    try:
        payload = decode(token,'secret',algorithms = ['HS256'])
    except :

        return False
    hashed_password = payload.get('password', None)
    return hashed_password and is_true(request,hashed_password)
        