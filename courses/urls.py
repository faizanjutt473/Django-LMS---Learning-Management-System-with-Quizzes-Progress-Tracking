from django.urls import path

from . import views

app_name = 'courses'

urlpatterns = [
    path('', views.course_list, name='course_list'),
    path('create/', views.course_create, name='course_create'),
    path('<slug:slug>/', views.course_detail, name='course_detail'),
    path('<slug:slug>/edit/', views.course_edit, name='course_edit'),
    path('<slug:slug>/delete/', views.course_delete, name='course_delete'),
    path('<slug:slug>/add-module/', views.module_create, name='module_create'),
    path('module/<int:module_id>/add-lesson/', views.lesson_create, name='lesson_create'),
    path('<slug:slug>/lesson/<int:lesson_id>/', views.lesson_detail, name='lesson_detail'),
]