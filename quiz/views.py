from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Quiz, Question, QuizAttempt, StudentAnswer
from django.utils import timezone

@login_required
def dashboard(request):
    return render(request, 'quiz/quiz_list.html', {'quizzes': Quiz.objects.all()})

@login_required
def quiz_list(request):
    quizzes = Quiz.objects.all()
    return render(request, 'quiz/quiz_list.html', {'quizzes': quizzes})

@login_required
def quiz_instructions(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    return render(request, 'quiz/quiz_instructions.html', {'quiz': quiz})

@login_required
def start_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    attempt = QuizAttempt.objects.create(student=request.user, quiz=quiz)
    for q in quiz.questions.all():
        StudentAnswer.objects.create(attempt=attempt, question=q)
    duration_seconds = quiz.duration * 60
    questions = quiz.questions.all()
    return render(request, 'quiz/take_quiz.html', {
        'quiz': quiz,
        'attempt': attempt,
        'questions': questions,
        'duration_seconds': duration_seconds,
    })

@login_required
def submit_quiz(request, attempt_id):
    attempt = get_object_or_404(QuizAttempt, id=attempt_id, student=request.user)
    quiz = attempt.quiz
    if attempt.submitted_at:
        return redirect('quiz:result', attempt_id=attempt.id)

    now = timezone.now()
    attempt.submitted_at = now
    time_taken_seconds = int((now - attempt.start_time).total_seconds())
    attempt.time_taken = time_taken_seconds

    total_score = 0
    for sa in attempt.answers.select_related('question').all():
        q = sa.question
        selected = request.POST.get(f'q_{q.id}', '')
        sa.selected_option = selected if selected else None
        if selected and selected == q.correct_answer:
            sa.is_correct = True
            sa.marks_obtained = q.marks
            total_score += q.marks
        else:
            sa.is_correct = False
            sa.marks_obtained = 0
        sa.save()

    attempt.total_score = total_score
    attempt.save()

    return redirect('quiz:result', attempt_id=attempt.id)

@login_required
def result_view(request, attempt_id):
    attempt = get_object_or_404(QuizAttempt, id=attempt_id, student=request.user)
    answers = attempt.answers.select_related('question').all()
    return render(request, 'quiz/result.html', {'attempt': attempt, 'answers': answers})

@login_required
def leaderboard(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    attempts = QuizAttempt.objects.filter(quiz=quiz, total_score__isnull=False).order_by('-total_score', 'time_taken')[:50]
    return render(request, 'quiz/leaderboard.html', {'quiz': quiz, 'attempts': attempts})
