from django.db import models

# Create your models here.

class admin_Authentication(models.Model):
    Name = models.CharField(max_length = 30)
    email = models.EmailField(default = None)
    user_ID = models.CharField(max_length = 30,unique = True)
    password = models.CharField(max_length = 1000)
    course = models.CharField(max_length = 50)
    admin = models.BooleanField(default = False)
    
class teacher_Authentication(models.Model):
    Name = models.CharField(max_length = 30)
    email = models.EmailField(default = None) 
    user_ID = models.CharField(max_length = 30,unique = True)
    password = models.CharField(max_length = 1000)
    
class student_Authentication(models.Model):
    Name = models.CharField(max_length = 30)
    phone = models.CharField(max_length = 25,default = None)
    email = models.EmailField(default = None)
    user_ID = models.CharField(max_length = 30,unique = True)
    password = models.CharField(max_length = 1000)
    
    