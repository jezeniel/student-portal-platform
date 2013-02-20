from django import forms
from django.shortcuts import render, redirect
from django.http import HttpResponse

from announcement.models import Announcement

class announcementForm(forms.Form):
    title = forms.CharField(max_length=100)
    content = forms.CharField(widget= forms.Textarea);
    
    
def announcement_post(request):
    if request.method == "GET":
        return render(request, 'proto_design/announce.html', { 'announcementForm' : announcementForm()})
    elif request.method == "POST":
        form = announcementForm(request.POST)
        if form.is_valid():
            announcement = Announcement.objects.create(title = form.cleaned_data['title'],
                                                       content = form.cleaned_data['content'],
                                                       author = request.user)
            
            return HttpResponse("you posted")