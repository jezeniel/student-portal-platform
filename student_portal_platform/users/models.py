from django.db import models
from django.contrib.auth.models import User

class UserInfo(models.Model):
    user = models.OneToOneField(User, unique=True)
    gender = models.CharField(max_length=10)
    address = models.CharField(max_length=100)
    birthday = models.DateField(null=True)
    course = models.CharField(max_length=20, default='')
    crush = models.PositiveIntegerField(default=0);

