from django.contrib import admin
from Authentication.models import *

# Register your models here.

admin.site.register(admin_Authentication)
admin.site.register(teacher_Authentication)
admin.site.register(student_Authentication)