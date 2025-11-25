from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegistrationForm, ProfileUpdateForm
from school.models import Student, Teacher, Attendance, BookIssue  # Import necessary models
import random
import string


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user_type = form.cleaned_data.get('user_type')

            if user_type == 'student':
                student_id = 'STU' + ''.join(random.choices(string.digits, k=6))
                Student.objects.create(user=user, student_id=student_id)
            elif user_type == 'teacher':
                teacher_id = 'TCH' + ''.join(random.choices(string.digits, k=6))
                Teacher.objects.create(user=user, teacher_id=teacher_id)

            login(request, user)
            return redirect('dashboard')
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=request.user)

    context = {'form': form}

    if request.user.user_type == 'student':
        try:
            context['student'] = Student.objects.get(user=request.user)
        except Student.DoesNotExist:
            context['student'] = None
    elif request.user.user_type == 'teacher':
        try:
            context['teacher'] = Teacher.objects.get(user=request.user)
        except Teacher.DoesNotExist:
            context['teacher'] = None

    return render(request, 'accounts/profile.html', context)


@login_required
def dashboard(request):
    user_type = request.user.user_type

    if user_type == 'student':
        # Student এর জন্য student dashboard show করবে
        try:
            student = Student.objects.get(user=request.user)

            # Get basic student data (with error handling)
            try:
                attendance_count = Attendance.objects.filter(student=student, status='Present').count()
                total_days = Attendance.objects.filter(student=student).count()
                attendance_percentage = (attendance_count / total_days * 100) if total_days > 0 else 0
            except:
                attendance_count = 0
                total_days = 0
                attendance_percentage = 0

            try:
                total_books = BookIssue.objects.filter(student=student, returned=False).count()
            except:
                total_books = 0

            context = {
                'student': student,
                'attendance_percentage': round(attendance_percentage, 2),
                'attendance_count': attendance_count,
                'total_days': total_days,
                'total_books': total_books,
            }
            return render(request, 'school/student_dashboard.html', context)
        except Student.DoesNotExist:
            messages.error(request, 'Student profile not found!')
            # Fallback to basic dashboard
            return render(request, 'accounts/dashboard.html', {'user_type': user_type})

    else:
        # Admin and teachers এর জন্য regular dashboard
        context = {'user_type': user_type}

        if user_type == 'teacher':
            try:
                context['teacher'] = Teacher.objects.get(user=request.user)
            except Teacher.DoesNotExist:
                context['teacher'] = None

        return render(request, 'accounts/dashboard.html', context)