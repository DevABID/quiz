from django.urls import path
from . import views

app_name = 'quiz'

urlpatterns = [
    path('', views.quiz_list, name='quiz_list'),
    path('<int:quiz_id>/start/', views.start_quiz, name='start_quiz'),
    path('submit/<int:attempt_id>/', views.submit_quiz, name='submit_quiz'),
    path('result/<int:attempt_id>/', views.result_view, name='result'),
    path('<int:quiz_id>/leaderboard/', views.leaderboard, name='leaderboard'),
]
