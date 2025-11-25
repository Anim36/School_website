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
    path('add-notice/', views.add_notice, name='add_notice'),

    # Student specific URLs
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    path('student/profile/', views.student_profile, name='student_profile'),

    # Class Routine Management URLs
    path('routine/add/', views.add_class_routine, name='add_class_routine'),
    path('routine/manage/', views.manage_class_routines, name='manage_class_routines'),
    path('routine/edit/<int:routine_id>/', views.edit_class_routine, name='edit_class_routine'),
    path('routine/delete/<int:routine_id>/', views.delete_class_routine, name='delete_class_routine'),

    # New Pages
    path('about/', views.about, name='about'),
    path('teachers-members/', views.teachers_members, name='teachers_members'),

    # Gallery URLs
    path('gallery/', views.gallery, name='gallery'),
    path('gallery/add/', views.add_gallery_image, name='add_gallery_image'),
    path('gallery/manage/', views.manage_gallery, name='manage_gallery'),
    path('gallery/delete/<int:image_id>/', views.delete_gallery_image, name='delete_gallery_image'),

]