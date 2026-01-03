from django.contrib import admin
from .models import Quiz, Question, QuizAttempt, StudentAnswer

class QuestionInline(admin.TabularInline):
    model = Question
    extra = 0

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]

admin.site.register(QuizAttempt)
admin.site.register(StudentAnswer)
