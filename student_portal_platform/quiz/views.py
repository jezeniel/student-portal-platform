from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, render_to_response, redirect
from django.contrib.auth.models import User

from .models import Quiz, QuizAttempt, Question, Choice, QuizAnswer
from .forms import QuizForm
from subject.models import Subject

def quiz_view(request, quiz_id):
    quiz = get_object_or_404(Quiz, id = quiz_id)

    if request.method == "GET":
        form = QuizForm(questions = quiz.question_set.order_by('?'))

    if request.method == "POST":
        form = QuizForm(request.POST ,questions = quiz.question_set.all())
        if form.is_valid():
            answers = [int(value) for name, value in form.cleaned_data.items()]
            quiz_attempt = QuizAttempt.objects.create(quiz = quiz,
                                                      student = request.user)
            quiz_answer = QuizAnswer.objects.create(attempt = quiz_attempt)

            for answer in answers:
                choice = Choice.objects.get(id = answer)
                quiz_answer.answer.add(choice)
                if choice.is_correct:
                    quiz_attempt.score += 1

            quiz_answer.save()
            quiz_attempt.save()
            return HttpResponse("Quiz Successfully Passed!")

    return render(request, 'final/quiz.html', {'form': form, 'quiz_id': quiz_id })


def quiz_delete(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    subject = quiz.subject
    quiz.delete()
    return redirect(subject.get_absolute_url())
