from django.db import models
from django.conf import settings
from django.utils import timezone

User = settings.AUTH_USER_MODEL

class Quiz(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    duration = models.PositiveIntegerField(help_text='Duration in minutes')
    total_marks = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()
    option1 = models.CharField(max_length=300)
    option2 = models.CharField(max_length=300)
    option3 = models.CharField(max_length=300)
    option4 = models.CharField(max_length=300)
    CORRECT_CHOICES = [('1','1'),('2','2'),('3','3'),('4','4')]
    correct_answer = models.CharField(max_length=1, choices=CORRECT_CHOICES)
    marks = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quiz.title} - Q{self.id}"

class QuizAttempt(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    start_time = models.DateTimeField(default=timezone.now)
    submitted_at = models.DateTimeField(null=True, blank=True)
    total_score = models.FloatField(null=True, blank=True)
    time_taken = models.PositiveIntegerField(null=True, blank=True, help_text='time taken in seconds')

    def __str__(self):
        return f"{self.student} - {self.quiz}"

class StudentAnswer(models.Model):
    attempt = models.ForeignKey(QuizAttempt, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_option = models.CharField(max_length=1, blank=True, null=True)
    is_correct = models.BooleanField(default=False)
    marks_obtained = models.FloatField(default=0)

    def __str__(self):
        return f"Ans: {self.attempt} - Q{self.question.id}"
