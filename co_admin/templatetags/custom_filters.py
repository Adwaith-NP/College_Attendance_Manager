from django import template
from teacher.models import attendance_date

register = template.Library()

@register.filter(name='status')
def status(date):
    return attendance_date.objects.filter(allotted_date = date).exists()