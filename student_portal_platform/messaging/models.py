from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

class Message(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    sender = models.ForeignKey(User, related_name="message_sent")
    receiver = models.ForeignKey(User, related_name="message_received")
    unread = models.BooleanField(default=True)
    date = models.DateTimeField(auto_now_add=True)
    deleted = models.BooleanField(default=False)

    def __unicode__(self):
        return "title: %s , sender: %s , receiver : %s " % (self.title, self.sender, self.receiver)

    def get_absolute_url(self):
        return reverse("message:message", kwargs={'message_id': self.id})

    def trash_count(self):
        return self.objects.filter(deleted=True).count()

    def delete(self):
        self.deleted = True

    def read(self):
        self.unread = True
