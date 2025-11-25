from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from .models import *
from .forms import NoticeForm, ClassRoutineForm


def home(request):
    notices = Notice.objects.all()[:5]
    return render(request, 'school/home.html', {'notices': notices})


@login_required
def student_management(request):
    # Check if user is admin or teacher
    if request.user.user_type not in ['admin', 'teacher']:
        return HttpResponseForbidden("You don't have permission to access this page.")

    students = Student.objects.all()
    return render(request, 'school/student_management.html', {'students': students})


@login_required
def teacher_management(request):
    # Check if user is admin
    if request.user.user_type != 'admin':
        return HttpResponseForbidden("You don't have permission to access this page.")

    teachers = Teacher.objects.all()
    return render(request, 'school/teacher_management.html', {'teachers': teachers})


@login_required
def class_routine(request):
    routines = ClassRoutine.objects.all()

    # If student, show only their class routine
    if request.user.user_type == 'student':
        try:
            student = Student.objects.get(user=request.user)
            # Filter by class name string directly
            routines = routines.filter(class_name__name=student.class_name)
        except Student.DoesNotExist:
            routines = ClassRoutine.objects.none()

    return render(request, 'school/class_routine.html', {'routines': routines})


@login_required
def notice_board(request):
    notices = Notice.objects.all().order_by('-created_at')

    # If student, show only notices for students or all
    if request.user.user_type == 'student':
        notices = notices.filter(target_audience__in=['Students', 'All'])

    return render(request, 'school/notice_board.html', {'notices': notices})


@login_required
def results(request):
    results = Result.objects.none()

    if request.user.user_type == 'student':
        try:
            student = Student.objects.get(user=request.user)
            results = Result.objects.filter(student=student)
        except Student.DoesNotExist:
            pass
    elif request.user.user_type == 'teacher':
        # Teachers can see results of their subjects
        try:
            teacher = Teacher.objects.get(user=request.user)
            subjects = Subject.objects.filter(teacher=teacher)
            results = Result.objects.filter(subject__in=subjects)
        except Teacher.DoesNotExist:
            pass
    else:  # admin
        results = Result.objects.all()

    return render(request, 'school/results.html', {'results': results})


@login_required
def attendance_tracking(request):
    attendance = Attendance.objects.none()

    if request.user.user_type == 'student':
        try:
            student = Student.objects.get(user=request.user)
            attendance = Attendance.objects.filter(student=student).order_by('-date')
        except Student.DoesNotExist:
            pass
    elif request.user.user_type == 'teacher':
        # Teachers can see attendance of their classes
        try:
            teacher = Teacher.objects.get(user=request.user)
            classes = Class.objects.filter(class_teacher=teacher)
            attendance = Attendance.objects.filter(class_name__in=classes)
        except Teacher.DoesNotExist:
            pass
    else:  # admin
        attendance = Attendance.objects.all()

    return render(request, 'school/attendance.html', {'attendance': attendance})


@login_required
def library_management(request):
    books = Book.objects.all()
    return render(request, 'school/library.html', {'books': books})


@login_required
def fee_payment(request):
    fees = Fee.objects.none()

    if request.user.user_type == 'student':
        try:
            student = Student.objects.get(user=request.user)
            fees = Fee.objects.filter(student=student).order_by('-due_date')
        except Student.DoesNotExist:
            pass
    elif request.user.user_type == 'teacher':
        return HttpResponseForbidden("You don't have permission to access this page.")
    else:  # admin
        fees = Fee.objects.all()

    return render(request, 'school/fee_payment.html', {'fees': fees})


@login_required
def online_admission(request):
    # Only students or public can access
    if request.user.user_type not in ['student', 'admin']:
        return HttpResponseForbidden("You don't have permission to access this page.")
    return render(request, 'school/online_admission.html')


@login_required
def add_notice(request):
    # Only admin and teachers can add notices
    if request.user.user_type not in ['admin', 'teacher']:
        return HttpResponseForbidden("You don't have permission to access this page.")

    if request.method == 'POST':
        form = NoticeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Notice published successfully!')
            return redirect('notice_board')
    else:
        form = NoticeForm()

    return render(request, 'school/add_notice.html', {'form': form})


# Student specific views
@login_required
def student_dashboard(request):
    if request.user.user_type != 'student':
        return HttpResponseForbidden("You don't have permission to access this page.")

    try:
        student = Student.objects.get(user=request.user)
        # Get student specific data
        attendance_count = Attendance.objects.filter(student=student, status='Present').count()
        total_days = Attendance.objects.filter(student=student).count()
        attendance_percentage = (attendance_count / total_days * 100) if total_days > 0 else 0

        # Get recent notices for students
        recent_notices = Notice.objects.filter(target_audience__in=['Students', 'All']).order_by('-created_at')[:3]

        context = {
            'student': student,
            'attendance_percentage': round(attendance_percentage, 2),
            'total_books': BookIssue.objects.filter(student=student, returned=False).count(),
            'recent_notices': recent_notices,
        }
        return render(request, 'school/student_dashboard.html', context)
    except Student.DoesNotExist:
        messages.error(request, 'Student profile not found!')
        return redirect('dashboard')


