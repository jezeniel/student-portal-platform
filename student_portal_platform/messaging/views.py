from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q

from .models import Message
from .forms import PersonalMessageForm


@login_required
def send_message(request, user_id):
    user = get_object_or_404(User, id=user_id)
    form = PersonalMessageForm(request.POST)
    if form.is_valid():
        Message.objects.create(sender=request.user,
                               receiver=user,
                               title=form.cleaned_data['title'],
                               content=form.cleaned_data['content'])
    return redirect(user.get_absolute_url())


def inbox_view(request):
    inbox = Message.objects.filter(receiver=request.user, deleted=False)
    return render(request, "official/inbox.html", {'inbox': inbox, 'user': request.user})


def sent_view(request):
    sent = Message.objects.filter(sender=request.user, deleted=False)
    return render(request, "official/sentmail.html", {'sentmail': sent, 'user': request.user})


def message_view(request, message_id):
    try:
      message = Message.objects.get(Q(id=message_id), Q(receiver=request.user) | Q(sender=request.user))
    except Message.DoesNotExist:
      return redirect("message:inbox")
    return render(request, "official/message.html", {'message': message})
