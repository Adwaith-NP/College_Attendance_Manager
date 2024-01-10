from django.db import models
from Authentication.models import admin_Authentication
from co_admin.models import Semester

# Create your models here.

class student_Authentication(models.Model):
    co_admin = models.ForeignKey(admin_Authentication,on_delete = models.CASCADE,to_field='user_ID',default = 1)
    sem = models.ForeignKey(Semester,on_delete = models.CASCADE,to_field='access_code',default = '2A')
    Name = models.CharField(max_length = 30)
    Parant_phone = models.CharField(max_length = 25,null = True)
    Student_phone = models.CharField(max_length = 25,null = True)
    email = models.EmailField(null = True)
    user_ID = models.CharField(max_length = 30,unique = True)
    password = models.CharField(max_length = 1000)
    
    def __str__(self):
        return self.Name