@login_required
def student_profile(request):
    if request.user.user_type != 'student':
        return HttpResponseForbidden("You don't have permission to access this page.")

    try:
        student = Student.objects.get(user=request.user)
        return render(request, 'school/student_profile.html', {'student': student})
    except Student.DoesNotExist:
        messages.error(request, 'Student profile not found!')
        return redirect('dashboard')


# Class Routine Management Views
@login_required
def add_class_routine(request):
    # Only teachers and admin can add routines
    if request.user.user_type not in ['admin', 'teacher']:
        return HttpResponseForbidden("You don't have permission to access this page.")

    print(f"User: {request.user}, Method: {request.method}")  # Debug

    if request.method == 'POST':
        print("POST request received")  # Debug
        form = ClassRoutineForm(request.POST)
        form.user = request.user  # Pass user to form

        print(f"Form is valid: {form.is_valid()}")  # Debug

        if form.is_valid():
            try:
                routine = form.save()
                print(f"Routine saved: {routine}")  # Debug
                messages.success(request, f'Class routine added successfully for {routine.class_name.name}!')
                return redirect('class_routine')
            except Exception as e:
                print(f"Error saving routine: {e}")  # Debug
                messages.error(request, f'Error saving routine: {str(e)}')
        else:
            # Print form errors for debugging
            print("Form errors:", form.errors)  # Debug
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ClassRoutineForm()
        form.user = request.user  # Pass user to form
        print("GET request - initializing form")  # Debug

        # If user is teacher, pre-filter subjects to only their subjects
        if request.user.user_type == 'teacher':
            try:
                teacher = Teacher.objects.get(user=request.user)
                teacher_subjects = Subject.objects.filter(teacher=teacher)
                print(f"Teacher {teacher} has {teacher_subjects.count()} subjects")  # Debug
                form.fields['subject'].queryset = teacher_subjects

                if not teacher_subjects.exists():
                    messages.warning(request, 'No subjects assigned to you. Please contact administrator.')
            except Teacher.DoesNotExist:
                messages.error(request, 'Teacher profile not found.')
                form.fields['subject'].queryset = Subject.objects.none()

    return render(request, 'school/add_class_routine.html', {'form': form})


@login_required
def manage_class_routines(request):
    # Only teachers and admin can manage routines
    if request.user.user_type not in ['admin', 'teacher']:
        return HttpResponseForbidden("You don't have permission to access this page.")

    routines = ClassRoutine.objects.all()

    # If teacher, show only routines for their subjects
    if request.user.user_type == 'teacher':
        try:
            teacher = Teacher.objects.get(user=request.user)
            subjects = Subject.objects.filter(teacher=teacher)
            routines = routines.filter(subject__in=subjects)
        except Teacher.DoesNotExist:
            routines = ClassRoutine.objects.none()

    return render(request, 'school/manage_class_routines.html', {'routines': routines})


@login_required
def edit_class_routine(request, routine_id):
    # Only teachers and admin can edit routines
    if request.user.user_type not in ['admin', 'teacher']:
        return HttpResponseForbidden("You don't have permission to access this page.")

    routine = get_object_or_404(ClassRoutine, id=routine_id)

    # If teacher, check if they teach this subject
    if request.user.user_type == 'teacher':
        try:
            teacher = Teacher.objects.get(user=request.user)
            if routine.subject.teacher != teacher:
                return HttpResponseForbidden("You don't have permission to edit this routine.")
        except Teacher.DoesNotExist:
            return HttpResponseForbidden("Teacher profile not found.")

    if request.method == 'POST':
        form = ClassRoutineForm(request.POST, instance=routine)
        form.user = request.user  # Pass user to form

        if form.is_valid():
            form.save()
            messages.success(request, 'Class routine updated successfully!')
            return redirect('manage_class_routines')
    else:
        form = ClassRoutineForm(instance=routine)
        form.user = request.user  # Pass user to form

        # If user is teacher, pre-filter subjects to only their subjects
        if request.user.user_type == 'teacher':
            try:
                teacher = Teacher.objects.get(user=request.user)
                form.fields['subject'].queryset = Subject.objects.filter(teacher=teacher)
            except Teacher.DoesNotExist:
                pass

    return render(request, 'school/edit_class_routine.html', {'form': form, 'routine': routine})


@login_required
def delete_class_routine(request, routine_id):
    # Only teachers and admin can delete routines
    if request.user.user_type not in ['admin', 'teacher']:
        return HttpResponseForbidden("You don't have permission to access this page.")

    routine = get_object_or_404(ClassRoutine, id=routine_id)

    # If teacher, check if they teach this subject
    if request.user.user_type == 'teacher':
        try:
            teacher = Teacher.objects.get(user=request.user)
            if routine.subject.teacher != teacher:
                return HttpResponseForbidden("You don't have permission to delete this routine.")
        except Teacher.DoesNotExist:
            return HttpResponseForbidden("Teacher profile not found.")

    if request.method == 'POST':
        routine.delete()
        messages.success(request, 'Class routine deleted successfully!')
        return redirect('manage_class_routines')

    return render(request, 'school/delete_class_routine.html', {'routine': routine})