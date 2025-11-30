from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden, JsonResponse
from .models import *
from .forms import NoticeForm, ClassRoutineForm, GalleryForm, ContactForm, AdmissionForm, RoutinePeriodForm, \
    BulkRoutineForm


def home(request):
    notices = Notice.objects.all().order_by('-created_at')[:5]
    return render(request, 'school/home.html', {'notices': notices})


def about(request):
    """About School Page"""
    context = {
        'school_info': SchoolInfo.objects.first(),
        'teachers_count': Teacher.objects.count(),
        'students_count': Student.objects.count(),
    }
    return render(request, 'school/about.html', context)


def teachers_members(request):
    """Teachers Members Page"""
    teachers = Teacher.objects.all().select_related('user')
    context = {
        'teachers': teachers,
        'school_info': SchoolInfo.objects.first(),
    }
    return render(request, 'school/teachers_members.html', context)


def gallery(request):
    """Gallery Page"""
    categories = Gallery.CATEGORY_CHOICES
    selected_category = request.GET.get('category', 'all')

    if selected_category == 'all':
        images = Gallery.objects.filter(is_active=True)
    else:
        images = Gallery.objects.filter(category=selected_category, is_active=True)

    context = {
        'images': images,
        'categories': categories,
        'selected_category': selected_category,
    }
    return render(request, 'school/gallery.html', context)


@login_required
def add_gallery_image(request):
    """Add new image to gallery (Admin and Teachers only)"""
    if request.user.user_type not in ['admin', 'teacher']:
        return HttpResponseForbidden("You don't have permission to access this page.")

    if request.method == 'POST':
        form = GalleryForm(request.POST, request.FILES)
        if form.is_valid():
            gallery_item = form.save(commit=False)
            gallery_item.uploaded_by = request.user
            gallery_item.save()
            messages.success(request, 'Image added to gallery successfully!')
            return redirect('gallery')
    else:
        form = GalleryForm()

    return render(request, 'school/add_gallery_image.html', {'form': form})


@login_required
def manage_gallery(request):
    """Manage gallery images (Admin and Teachers only)"""
    if request.user.user_type not in ['admin', 'teacher']:
        return HttpResponseForbidden("You don't have permission to access this page.")

    images = Gallery.objects.all().order_by('-upload_date')
    return render(request, 'school/manage_gallery.html', {'images': images})


@login_required
def delete_gallery_image(request, image_id):
    """Delete gallery image"""
    if request.user.user_type not in ['admin', 'teacher']:
        return HttpResponseForbidden("You don't have permission to access this page.")

    image = get_object_or_404(Gallery, id=image_id)

    # Check if user owns the image or is admin
    if image.uploaded_by != request.user and request.user.user_type != 'admin':
        return HttpResponseForbidden("You can only delete your own images.")

    if request.method == 'POST':
        image.delete()
        messages.success(request, 'Image deleted successfully!')
        return redirect('manage_gallery')

    return render(request, 'school/delete_gallery_image.html', {'image': image})


def contact(request):
    """Contact Page"""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_message = form.save()
            messages.success(request, 'Thank you for your message! We will get back to you soon.')
            return redirect('contact')
    else:
        form = ContactForm()

    context = {
        'form': form,
        'school_info': SchoolInfo.objects.first(),
    }
    return render(request, 'school/contact.html', context)


@login_required
def contact_messages(request):
    """View contact messages (Admin and Teachers only)"""
    if request.user.user_type not in ['admin', 'teacher']:
        return HttpResponseForbidden("You don't have permission to access this page.")

    messages_list = Contact.objects.all()

    # Filter by status if provided
    status_filter = request.GET.get('status', 'all')
    if status_filter == 'unread':
        messages_list = messages_list.filter(is_read=False)
    elif status_filter == 'read':
        messages_list = messages_list.filter(is_read=True)
    elif status_filter == 'responded':
        messages_list = messages_list.filter(responded=True)

    context = {
        'messages': messages_list,
        'status_filter': status_filter,
    }
    return render(request, 'school/contact_messages.html', context)


@login_required
def contact_message_detail(request, message_id):
    """View contact message details"""
    if request.user.user_type not in ['admin', 'teacher']:
        return HttpResponseForbidden("You don't have permission to access this page.")

    message = get_object_or_404(Contact, id=message_id)

    # Mark as read when viewed
    if not message.is_read:
        message.is_read = True
        message.save()

    context = {
        'message': message,
    }
    return render(request, 'school/contact_message_detail.html', context)


