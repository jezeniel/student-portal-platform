from django.db import models
from django.db.models.signals import m2m_changed
from django.dispatch import receiver 
from django.contrib.auth.models import User

class Subject(models.Model):
    name = models.CharField(max_length=50)
    students = models.ManyToManyField(User)
    teacher = models.ForeignKey(User, related_name="subject_teaching")
    pub_date = models.DateField(auto_now_add=True)
    start_date = models.DateField()
    end_date = models.DateField()
    ongoing = models.BooleanField(default=False)
    
    def __unicode__(self):
        return self.name

class Grade(models.Model):
    subject = models.ForeignKey(Subject)
    student = models.ForeignKey(User)
    grade = models.DecimalField(max_digits = 5,decimal_places=2, default=0)
    
    def __unicode__(self):
        return self.student.username + '-' + self.subject.name + '-' + str(self.grade)

#SIGNALS
@receiver(m2m_changed, sender = Subject.students.through)
def grade_add_handler(sender,instance, action, model, pk_set, **kwargs):
    ''' Initialize grade for students joined a subject'''
    if action == 'pre_add':
        for pk in pk_set:
            user = model.objects.get(id = pk)
            grade, created = Grade.objects.get_or_create(student = user, subject = instance)