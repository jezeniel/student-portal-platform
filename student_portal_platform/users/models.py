import os
from datetime import date

from django.utils import timezone
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

    def get_age(self):
        today = timezone.now().date()
        if self.birthday is None:
            return "n/a"
        try:
            birthday = self.birthday.replace(year=today.year)
        except ValueError:
            birthday = self.birthday.replace(year=today.year, day=today.day-1)
        return today.year - self.birthday.year - (birthday > today)

    def get_absolute_url(self):
        return reverse("profile_url", kwargs={'user_id': self.user.id})

    @classmethod
    def get_photo(self, photo, thumb_name, fallback_img):
        try:
            img_url = photo.url
            url, extension = os.path.splitext(img_url)
            return "%s%s%s" % (url, thumb_name, extension)
        except ValueError:
            return "/static/img/%s" % (fallback_img)

    def get_size64(self):
        return self.get_photo(self.primaryphoto, "thumb_64", "img64.png")

    def get_size32(self):
        return self.get_photo(self.primaryphoto, "thumb_32", "img32.png")

    def get_size128(self):
        return self.get_photo(self.primaryphoto, "thumb_128", "img128.png")
