from django.contrib import admin
from co_admin.models import subject,Semester,attendanceDate

# Register your models here.
admin.site.register(subject)
admin.site.register(Semester)
admin.site.register(attendanceDate)
