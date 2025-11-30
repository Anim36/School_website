from django.contrib import admin
from .models import *

@admin.register(SchoolInfo)
class SchoolInfoAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'email']

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['student_id', 'user', 'class_name', 'section', 'roll_number']
    list_filter = ['class_name', 'section']
    search_fields = ['student_id', 'user__first_name', 'user__last_name']

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['teacher_id', 'user', 'qualification', 'specialization']
    search_fields = ['teacher_id', 'user__first_name', 'user__last_name']


@admin.register(RoutinePeriod)
class RoutinePeriodAdmin(admin.ModelAdmin):
    list_display = ['start_time', 'end_time', 'is_break', 'break_name', 'order']
    list_filter = ['is_break']
    ordering = ['order', 'start_time']

@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ['name', 'section', 'class_teacher']
    list_filter = ['name', 'section']

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'class_name', 'teacher']
    list_filter = ['class_name', 'teacher']

@admin.register(ClassRoutine)
class ClassRoutineAdmin(admin.ModelAdmin):
    list_display = ['class_name', 'day', 'period', 'subject', 'teacher']  # ✅ period use korbo
    list_filter = ['class_name', 'day', 'teacher']
    search_fields = ['class_name__name', 'subject__name', 'teacher__user__first_name', 'teacher__user__last_name']

@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ['title', 'target_audience', 'created_at']
    list_filter = ['target_audience', 'created_at']
    search_fields = ['title', 'content']

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['student', 'date', 'status', 'class_name']
    list_filter = ['date', 'status', 'class_name']

@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ['student', 'subject', 'exam_name', 'marks', 'grade']
    list_filter = ['exam_name', 'grade']

@admin.register(Fee)
class FeeAdmin(admin.ModelAdmin):
    list_display = ['student', 'amount', 'due_date', 'paid']
    list_filter = ['paid', 'due_date']

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'isbn', 'quantity', 'available']
    search_fields = ['title', 'author', 'isbn']

@admin.register(BookIssue)
class BookIssueAdmin(admin.ModelAdmin):
    list_display = ['book', 'student', 'issue_date', 'return_date', 'returned']
    list_filter = ['returned', 'issue_date']


@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'uploaded_by', 'upload_date', 'is_active']
    list_filter = ['category', 'is_active', 'upload_date']
    search_fields = ['title', 'description']


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'submitted_at', 'is_read', 'responded']
    list_filter = ['subject', 'is_read', 'responded', 'submitted_at']
    search_fields = ['name', 'email', 'message']
    readonly_fields = ['submitted_at']

    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)

    mark_as_read.short_description = "Mark selected messages as read"

    def mark_as_responded(self, request, queryset):
        queryset.update(responded=True)

    mark_as_responded.short_description = "Mark selected messages as responded"

    actions = [mark_as_read, mark_as_responded]


@admin.register(AdmissionApplication)
class AdmissionApplicationAdmin(admin.ModelAdmin):
    list_display = ['name', 'class_applying', 'email', 'phone', 'application_date', 'status']
    list_filter = ['status', 'class_applying', 'application_date', 'gender']
    search_fields = ['name', 'email', 'phone', 'father_name', 'mother_name']
    readonly_fields = ['application_date']
    list_editable = ['status']

    def mark_as_reviewed(self, request, queryset):
        queryset.update(status='reviewed')

    mark_as_reviewed.short_description = "Mark selected applications as reviewed"

    def mark_as_accepted(self, request, queryset):
        queryset.update(status='accepted')

    mark_as_accepted.short_description = "Mark selected applications as accepted"

    def mark_as_rejected(self, request, queryset):
        queryset.update(status='rejected')

    mark_as_rejected.short_description = "Mark selected applications as rejected"

    actions = [mark_as_reviewed, mark_as_accepted, mark_as_rejected]