@login_required
def mark_contact_responded(request, message_id):
    """Mark contact message as responded"""
    if request.user.user_type not in ['admin', 'teacher']:
        return HttpResponseForbidden("You don't have permission to access this page.")

    message = get_object_or_404(Contact, id=message_id)

    if request.method == 'POST':
        message.responded = True
        message.save()
        messages.success(request, 'Message marked as responded.')
        return redirect('contact_messages')

    return redirect('contact_message_detail', message_id=message_id)


@login_required
def delete_contact_message(request, message_id):
    """Delete contact message"""
    if request.user.user_type not in ['admin', 'teacher']:
        return HttpResponseForbidden("You don't have permission to access this page.")

    message = get_object_or_404(Contact, id=message_id)

    if request.method == 'POST':
        message.delete()
        messages.success(request, 'Message deleted successfully.')
        return redirect('contact_messages')

    context = {
        'message': message,
    }
    return render(request, 'school/delete_contact_message.html', context)


@login_required
def student_management(request):
    if request.user.user_type not in ['admin', 'teacher']:
        return HttpResponseForbidden("You don't have permission to access this page.")

    students = Student.objects.all()
    return render(request, 'school/student_management.html', {'students': students})


@login_required
def teacher_management(request):
    if request.user.user_type != 'admin':
        return HttpResponseForbidden("You don't have permission to access this page.")

    teachers = Teacher.objects.all()
    return render(request, 'school/teacher_management.html', {'teachers': teachers})


@login_required
def manage_routine_periods(request):
    """Manage routine periods (time slots)"""
    if request.user.user_type not in ['admin', 'teacher']:
        return HttpResponseForbidden("You don't have permission to access this page.")

    periods = RoutinePeriod.objects.all()

    if request.method == 'POST':
        form = RoutinePeriodForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Routine period added successfully!')
            return redirect('manage_routine_periods')
    else:
        form = RoutinePeriodForm()

    context = {
        'periods': periods,
        'form': form
    }
    return render(request, 'school/manage_routine_periods.html', context)


@login_required
def edit_routine_period(request, period_id):
    """Edit routine period"""
    if request.user.user_type not in ['admin', 'teacher']:
        return HttpResponseForbidden("You don't have permission to access this page.")

    period = get_object_or_404(RoutinePeriod, id=period_id)

    if request.method == 'POST':
        form = RoutinePeriodForm(request.POST, instance=period)
        if form.is_valid():
            form.save()
            messages.success(request, 'Routine period updated successfully!')
            return redirect('manage_routine_periods')
    else:
        form = RoutinePeriodForm(instance=period)

    context = {
        'form': form,
        'period': period
    }
    return render(request, 'school/edit_routine_period.html', context)


@login_required
def delete_routine_period(request, period_id):
    """Delete routine period"""
    if request.user.user_type not in ['admin', 'teacher']:
        return HttpResponseForbidden("You don't have permission to access this page.")

    period = get_object_or_404(RoutinePeriod, id=period_id)

    if request.method == 'POST':
        # Check if this period is used in any routine
        if ClassRoutine.objects.filter(period=period).exists():
            messages.error(request, 'Cannot delete this period because it is used in class routines!')
        else:
            period.delete()
            messages.success(request, 'Routine period deleted successfully!')
        return redirect('manage_routine_periods')

    context = {
        'period': period
    }
    return render(request, 'school/delete_routine_period.html', context)


