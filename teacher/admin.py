from django.contrib import admin
from .models import added_student_To_sub,attendance,attendance_date

# Register your models here.

admin.site.register(added_student_To_sub)
admin.site.register(attendance)
admin.site.register(attendance_date)