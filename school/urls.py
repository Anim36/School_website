from django.urls import path
from . import views

urlpatterns = [
    # Management URLs
    path('students/', views.student_management, name='student_management'),
    path('teachers/', views.teacher_management, name='teacher_management'),
    path('routine/', views.class_routine, name='class_routine'),
    path('notices/', views.notice_board, name='notice_board'),
    path('results/', views.results, name='results'),
    path('attendance/', views.attendance_tracking, name='attendance'),
    path('library/', views.library_management, name='library'),
    path('fees/', views.fee_payment, name='fee_payment'),
    path('admission/', views.online_admission, name='online_admission'),
    path('admission/success/<int:application_id>/', views.admission_success, name='admission_success'),
    path('add-notice/', views.add_notice, name='add_notice'),

    # Student specific URLs
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    path('student/profile/', views.student_profile, name='student_profile'),

    # Class Routine Management URLs
    path('routine/add/', views.add_class_routine, name='add_class_routine'),
    path('routine/manage/', views.manage_class_routines, name='manage_class_routines'),

    # New Pages
    path('about/', views.about, name='about'),
    path('teachers-members/', views.teachers_members, name='teachers_members'),

    # Gallery URLs
    path('gallery/', views.gallery, name='gallery'),
    path('gallery/add/', views.add_gallery_image, name='add_gallery_image'),
    path('gallery/manage/', views.manage_gallery, name='manage_gallery'),
    path('gallery/delete/<int:image_id>/', views.delete_gallery_image, name='delete_gallery_image'),

    # Contact URLs
    path('contact/', views.contact, name='contact'),
    path('contact/messages/', views.contact_messages, name='contact_messages'),
    path('contact/messages/<int:message_id>/', views.contact_message_detail, name='contact_message_detail'),
    path('contact/messages/<int:message_id>/responded/', views.mark_contact_responded, name='mark_contact_responded'),
    path('contact/messages/<int:message_id>/delete/', views.delete_contact_message, name='delete_contact_message'),
]