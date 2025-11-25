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
    list_display = ['class_name', 'day', 'subject', 'start_time', 'end_time']
    list_filter = ['class_name', 'day']

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