@login_required
def add_class_routine(request):
    """Add class routine with improved interface"""
    if request.user.user_type not in ['admin', 'teacher']:
        return HttpResponseForbidden("You don't have permission to access this page.")

    # Check if RoutinePeriod table exists and has data
    try:
        periods = RoutinePeriod.objects.filter(is_break=False)
        if not periods.exists():
            messages.warning(request, 'No routine periods found. Please add periods first.')
            return redirect('manage_routine_periods')
    except:
        messages.error(request, 'Routine system is not set up properly.')
        return redirect('class_routine')

    single_form = ClassRoutineForm()
    bulk_form = BulkRoutineForm()

    # Get data for template
    classes = Class.objects.all()
    teachers = Teacher.objects.all()
    days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']

    # Handle single routine form
    if request.method == 'POST' and 'single_routine' in request.POST:
        single_form = ClassRoutineForm(request.POST)
        if single_form.is_valid():
            class_name = single_form.cleaned_data['class_name']
            day = single_form.cleaned_data['day']
            period = single_form.cleaned_data['period']
            subject_name = single_form.cleaned_data['subject']  # ✅ Text input থেকে subject name নিন
            teacher = single_form.cleaned_data['teacher']

            # Check for duplicate
            if ClassRoutine.objects.filter(class_name=class_name, day=day, period=period).exists():
                messages.error(request, f'A routine already exists for {class_name} on {day} during {period}.')
            else:
                # ✅ Subject create বা get করুন
                subject, created = Subject.objects.get_or_create(
                    name=subject_name,
                    class_name=class_name,
                    defaults={'teacher': teacher}
                )

                # ClassRoutine create করুন
                ClassRoutine.objects.create(
                    class_name=class_name,
                    day=day,
                    period=period,
                    subject=subject,
                    teacher=teacher
                )

                messages.success(request, f'Routine added successfully for {class_name} on {day}!')
                return redirect('add_class_routine')

    # Handle bulk routine form
    elif request.method == 'POST' and 'bulk_routine' in request.POST:
        bulk_form = BulkRoutineForm(request.POST)
        if bulk_form.is_valid():
            class_name = bulk_form.cleaned_data['class_name']
            day = bulk_form.cleaned_data['day']

            periods = RoutinePeriod.objects.filter(is_break=False).order_by('order')
            routines_created = 0

            for period in periods:
                subject_field = f'period_{period.id}_subject'
                teacher_field = f'period_{period.id}_teacher'

                subject_name = bulk_form.cleaned_data.get(subject_field)  # ✅ Text input থেকে subject name
                teacher = bulk_form.cleaned_data.get(teacher_field)

                # Only create routine if both subject name and teacher are provided
                if subject_name and teacher:  # ✅ subject_name check করুন (empty string check)
                    subject_name = subject_name.strip()
                    if subject_name:  # ✅ শুধু whitespace না হলে
                        # Check for duplicate
                        if not ClassRoutine.objects.filter(class_name=class_name, day=day, period=period).exists():
                            # ✅ Subject create বা get করুন
                            subject, created = Subject.objects.get_or_create(
                                name=subject_name,
                                class_name=class_name,
                                defaults={'teacher': teacher}
                            )

                            ClassRoutine.objects.create(
                                class_name=class_name,
                                day=day,
                                period=period,
                                subject=subject,
                                teacher=teacher
                            )
                            routines_created += 1

            if routines_created > 0:
                messages.success(request,
                                 f'Successfully created {routines_created} routines for {class_name} on {day}!')
            else:
                messages.warning(request, 'No routines were created. Please fill in at least one period.')

            return redirect('add_class_routine')

    context = {
        'single_form': single_form,
        'bulk_form': bulk_form,
        'classes': classes,
        'teachers': teachers,
        'days': days,
        'periods': periods,
    }

    return render(request, 'school/add_class_routine.html', context)


@login_required
def edit_class_routine(request, routine_id):
    """Edit class routine"""
    if request.user.user_type not in ['admin', 'teacher']:
        return HttpResponseForbidden("You don't have permission to access this page.")

    routine = get_object_or_404(ClassRoutine, id=routine_id)

    if request.method == 'POST':
        form = ClassRoutineForm(request.POST, instance=routine)
        if form.is_valid():
            # ✅ Subject update করার logic
            subject_name = form.cleaned_data['subject']  # Text input থেকে subject name
            teacher = form.cleaned_data['teacher']

            # Subject update বা create করুন
            subject, created = Subject.objects.get_or_create(
                name=subject_name,
                class_name=routine.class_name,
                defaults={'teacher': teacher}
            )

            # Routine update করুন
            routine.subject = subject
            routine.teacher = teacher
            routine.day = form.cleaned_data['day']
            routine.period = form.cleaned_data['period']
            routine.save()

            messages.success(request, 'Class routine updated successfully!')
            return redirect('manage_class_routines')
    else:
        # Initial form load-এ current subject name set করুন
        form = ClassRoutineForm(instance=routine)
        form.fields['subject'].initial = routine.subject.name  # ✅ Text field-এ current subject name set করুন

    context = {
        'form': form,
        'routine': routine
    }
    return render(request, 'school/edit_class_routine.html', context)


