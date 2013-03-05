from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, render_to_response
from django.contrib.auth.models import User

from quiz.models import Quiz, QuizAttempt, Choice, QuizAnswer
from quiz.forms import QuizForm

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
                
    return render(request, 'development/quiz.html', {'form': form, 'quiz_id': quiz_id })
    