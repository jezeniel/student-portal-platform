from django.db import models

from django.contrib.auth.models import User

class ProfileComment(models.Model):
    receiver = models.ForeignKey(User, related_name="profilecomments")
    author = models.ForeignKey(User, related_name="profilecomments_author")
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']
