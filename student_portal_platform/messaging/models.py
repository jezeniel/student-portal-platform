from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse


class MessageManager(models.Manager):
    use_for_related_fields = True

    def count_unread(self):
        return self.filter(unread=True).count()

    def count_deleted(self):
        return self.filter(deleted=True).count()

    def get_unread(self):
        return self.filter(unread=True)

    def get_deleted(self):
        return self.filter(deleted=True)


class ConversationManager(models.Manager):
    use_for_related_fields = True

    def count_unread(self):
        self.message_set.filter(unread=True).count()


class Conversation(models.Model):
    last_update = models.DateTimeField(auto_now=True)
    users = models.ManyToManyField(User, related_name="conversations")
    objects = ConversationManager()

    class Meta:
        ordering = ['-last_update']

    def __unicode__(self):
            return "Users:%s" % (self.id)

    def get_latest_message(self):
        return self.message_set.latest('date')

    def read_messages(self, user):
        for message in self.message_set.filter(unread=True, receiver=user):
            message.read()

    def get_absolute_url(self):
        return reverse("message:conversation", kwargs={'conversation_id': self.id})


class Message(models.Model):
    conversation = models.ForeignKey(Conversation)
    content = models.TextField()
    sender = models.ForeignKey(User, related_name="message_sent")
    receiver = models.ForeignKey(User, related_name="message_received")
    date = models.DateTimeField(auto_now_add=True)
    deleted = models.BooleanField(default=False)
    unread = models.BooleanField(default=True)
    related_manager = MessageManager()
    objects = models.Manager()

    class Meta:
        ordering = ['-date']

    def __unicode__(self):
        return "Conversation: %s - Sender: %s" % (self.conversation.id, self.sender.username)

    def more_than_one_day(self):
        if timezone.now() > self.date + timezone.timedelta(days=1):
            return True
        else:
            return False

    def delete(self):
        self.deleted = True
        self.save()

    def read(self):
        self.unread = False
        self.save()
