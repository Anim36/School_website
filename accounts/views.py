from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegistrationForm, ProfileUpdateForm
from school.models import Student, Teacher
import random
import string


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user_type = form.cleaned_data.get('user_type')

            if user_type == 'student':
                # Generate student ID
                student_id = 'STU' + ''.join(random.choices(string.digits, k=6))

                # Get student specific data from form
                date_of_birth = form.cleaned_data.get('date_of_birth')
                gender = form.cleaned_data.get('gender')
                class_name = form.cleaned_data.get('class_name') or 'Class 1'
                section = form.cleaned_data.get('section') or 'A'
                roll_number = form.cleaned_data.get('roll_number') or 1
                parent_name = form.cleaned_data.get('parent_name') or ''
                parent_phone = form.cleaned_data.get('parent_phone') or ''

                Student.objects.create(
                    user=user,
                    student_id=student_id,
                    date_of_birth=date_of_birth,
                    gender=gender,
                    class_name=class_name,
                    section=section,
                    roll_number=roll_number,
                    parent_name=parent_name,
                    parent_phone=parent_phone
                )

            elif user_type == 'teacher':
                # Generate teacher ID
                teacher_id = 'TCH' + ''.join(random.choices(string.digits, k=6))
                Teacher.objects.create(user=user, teacher_id=teacher_id)

            login(request, user)
            return redirect('dashboard')
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})


@login_required
def dashboard(request):
    user_type = request.user.user_type
    context = {'user_type': user_type}

    if user_type == 'student':
        try:
            context['student'] = Student.objects.get(user=request.user)
        except Student.DoesNotExist:
            context['student'] = None
    elif user_type == 'teacher':
        try:
            context['teacher'] = Teacher.objects.get(user=request.user)
        except Teacher.DoesNotExist:
            context['teacher'] = None

    return render(request, 'accounts/dashboard.html', context)


@login_required
def profile(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ProfileUpdateForm(instance=request.user)

    context = {
        'form': form
    }

    # Add student/teacher info to context
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