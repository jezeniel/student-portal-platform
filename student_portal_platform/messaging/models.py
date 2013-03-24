from django.db import models
from django.contrib.auth.models import User


class Message(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    sender = models.ForeignKey(User, related_name="message_sent")
    receiver = models.ForeignKey(User, related_name="message_received")
    unread = models.BooleanField(default=True)
    date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "title: %s , sender: %s , receiver : %s " % (self.title, self.sender, self.receiver)

    def delete(self):
        self.delete()

    def read(self):
        self.unread = True
