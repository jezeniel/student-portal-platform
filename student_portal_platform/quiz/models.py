from django.db import models
from django.contrib.auth.models import User

from subject.models import Subject

class Quiz(models.Model):
    subject = models.ForeignKey(Subject)
    title = models.CharField(max_length=100)
    create_date = models.DateTimeField(auto_now_add = True)
    start_date = models.DateTimeField()
    exp_date = models.DateTimeField()
    
    def __unicode__(self):
        return "%s:%s" % (self.subject.name,self.title)

class Question(models.Model):
    quiz = models.ForeignKey(Quiz)
    question = models.CharField(max_length=100)
    
    def __unicode__(self):
        return  "%s-%s" % (self.quiz.title,self.question) 
    
class Choice(models.Model):
    question = models.ForeignKey(Question)
    choice_text = models.CharField(max_length=100)
    is_correct = models.BooleanField(default = False)
    
    def __unicode__(self):
        return "%s : %s" % (self.question.question, self.choice_text) 

class QuizAttempt(models.Model):
    quiz = models.ForeignKey(Quiz)
    score = models.IntegerField(default=0)
    student = models.ForeignKey(User)

    def __unicode__(self):
        return "%s : %s - %d" % (self.quiz.title, self.student.username, self.score)
    
class QuizAnswer(models.Model):
    attempt = models.ForeignKey(QuizAttempt)
    answer = models.ManyToManyField(Choice)

    def __unicode__(self):
        return "%s - $s" % (self.attempt, self.answer.choice_text)
    