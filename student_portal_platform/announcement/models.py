from django.db import models
from django.contrib.auth.models import User

from subject.models import Subject

class Announcement(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(User)
    content = models.TextField()
    postdate = models.DateTimeField(auto_now_add = True)

    class Meta:
        abstract = True
        ordering = ['-postdate']

class SubjectAnnouncement(Announcement):
    subject = models.ForeignKey(Subject)

    def __unicode__(self):
        return "%s : %s - %s" % (self.subject, self.title, str(self.postdate))

class GlobalAnnouncement(Announcement):
    def __unicode__(self):
        return "%s - %s"  % (self.title, str(self.postdate))



