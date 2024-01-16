from django.db import models
from co_admin.models import subject
from student.models import student_Authentication
# Create your models here.

class added_student_To_sub(models.Model):
    subject_ForeignKey = models.ForeignKey(subject,on_delete = models.CASCADE,to_field = 'id')
    student_ForeignKry = models.ForeignKey(student_Authentication,on_delete = models.CASCADE,to_field = 'user_ID')
    
