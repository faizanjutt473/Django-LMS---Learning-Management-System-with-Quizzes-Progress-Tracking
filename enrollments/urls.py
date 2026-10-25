from django.urls import path

from . import views

app_name = 'enrollments'

urlpatterns = [
    path('enroll/<slug:slug>/', views.enroll_course, name='enroll'),
    path('my-courses/', views.my_courses, name='my_courses'),
    path('complete/<int:lesson_id>/', views.complete_lesson, name='complete_lesson'),
]