@login_required
def delete_class_routine(request, routine_id):
    """Delete class routine"""
    if request.user.user_type not in ['admin', 'teacher']:
        return HttpResponseForbidden("You don't have permission to access this page.")

    routine = get_object_or_404(ClassRoutine, id=routine_id)

    if request.method == 'POST':
        routine.delete()
        messages.success(request, 'Class routine deleted successfully!')
        return redirect('manage_class_routines')

    context = {
        'routine': routine
    }
    return render(request, 'school/delete_class_routine.html', context)


@login_required
def class_routine(request):
    """Display class routine in Excel-like table"""
    try:
        # Check if RoutinePeriod table exists
        RoutinePeriod.objects.exists()
    except:
        messages.error(request, 'Routine system is being set up. Please try again in a moment.')
        return render(request, 'school/class_routine.html', {
            'routine_matrix': {},
            'periods': [],
            'days': ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday'],
            'classes': Class.objects.all(),
        })

    routines = ClassRoutine.objects.all().select_related('class_name', 'period', 'subject', 'teacher')

    if request.user.user_type == 'student':
        try:
            student = Student.objects.get(user=request.user)
            routines = routines.filter(class_name__name=student.class_name)
        except Student.DoesNotExist:
            routines = ClassRoutine.objects.none()
    elif request.user.user_type == 'teacher':
        try:
            teacher = Teacher.objects.get(user=request.user)
            routines = routines.filter(teacher=teacher)
        except Teacher.DoesNotExist:
            routines = ClassRoutine.objects.none()

    # Organize data for template
    periods = RoutinePeriod.objects.all()
    days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday']
    classes = Class.objects.all()

    # Create routine matrix
    routine_matrix = {}
    for class_obj in classes:
        routine_matrix[class_obj.id] = {}
        for day in days:
            routine_matrix[class_obj.id][day] = {}
            for period in periods:
                try:
                    routine = routines.get(class_name=class_obj, day=day, period=period)
                    routine_matrix[class_obj.id][day][period.id] = {
                        'subject': routine.subject.name,
                        'teacher': routine.teacher.user.get_full_name(),
                        'id': routine.id
                    }
                except ClassRoutine.DoesNotExist:
                    routine_matrix[class_obj.id][day][period.id] = None

    context = {
        'routine_matrix': routine_matrix,
        'periods': periods,
        'days': days,
        'classes': classes,
    }
    return render(request, 'school/class_routine.html', context)


@login_required
def manage_class_routines(request):
    """Manage all class routines"""
    if request.user.user_type not in ['admin', 'teacher']:
        return HttpResponseForbidden("You don't have permission to access this page.")

    routines = ClassRoutine.objects.all().select_related('class_name', 'period', 'subject', 'teacher')

    if request.user.user_type == 'teacher':
        try:
            teacher = Teacher.objects.get(user=request.user)
            routines = routines.filter(teacher=teacher)
        except Teacher.DoesNotExist:
            routines = ClassRoutine.objects.none()

    context = {
        'routines': routines
    }
    return render(request, 'school/manage_class_routines.html', context)


@login_required
def get_routine_data(request):
    """API endpoint to get routine data for specific class and day"""
    class_id = request.GET.get('class_id')
    day = request.GET.get('day')

    routines = ClassRoutine.objects.filter(
        class_name_id=class_id,
        day=day
    ).select_related('period', 'subject', 'teacher')

    data = {}
    for routine in routines:
        data[routine.period.id] = {
            'subject': routine.subject.name,
            'teacher': routine.teacher.user.get_full_name(),
            'routine_id': routine.id
        }

    return JsonResponse(data)


@login_required
def get_subjects_by_class(request):
    """API endpoint to get subjects by class"""
    class_id = request.GET.get('class_id')
    if class_id:
        subjects = Subject.objects.filter(class_name_id=class_id)
        data = {str(subject.id): str(subject) for subject in subjects}
    else:
        data = {}

    return JsonResponse(data)


@login_required
def get_existing_routines(request):
    """API endpoint to get existing routines for a class and day"""
    class_id = request.GET.get('class_id')
    day = request.GET.get('day')

    routines = {}
    if class_id and day:
        existing_routines = ClassRoutine.objects.filter(
            class_name_id=class_id,
            day=day
        ).select_related('period', 'subject', 'teacher')

        for routine in existing_routines:
            routines[str(routine.period.id)] = {
                'subject_name': str(routine.subject.name),  # ✅ Subject name পাঠান
                'teacher_name': str(routine.teacher.user.get_full_name()),
            }

    return JsonResponse(routines)


