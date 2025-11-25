from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import *
from .forms import *

def is_admin(user):
    return user.user_type == 'admin'

def is_teacher(user):
    return user.user_type == 'teacher'

def is_student(user):
    return user.user_type == 'student'

def home(request):
    notices = Notice.objects.all()[:5]
    return render(request, 'school/home.html', {'notices': notices})

@login_required
def student_management(request):
    if not is_admin(request.user):
        return redirect('dashboard')
    students = Student.objects.all()
    return render(request, 'school/student_management.html', {'students': students})

@login_required
def teacher_management(request):
    if not is_admin(request.user):
        return redirect('dashboard')
    teachers = Teacher.objects.all()
    return render(request, 'school/teacher_management.html', {'teachers': teachers})

@login_required
def class_routine(request):
    routines = ClassRoutine.objects.all()
    return render(request, 'school/class_routine.html', {'routines': routines})

@login_required
def notice_board(request):
    notices = Notice.objects.all()
    return render(request, 'school/notice_board.html', {'notices': notices})

@login_required
def results(request):
    if is_student(request.user):
        try:
            student = Student.objects.get(user=request.user)
            results = Result.objects.filter(student=student)
        except Student.DoesNotExist:
            # If student profile doesn't exist, show empty results
            results = Result.objects.none()
    else:
        results = Result.objects.all()
    return render(request, 'school/results.html', {'results': results})

@login_required
def attendance_tracking(request):
    if is_student(request.user):
        try:
            student = Student.objects.get(user=request.user)
            attendance = Attendance.objects.filter(student=student)
        except Student.DoesNotExist:
            # If student profile doesn't exist, show empty attendance
            attendance = Attendance.objects.none()
    else:
        attendance = Attendance.objects.all()
    return render(request, 'school/attendance.html', {'attendance': attendance})

@login_required
def library_management(request):
    books = Book.objects.all()
    return render(request, 'school/library.html', {'books': books})

@login_required
def fee_payment(request):
    if is_student(request.user):
        try:
            student = Student.objects.get(user=request.user)
            fees = Fee.objects.filter(student=student)
        except Student.DoesNotExist:
            # If student profile doesn't exist, show empty fees
            fees = Fee.objects.none()
    else:
        fees = Fee.objects.all()
    return render(request, 'school/fee_payment.html', {'fees': fees})

@login_required
def online_admission(request):
    return render(request, 'school/online_admission.html')

#@login_required
#def parent_portal(request):
    #return render(request, 'school/parent_portal.html')

@login_required
@user_passes_test(is_admin)
def add_notice(request):
    if request.method == 'POST':
        form = NoticeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('notice_board')
    else:
        form = NoticeForm()
    return render(request, 'school/add_notice.html', {'form': form})