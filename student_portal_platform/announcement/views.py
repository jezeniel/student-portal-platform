from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse

from .models import Announcement
from .forms import AnnouncementForm


@login_required(login_url="login_url")
def announcement_post(request):
    if request.method == "GET":
        return render(request, 'proto_design/post-announce.html',
                      { 'announcementForm' : AnnouncementForm()})
        
    elif request.method == "POST":
        form = announcementForm(request.POST)
        if form.is_valid():
            announcement = Announcement.objects.create(title = form.cleaned_data['title'],
                                                       content = form.cleaned_data['content'],
                                                       author = request.user)
            return HttpResponse("you posted")
        
        
def announcement_view(request, post_id):
    return HttpResponse("You are viewing " + post_id)