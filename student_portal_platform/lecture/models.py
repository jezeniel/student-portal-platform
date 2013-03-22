from django.db import models
from django.contrib.auth.models import User

from subject.models import Subject

class Lecture(models.Model):
    subject = models.ForeignKey(Subject)
    chapter = models.CharField(max_length=100)
    author  = models.ForeignKey(User)
    content = models.TextField()
    date_created = models.DateTimeField(auto_now_add = True)

    def __unicode__(self):
        return "%s - %s : %s" % (self.subject, self.name, self.chapter)