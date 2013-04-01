import string
from random import choice as randchoice
from urllib import urlencode
from hashlib import sha1
from urllib2 import urlopen
from xml.etree import ElementTree

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.conf import settings

from subject.models import Subject


def generate_pass(size=10, chars=string.ascii_uppercase + string.ascii_lowercase + string.digits):
    return ''.join(randchoice(chars) for x in range(size))


def parse(response):
    try:
        xml = ElementTree.XML(response)
        code = xml.find('returncode').text
        if code == 'SUCCESS':
            return xml
        else:
            raise
    except:
        return None

def failparse(response):
    try:
        xml = ElementTree.XML(response)
        code = xml.find('returncode').text
        if code == 'FAILED':
            return xml
        else:
            raise
    except:
        return None


class Meeting(models.Model):
    subject = models.OneToOneField(Subject)
    moderator_pass = models.CharField(blank=True, max_length=255)
    attendee_pass = models.CharField(blank=True, max_length=255)
    welcome_msg = models.CharField(blank=True, max_length=255)

    def __unicode__(self):
        return self.subject

    @classmethod
    def api_call(self, call, **kwargs):
        url = urlencode(kwargs['kwargs'])
        checksum = sha1(call + url + settings.BBB_SALT).hexdigest()
        return "%s?%s&checksum=%s" % (call, url, checksum)

    def create(self, logout_url):
        call = 'create'
        query = {'name': self.subject.name,
               'meetingID': self.subject.id,
               'attendeePW': self.attendee_pass,
               'moderatorPW': self.moderator_pass,
               'welcome': self.welcome_msg,
               'logoutURL': logout_url}
        url = settings.BBB_API + self.api_call(call, kwargs=query)
        result = parse(urlopen(url).read())
        return result

    def is_running(self):
        call = 'isMeetingRunning'
        query = {'meetingID': self.subject.id}
        url = settings.BBB_API + self.api_call(call, kwargs=query)
        print url
        result = parse(urlopen(url).read())
        isrunning = result.find('running').text
        print isrunning
        if isrunning is 'true':
            return True
        else:
            return False

    def end(self):
        call = 'end'
        query = {'meetingID': self.subject.id,
                 'password': self.moderator_pass}
        url = settings.BBB_API + self.api_call(call, kwargs=query)
        result = parse(urlopen(url).read())
        return result

    def join(self, name, user_type):
        call = 'join'
        if user_type == "teacher":
            password = self.moderator_pass
        else:
            password = self.attendee_pass
        query = {'fullName': name,
                 'meetingID': self.subject.id,
                 'password': password}
        url = settings.BBB_API + self.api_call(call, kwargs=query)
        result = failparse(urlopen(url).read())
        code = 'SUCCESS'
        if result is not None:
            code = result.find('returncode').text
        return (url, code)

    def save(self, *args, **kwargs):
        self.moderator_pass = generate_pass()
        self.attendee_pass = generate_pass()
        self.welcome_msg = "Welcome to %s!" % (self.subject.name)
        super(Meeting, self).save(*args, **kwargs)

@receiver(post_save, sender=Subject)
def create_meeting_instance(sender, instance, raw, **kwargs):
    Meeting.objects.get_or_create(subject=instance)
