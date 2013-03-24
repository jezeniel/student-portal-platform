import os

from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

class UserInfo(models.Model):
    user = models.OneToOneField(User, unique=True)
    primaryphoto = models.ImageField("Profile Photo", upload_to = "images/", blank = True, null = True)
    gender = models.CharField(max_length=10)
    address = models.CharField(max_length=255)
    birthday = models.DateField(null=True)
    course = models.CharField(max_length=255, default='')
    about_me = models.TextField(blank = True)
    crush = models.PositiveIntegerField(default=0);
    posts = models.PositiveIntegerField(default=0);

    def __unicode__(self):
        return "%s" % (self.user)

    def get_absolute_url(self):
        return reverse("profile_url", kwargs={'user_id': self.user.id})

    def get_size64(self):
        url, extension = os.path.splitext(self.primaryphoto.url)
        return url + "thumb_64" + extension

    def get_size32(self):
        url, extension = os.path.splitext(self.primaryphoto.url)
        return url + "thumb_32" + extension

    def get_size128(self):
        url, extension = os.path.splitext(self.primaryphoto.url)
        return url + "thumb_128" + extension
