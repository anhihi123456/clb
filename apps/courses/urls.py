from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [
    # Giao diện học viên & chung
    path('', views.course_list, name='course_list'),
    path('<str:course_code>/', views.course_detail, name='course_detail'),
    path('<str:course_code>/enroll/', views.enroll_course, name='enroll_course'),
    path('<str:course_code>/lesson/<int:order>/', views.lesson_detail, name='lesson_detail'),

    # Giao diện Giảng viên (Teacher setup)
    path('teacher/dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('teacher/<str:course_code>/lessons/', views.teacher_lesson_list, name='teacher_lesson_list'),
    path('teacher/<str:course_code>/lessons/create/', views.teacher_lesson_create, name='teacher_lesson_create'),
    path('teacher/<str:course_code>/lessons/<int:lesson_id>/edit/', views.teacher_lesson_update, name='teacher_lesson_update'),
    path('teacher/<str:course_code>/lessons/<int:lesson_id>/delete/', views.teacher_lesson_delete, name='teacher_lesson_delete'),

    # API hỗ trợ Live Preview
    path('api/parse-embed/', views.api_parse_embed_preview, name='api_parse_embed'),
]

