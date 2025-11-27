from django.utils import timezone
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
        print("Form is valid:", form.is_valid())
        print("Form errors:", form.errors)

        if form.is_valid():
            user = form.save()
            user_type = form.cleaned_data.get('user_type')

            # Common address fields for all users
            division = form.cleaned_data.get('division', '')
            district = form.cleaned_data.get('district', '')
            thana = form.cleaned_data.get('thana', '')
            postal_code = form.cleaned_data.get('postal_code', '')
            area_village = form.cleaned_data.get('area_village', '')
            house_details = form.cleaned_data.get('house_details', '')

            print(f"User Type: {user_type}")
            print(f"Division: {division}, District: {district}")

            if user_type == 'student':
                student_id = 'STU' + ''.join(random.choices(string.digits, k=6))

                # Student information from form
                gender = form.cleaned_data.get('gender', '')
                date_of_birth = form.cleaned_data.get('date_of_birth')
                class_name = form.cleaned_data.get('class_name', 'Class 1')
                section = form.cleaned_data.get('section', 'A')
                roll_number = form.cleaned_data.get('roll_number', 1)
                father_name = form.cleaned_data.get('father_name', '')
                mother_name = form.cleaned_data.get('mother_name', '')
                parent_phone = form.cleaned_data.get('parent_phone', '')
                parent_email = form.cleaned_data.get('parent_email', '')
                parent_address = form.cleaned_data.get('parent_address', '')

                print(f"Creating student: {gender}, {class_name}, {section}")

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
                    parent_address=parent_address,
                    # নতুন address fields
                    division=division,
                    district=district,
                    thana=thana,
                    postal_code=postal_code,
                    area_village=area_village,
                    house_details=house_details
                )
                messages.success(request, f'Student account created successfully! Your Student ID is: {student_id}')

            elif user_type == 'teacher':
                teacher_id = 'TCH' + ''.join(random.choices(string.digits, k=6))

                # Teacher information from form - FIXED: Use the selected joining_date
                gender = form.cleaned_data.get('teacher_gender', '')
                date_of_birth = form.cleaned_data.get('teacher_dob')
                qualification = form.cleaned_data.get('qualification', '')
                specialization = form.cleaned_data.get('specialization', '')
                joining_date = form.cleaned_data.get('joining_date')

                print(f"Creating teacher with:")
                print(f"Gender: {gender}")
                print(f"DOB: {date_of_birth}")
                print(f"Qualification: {qualification}")
                print(f"Specialization: {specialization}")
                print(f"Joining Date: {joining_date}")

                # FIXED: Use the selected joining_date, don't override with current date
                # Only use current date if joining_date is not provided
                if not joining_date:
                    joining_date = timezone.now().date()
                    print(f"No joining date provided, using current date: {joining_date}")
                else:
                    print(f"Using selected joining date: {joining_date}")

                try:
                    Teacher.objects.create(
                        user=user,
                        teacher_id=teacher_id,
                        gender=gender,
                        date_of_birth=date_of_birth,
                        qualification=qualification,
                        specialization=specialization,
                        joining_date=joining_date,  # This will use the selected date
                        # নতুন address fields
                        division=division,
                        district=district,
                        thana=thana,
                        postal_code=postal_code,
                        area_village=area_village,
                        house_details=house_details
                    )
                    messages.success(request, f'Teacher account created successfully! Your Teacher ID is: {teacher_id}')
                    print("Teacher created successfully!")
                except Exception as e:
                    print(f"Error creating teacher: {e}")
                    messages.error(request, f'Error creating teacher account: {e}')
                    # Delete the user if teacher creation fails
                    user.delete()
                    return redirect('register')

            login(request, user)
            return redirect('dashboard')
        else:
            # Form errors debug korar jonno
            print("Form has errors, showing error message")
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

            # Attendance calculation
            try:
                attendance_count = Attendance.objects.filter(student=student, status='Present').count()
                total_days = Attendance.objects.filter(student=student).count()
                attendance_percentage = (attendance_count / total_days * 100) if total_days > 0 else 0
            except:
                attendance_count = 0
                total_days = 0
                attendance_percentage = 0

            # Books calculation
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