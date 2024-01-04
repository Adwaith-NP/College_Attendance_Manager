from django.db import models

# Create your models here.

class admin_Authentication(models.Model):
    Name = models.CharField(max_length = 31,null=False)
    email = models.EmailField(default = None)
    user_ID = models.CharField(max_length = 31,unique = True,null=False)
    password = models.CharField(max_length = 1001,null=False)
    course = models.CharField(max_length = 50,default = None,null=True) 
    admin = models.BooleanField(default = False)
    
    def __str__(self):
        return self.Name
    
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
    
    