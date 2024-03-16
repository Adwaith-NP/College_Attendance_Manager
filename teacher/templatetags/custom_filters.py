from django import template
from datetime import date
from teacher.models import attendance_date,attendance
from django.utils import timezone
from co_admin.models import subject
from datetime import time

register = template.Library()

@register.filter(name='isoformat_date')
def isoformat_date(value):
    if isinstance(value, date):
        return value.isoformat()
    return value

@register.filter(name='added_or_not')
def added_or_not(sub_pk,date = None):
    current_date = timezone.now().date()
    current_time = timezone.now().time()
    starting_time = time(0,0)
    ending_time = time(23,59)
    if date:
        current_date = date
    subject_instance = subject.objects.get(id = sub_pk)
    closest_record = attendance_date.objects.filter(
        allotted_date__lte=current_date,
        subject_ForeignKey = subject_instance,
        additional_hover = 0
        ).order_by('-allotted_date').first()
    if not (current_time>starting_time and current_time <ending_time):
        return 'Time'
    if closest_record and current_date == closest_record.allotted_date :
        return False
    return True

@register.filter(name='attented_classes')
def attented_classes(sub,student):
    count = attendance.objects.filter(attendance_date_ForeignKey__subject_ForeignKey = sub,
                                      student_ForeignKry = student,
                                      attendance_boolean = True).count()
    return count


@register.filter(name='attented_or_not')
def attented_or_not(date,student):
    return_value =  attendance.objects.filter(attendance_date_ForeignKey = date,student_ForeignKry = student,attendance_boolean = True).exists()
    if return_value:
        return True
    return False