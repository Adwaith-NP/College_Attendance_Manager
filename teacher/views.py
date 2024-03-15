from django.shortcuts import render,redirect
from django.urls import reverse
from verify_user import verify
from Authentication.models import teacher_Authentication
from co_admin.models import subject,Semester,attendanceDate
from student.models import student_Authentication
from student.models import student_Authentication
from teacher.models import added_student_To_sub,attendance_date,attendance
from django.utils import timezone
from django.http import Http404

# Create your views here.

# store the current date
current_date = None


def user_deails(request):
    user_id = request.COOKIES.get('user_id')
    try:
        teacher_data = teacher_Authentication.objects.get(user_ID = user_id)
        teacher_instance = teacher_Authentication.objects.filter(user_ID = user_id)
        teacher_subject = subject.objects.filter(teacher__in = teacher_instance)
        return [user_id,teacher_instance,teacher_subject,teacher_data]
    except:
            raise Http404("Page not fount")
def home(request):
    global current_date 
    current_date = timezone.now().date()
    if verify(request):
        teacher_subject = user_deails(request)[2]
        teacher_instance = user_deails(request)[3]
        additional_added_attendance = attendanceDate.objects.filter(teacherID__in = user_deails(request)[1])
        

        
        data = {
            'teacher_instance' : teacher_instance,
            'subjects' : teacher_subject,
            'co_admin_added_date' : additional_added_attendance,
            
        }
        return render(request,'teacher_view.html',data)
    else:
        return redirect(reverse('Authentication:Login'))
    
    
 # function for add student to the subject   
def addStudentToTeacherDatabase(request,sem_code,pk_sub):

    if verify(request):
        try:
            subject_instance = subject.objects.get(id = pk_sub)
            Semester_instance = Semester.objects.filter(access_code = sem_code)
            sub_sem = (subject_instance.semester_code.co_admin.course,subject_instance.semester_code.semester,subject_instance.subject)
            added_student_list_in_database = added_student_To_sub.objects.filter(subject_ForeignKey = subject_instance)
            exlude_student_id = added_student_list_in_database.values_list('student_ForeignKry',flat=True)
            students_List_In_Sem = student_Authentication.objects.filter(sem__in = Semester_instance).exclude(user_ID__in = exlude_student_id)
        except:
            raise Http404("Page not fount")
        
        
        if request.method == 'POST':
            added_student_list = request.POST.getlist('addedStudentList')
            for userID in added_student_list:
                student_instance = student_Authentication.objects.get(user_ID = userID)
                added_student_To_sub_save_data = added_student_To_sub(subject_ForeignKey = subject_instance,student_ForeignKry = student_instance)
                added_student_To_sub_save_data.save()
                
                
                   
        
        data = {
            'sudentList' : students_List_In_Sem,
            'added_students' : added_student_list_in_database,
            'sem_code' : sem_code,
            'pk_sub' : pk_sub,
            'sub_sem' : sub_sem
            
        }
        return render(request,'addStudentToSub.html',data)
    else:
        return redirect(reverse('Authentication:Login'))
    
    
def delete_student_from_teacher_database(request,userID,sem_code,pk_sub):
    if verify(request):
        try:
            student_instance = student_Authentication.objects.get(user_ID = userID)
            subject_instance = subject.objects.get(id = pk_sub)
            added_student_To_sub_save_data = added_student_To_sub.objects.filter(subject_ForeignKey = subject_instance,student_ForeignKry = student_instance)
            added_student_To_sub_save_data.delete()
        except:
            raise Http404("Page not fount")
        return redirect(reverse('teacher_app:addStudent',args=[sem_code, pk_sub]))
    else:
        return redirect(reverse('Authentication:Login'))
    
def add_students_attandace(request,pk_sub,slot,date):
    if verify(request):
        global current_date
        if date != 'date':
            current_date = date
        try:
            subject_instence = subject.objects.get(pk = pk_sub)
            added_student_To_sub_list = added_student_To_sub.objects.filter(subject_ForeignKey = subject_instence)
        except:
            raise Http404("Page not fount")
        
        if request.method == 'POST':
            attendans_list = request.POST.getlist('Attendance_marked')
            
            #Save the attendance date
            if attendance_date.objects.filter(subject_ForeignKey = subject_instence,allotted_date = current_date).exists():
                return redirect(reverse('teacher_app:home'))
            try:
                attendance_date_set = attendance_date(subject_ForeignKey = subject_instence,allotted_date = current_date)
                attendance_date_set.save()
            except:
                return redirect(reverse('teacher_app:home'))
            try:
                attendance_date_set_instance = attendance_date.objects.get(additional_hover = slot,allotted_date=current_date)
            except:
                return redirect(reverse('teacher_app:home'))
            
            
            
            #Add attendance
            for id in added_student_To_sub_list:
                try:
                    student_ForeignKry_instace = student_Authentication.objects.get(user_ID = id.student_ForeignKry.user_ID)
                    if id.student_ForeignKry.user_ID in attendans_list:
                        add_attandace = attendance(attendance_date_ForeignKey = attendance_date_set_instance,
                                                   student_ForeignKry = student_ForeignKry_instace,
                                                   attendance_boolean = True)
                    else:
                        add_attandace = attendance(attendance_date_ForeignKey = attendance_date_set_instance,
                                                   student_ForeignKry = student_ForeignKry_instace)
                    add_attandace.save()
                except:
                    print('Error plese try egain')
                    return redirect(reverse('teacher_app:home'))
            
            print('Attendace added')
            return redirect(reverse('teacher_app:home'))
            
        data = {
            'students_list' : added_student_To_sub_list,
            'currect_date' : current_date
        }
        return render(request,'add_students_attendance.html',data)
    else:
        return redirect(reverse('Authentication:Login'))