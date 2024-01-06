from django.db import models
from Authentication.models import teacher_Authentication

# Create your models here.

class subject(models.Model):
    teacher = models.ForeignKey(teacher_Authentication,default = 1,on_delete = models.CASCADE,to_field='user_ID')
    subject = models.CharField(max_length = 30)
    
    def __str__(self):
        return self.subject
