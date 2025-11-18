from django.contrib import admin
from .models import Quiz, Question, QuizAttempt, StudentAnswer

# Inline for editing questions inside a quiz
class QuestionInline(admin.TabularInline):
    model = Question
    extra = 0

# Quiz admin
@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]  # Show questions inside the quiz
    list_display = ('title', 'status', 'publish_date', 'created_at')
    list_filter = ('status',)
    search_fields = ('title',)
    ordering = ('-created_at',)

# Question admin (separate view)
@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('quiz', 'id', 'question_text')
    search_fields = ('quiz__title', 'question_text')

# QuizAttempt admin
@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = ('student', 'quiz', 'start_time', 'submitted_at', 'total_score')
    list_filter = ('quiz', 'start_time')
    search_fields = ('student__username', 'quiz__title')

# StudentAnswer admin
@admin.register(StudentAnswer)
class StudentAnswerAdmin(admin.ModelAdmin):
    list_display = ('attempt', 'question', 'selected_option', 'is_correct', 'marks_obtained')
    search_fields = ('attempt__student__username', 'question__question_text')
