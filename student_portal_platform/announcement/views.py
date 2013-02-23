from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

from .models import Announcement
from .forms import AnnouncementForm


@login_required(login_url="login_url")
def announcement_post(request):
    if request.method == "GET":
        return render(request, 'proto_design/announce-post.html',
                      { 'announcementForm' : AnnouncementForm()})
        
    elif request.method == "POST":
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            announcement = Announcement.objects.create(title = form.cleaned_data['title'],
                                                       content = form.cleaned_data['content'],
                                                       author = request.user)
            return HttpResponse("you posted")
        
def announcement_view(request, post_id):
    announcement = get_object_or_404(Announcement, id=post_id)
    return render(request, 'proto_design/announce-view.html', {'announcement': announcement})