from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('quizzes/', views.quiz_list, name='quiz_list'),
    path('quiz/<int:quiz_id>/instructions/', views.quiz_instructions, name='quiz_instructions'),
    path('quiz/<int:quiz_id>/start/', views.start_quiz, name='start_quiz'),
    path('quiz/<int:attempt_id>/submit/', views.submit_quiz, name='submit_quiz'),
    path('attempt/<int:attempt_id>/result/', views.result_view, name='result'),
    path('quiz/<int:quiz_id>/leaderboard/', views.leaderboard, name='leaderboard'),
]
