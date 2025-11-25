from django.urls import path
from . import views

urlpatterns = [
    path('students/', views.student_management, name='student_management'),
    path('teachers/', views.teacher_management, name='teacher_management'),
    path('routine/', views.class_routine, name='class_routine'),
    path('notices/', views.notice_board, name='notice_board'),
    path('results/', views.results, name='results'),
    path('attendance/', views.attendance_tracking, name='attendance'),
    path('library/', views.library_management, name='library'),
    path('fees/', views.fee_payment, name='fee_payment'),
    path('admission/', views.online_admission, name='online_admission'),
    #path('parent-portal/', views.parent_portal, name='parent_portal'),
    path('add-notice/', views.add_notice, name='add_notice'),
]