@login_required
def notice_board(request):
    notices = Notice.objects.all().order_by('-created_at')

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
        try:
            teacher = Teacher.objects.get(user=request.user)
            subjects = Subject.objects.filter(teacher=teacher)
            results = Result.objects.filter(subject__in=subjects)
        except Teacher.DoesNotExist:
            pass
    else:
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
        try:
            teacher = Teacher.objects.get(user=request.user)
            classes = Class.objects.filter(class_teacher=teacher)
            attendance = Attendance.objects.filter(class_name__in=classes)
        except Teacher.DoesNotExist:
            pass
    else:
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
    else:
        fees = Fee.objects.all()

    return render(request, 'school/fee_payment.html', {'fees': fees})


def online_admission(request):
    """
    Online admission form that doesn't require login
    New students can apply for admission without having an account
    """
    if request.method == 'POST':
        form = AdmissionForm(request.POST, request.FILES)
        if form.is_valid():
            admission_application = form.save()

            # Success page এ redirect করবো
            return redirect('admission_success', application_id=admission_application.id)
        else:
            # Debug: Print form errors to console
            print("FORM ERRORS:", form.errors)
            print("FORM NON FIELD ERRORS:", form.non_field_errors())
            messages.error(request, 'Please correct the errors below.')
    else:
        form = AdmissionForm()

    return render(request, 'school/online_admission.html', {'form': form})


def admission_success(request, application_id):
    """Admission application success page"""
    application = get_object_or_404(AdmissionApplication, id=application_id)

    context = {
        'application': application,
        'school_info': SchoolInfo.objects.first(),
    }
    return render(request, 'school/admission_success.html', context)


@login_required
def add_notice(request):
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


@login_required
def student_dashboard(request):
    if request.user.user_type != 'student':
        return HttpResponseForbidden("You don't have permission to access this page.")

    try:
        student = Student.objects.get(user=request.user)

        attendance_count = Attendance.objects.filter(student=student, status='Present').count()
        total_days = Attendance.objects.filter(student=student).count()
        attendance_percentage = (attendance_count / total_days * 100) if total_days > 0 else 0

        recent_results = Result.objects.filter(student=student).order_by('-id')[:3]
        recent_notices = Notice.objects.filter(target_audience__in=['Students', 'All']).order_by('-created_at')[:3]

        total_fees = Fee.objects.filter(student=student).count()
        paid_fees = Fee.objects.filter(student=student, paid=True).count()
        pending_fees = total_fees - paid_fees

        issued_books = BookIssue.objects.filter(student=student, returned=False).count()

        context = {
            'student': student,
            'attendance_percentage': round(attendance_percentage, 2),
            'attendance_count': attendance_count,
            'total_days': total_days,
            'recent_results': recent_results,
            'recent_notices': recent_notices,
            'total_books': issued_books,
            'total_fees': total_fees,
            'paid_fees': paid_fees,
            'pending_fees': pending_fees,
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


@login_required
def create_default_periods(request):
    """Create default routine periods"""
    if request.user.user_type not in ['admin', 'teacher']:
        return HttpResponseForbidden("You don't have permission to access this page.")

    # Default periods based on your Excel sheet
    default_periods = [
        {'start_time': '09:00', 'end_time': '09:45', 'is_break': False, 'break_name': '', 'order': 1},
        {'start_time': '09:45', 'end_time': '10:30', 'is_break': False, 'break_name': '', 'order': 2},
        {'start_time': '10:30', 'end_time': '11:15', 'is_break': False, 'break_name': '', 'order': 3},
        {'start_time': '11:15', 'end_time': '12:00', 'is_break': True, 'break_name': 'Break Time', 'order': 4},
        {'start_time': '12:00', 'end_time': '12:45', 'is_break': False, 'break_name': '', 'order': 5},
        {'start_time': '12:45', 'end_time': '13:30', 'is_break': False, 'break_name': '', 'order': 6},
    ]

    created_count = 0
    for period_data in default_periods:
        period, created = RoutinePeriod.objects.get_or_create(
            start_time=period_data['start_time'],
            end_time=period_data['end_time'],
            defaults=period_data
        )
        if created:
            created_count += 1

    if created_count > 0:
        messages.success(request, f'Successfully created {created_count} default periods!')
    else:
        messages.info(request, 'All default periods already exist.')

    return redirect('manage_routine_periods')