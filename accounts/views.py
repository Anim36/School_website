from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegistrationForm, ProfileUpdateForm
from school.models import Student, Teacher, Attendance, BookIssue
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

                # Student information from form
                gender = request.POST.get('gender', '')
                date_of_birth = request.POST.get('date_of_birth') or None
                class_name = request.POST.get('class_name', 'Class 1')
                section = request.POST.get('section', 'A')
                roll_number = request.POST.get('roll_number', 1)
                father_name = request.POST.get('father_name', '')
                mother_name = request.POST.get('mother_name', '')
                parent_phone = request.POST.get('parent_phone', '')
                parent_email = request.POST.get('parent_email', '')
                parent_address = request.POST.get('parent_address', '')

                Student.objects.create(
                    user=user,
                    student_id=student_id,
                    gender=gender,
                    date_of_birth=date_of_birth,
                    class_name=class_name,
                    section=section,
                    roll_number=roll_number,
                    father_name=father_name,
                    mother_name=mother_name,
                    parent_phone=parent_phone,
                    parent_email=parent_email,
                    parent_address=parent_address
                )
                messages.success(request, f'Student account created successfully! Your Student ID is: {student_id}')

            elif user_type == 'teacher':
                teacher_id = 'TCH' + ''.join(random.choices(string.digits, k=6))

                # Teacher information from form
                gender = request.POST.get('teacher_gender', '')
                date_of_birth = request.POST.get('teacher_dob') or None
                qualification = request.POST.get('qualification', '')
                specialization = request.POST.get('specialization', '')

                Teacher.objects.create(
                    user=user,
                    teacher_id=teacher_id,
                    gender=gender,
                    date_of_birth=date_of_birth,
                    qualification=qualification,
                    specialization=specialization
                )
                messages.success(request, f'Teacher account created successfully! Your Teacher ID is: {teacher_id}')

            login(request, user)
            return redirect('dashboard')
        else:
            # Form errors debug korar jonno
            messages.error(request, 'Please correct the errors below.')
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
        try:
            student = Student.objects.get(user=request.user)

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
            return render(request, 'accounts/dashboard.html', {'user_type': user_type})

    else:
        context = {'user_type': user_type}

        if user_type == 'teacher':
            try:
                context['teacher'] = Teacher.objects.get(user=request.user)
            except Teacher.DoesNotExist:
                context['teacher'] = None

        return render(request, 'accounts/dashboard.html', context)