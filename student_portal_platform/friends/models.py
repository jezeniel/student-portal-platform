from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User


class FriendRequest(models.Model):
    from_user = models.ForeignKey(User, related_name = "friendrequest_from")
    to_user = models.ForeignKey(User, related_name = "friendrequest_to")

    def accept(self):
        Friendship.objects.befriend(self.from_user, self.to_user)
        self.delete()

    def decline(self):
        self.delete()

    def cancel(self):
        self.delete()

    def has_request(self,from_user, to_user):
        try:
            self.objects.get(from_user = from_user, to_user = to_user)
        except self.DoesNotExist:
            return False
        return True

    def __unicode__(self):
        return "Friend Request: From: %s To: %s" % (self.from_user.username,
                                                    self.to_user.username)

class FriendshipManager(models.Manager):
    def befriend(self, user1,user2):
        Friendship.objects.get(user=user1).friends.add(
                                                       Friendship.objects.get(user=user2))

    def unfriend(self, user1, user2):
        Friendship.objects.get(user=user1).friends.remove(
                                                          Friendship.objects.get(user=user2))

class Friendship(models.Model):
    user = models.OneToOneField(User)
    friends = models.ManyToManyField('self', symmetrical=True)
    objects = FriendshipManager()

    def count_friends(self):
        return self.friends.count()

    def __unicode__(self):
        return self.user.username


@receiver(post_save, sender = User)
def create_friendship_instance(sender, instance, created, raw, **kwargs):
    if created and not raw:
        Friendship.objects.create(user = instance)

