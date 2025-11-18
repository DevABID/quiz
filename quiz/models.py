from django.db import models
from django.utils import timezone
from django.conf import settings

User = settings.AUTH_USER_MODEL

class Quiz(models.Model):
    STATUS_CHOICES = [('draft', 'Draft'), ('published', 'Published')]

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    duration = models.PositiveIntegerField(help_text='Duration in minutes')
    total_marks = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    publish_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def check_auto_publish(self):
        """Automatically publish if publish_date is reached"""
        if self.status == 'draft' and self.publish_date and self.publish_date <= timezone.now():
            self.status = 'published'
            self.save(update_fields=['status'])

    def is_published(self):
        # Check and auto-update
        self.check_auto_publish()
        return self.status == 'published'

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    # Optional question image
    image = models.ImageField(upload_to='question_images/', blank=True, null=True)

    # Optional question text
    question_text = models.TextField(blank=True, null=True)

    # Options (text optional, image optional)
    option1 = models.CharField(max_length=300, blank=True, null=True)
    option1_image = models.ImageField(upload_to='option_images/', blank=True, null=True)

    option2 = models.CharField(max_length=300, blank=True, null=True)
    option2_image = models.ImageField(upload_to='option_images/', blank=True, null=True)

    option3 = models.CharField(max_length=300, blank=True, null=True)
    option3_image = models.ImageField(upload_to='option_images/', blank=True, null=True)

    option4 = models.CharField(max_length=300, blank=True, null=True)
    option4_image = models.ImageField(upload_to='option_images/', blank=True, null=True)

    CORRECT_CHOICES = [('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')]
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
