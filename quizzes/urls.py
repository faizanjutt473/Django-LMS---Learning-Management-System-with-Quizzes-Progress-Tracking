from django.urls import path

from . import views

app_name = 'quizzes'

urlpatterns = [
    path('create/<slug:slug>/', views.quiz_create, name='quiz_create'),
    path('<int:quiz_id>/add-question/', views.question_create, name='question_create'),
    path('<int:quiz_id>/take/', views.take_quiz, name='take_quiz'),
    path('result/<int:result_id>/', views.quiz_result, name='quiz_result'),
    path('my-results/', views.my_results, name='my_results'),
]