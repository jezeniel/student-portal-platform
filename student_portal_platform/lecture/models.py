import os.path

from django.db import models
from django.contrib.auth.models import User


from subject.models import Subject

def upload_path(instance, filename):
    return '/'.join(['lecture', str(instance.subject.id), filename])

class Lecture(models.Model):
    subject = models.ForeignKey(Subject)
    chapter = models.CharField(max_length=100)
    author  = models.ForeignKey(User)
    content = models.TextField()
    date_created = models.DateTimeField(auto_now_add = True)

    def __unicode__(self):
        return "%s - %s : %s" % (self.subject, self.name, self.chapter)

class LectureFile(models.Model):
    subject = models.ForeignKey(Subject)
    docfile = models.FileField(upload_to=upload_path)
    date_uploaded = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_uploaded']

    def filename(self):
        return os.path.basename(self.docfile.name)
