from django.db import models
from Authentication.models import teacher_Authentication,admin_Authentication

# Create your models here.


    
class Semester(models.Model):
    co_admin = models.ForeignKey(admin_Authentication,default = 1,on_delete = models.CASCADE,to_field='user_ID')
    semester = models.CharField(max_length = 20,default = 'None')
    section = models.CharField(max_length = 20,default = 'None')
    access_code = models.CharField(max_length = 20,unique = True)
    
    def __str__(self):
        return str(self.access_code)
    
class subject(models.Model):
    teacher = models.ForeignKey(teacher_Authentication,default = 1,on_delete = models.CASCADE,to_field='user_ID')
    subject = models.CharField(max_length = 30)
    semester_code = models.ForeignKey(Semester,to_field='access_code',on_delete = models.CASCADE,default = '3A')
    
    def __str__(self):
        return self.subject
    
class attendanceDate(models.Model):
    co_admin = models.ForeignKey(admin_Authentication,default = 1,on_delete = models.CASCADE,to_field='user_ID')
    teacherID = models.ForeignKey(teacher_Authentication,default = 1,on_delete = models.CASCADE,to_field='user_ID')
    attendance_date = models.DateField(null = True)
