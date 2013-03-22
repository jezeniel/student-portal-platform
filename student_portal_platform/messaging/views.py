from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .models import Message
from .forms import PersonalMessageForm

@login_required
def send_message(request, user_id):
    user = get_object_or_404(User, id = user_id)
    form = PersonalMessageForm(request.POST)
    if form.is_valid():
        message = Message.objects.create(sender = request.user,
                                         receiver = user,
                                         title = form.cleaned_data['title'],
                                         content = form.cleaned_data['content'])    
    return redirect("profile_url", user_id = user.id)
    
        
    
