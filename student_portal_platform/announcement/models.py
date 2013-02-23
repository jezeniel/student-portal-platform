from django.db import models
from django.contrib.auth.models import User

class Announcement(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(User)
    content = models.TextField()
    postdate = models.DateTimeField(auto_now_add = True)
    subjectcode = models.CharField(max_length = 50, default = 'global')
    
    def __unicode__(self):
        return self.subjectcode + '--' + self.title + '-' + str(self.postdate)
    