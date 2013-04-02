from urllib2 import urlopen
from xml.etree import ElementTree

from django.shortcuts import redirect, get_object_or_404
from django.http import HttpResponse, HttpRequest
from django.contrib import messages

from .models import Meeting
from subject.models import Subject


def create_room(request, course_id):
    subject = get_object_or_404(Subject, id=course_id)
    result = subject.meeting.create(HttpRequest.build_absolute_uri(request, subject.get_absolute_url()))
    if result is not None:
        messages.success(request, "Successfully created a conference.")
    else:
        messages.error(request, "Room already created or not available.")
    return redirect(subject.get_absolute_url())


def end_room(request, course_id):
    subject = get_object_or_404(Subject, id=course_id)
    result = subject.meeting.end()
    if result is not None:
        messages.success(request, "Successfully ended the current conference.")
    else:
        messages.error(request, "Failed to end conference. Maybe you did not start any conference?")
    return redirect(subject.get_absolute_url())


def join_room(request, course_id):
    subject = get_object_or_404(Subject, id=course_id)
    url, code = subject.meeting.join(request.user.get_full_name(), request.user.groups.all()[0].name)
    if code == "FAILED":
        messages.error(request, "There are no class currently ongoing.")
        return redirect(subject.get_absolute_url())
    else:
        return redirect(url)
