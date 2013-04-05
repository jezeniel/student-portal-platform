from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User


class Subject(models.Model):
    name = models.CharField(max_length=100)
    students = models.ManyToManyField(User, related_name="subject_attending")
    teacher = models.ForeignKey(User, related_name="subject_teaching")
    pub_date = models.DateField(auto_now_add=True)
    start_date = models.DateField()
    end_date = models.DateField()
    ongoing = models.BooleanField(default=False)
    private = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("course:view", kwargs={'course_id': self.id})


class SubjectInvitation(models.Model):
    subject = models.ForeignKey(Subject, related_name="invitations")
    teacher = models.ForeignKey(User, related_name="invited_students")
    student = models.ForeignKey(User, related_name="course_invitations")

    def __unicode__(self):
        return "S:%s T:%s S:%s" % (self.subject.name, self.teacher.username, self.student.username)

    def accept(self):
        self.subject.students.add(self.student)
        self.delete()

    def decline(self):
        self.delete()
