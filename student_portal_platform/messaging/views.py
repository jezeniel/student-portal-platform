from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q

from .models import Message, Conversation
from .forms import PersonalMessageForm


@login_required
def send_message(request, user_id):
    user = get_object_or_404(User, id=user_id)
    form = PersonalMessageForm(request.POST)
    if form.is_valid():
        conversation = Conversation.objects.filter(users=request.user).filter(users=user)
        if conversation:
            conversation = conversation[0]
        else:
            conversation = Conversation.objects.create()
            conversation.users.add(request.user, user)
        Message.objects.create(sender=request.user,
                               receiver=user,
                               conversation=conversation,
                               content=form.cleaned_data['content'])

    return redirect(user.get_absolute_url())


def inbox_view(request):
    conversations = request.user.conversations.all()
    return render(request, "final/inbox.html", {'conversations': conversations})


def sent_view(request):
    sent = Message.objects.filter(sender=request.user, deleted=False)
    return render(request, "official/sentmail.html", {'sentmail': sent, 'user': request.user})


def conversation_view(request, conversation_id):
    try:
        conversation = request.user.conversations.get(id=conversation_id)
        conversation.read_messages(request.user)
    except Conversation.DoesNotExist:
        return redirect("message:inbox")
    return render(request, "final/message.html", {'conversation': conversation})

