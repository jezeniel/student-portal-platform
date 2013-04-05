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


@login_required
def inbox_view(request):
    conversations = request.user.conversations.all()
    return render(request, "final/inbox.html", {'conversations': conversations})


@login_required
def sent_view(request):
    sent = Message.objects.filter(sender=request.user, deleted=False)
    return render(request, "official/sentmail.html", {'sentmail': sent, 'user': request.user})


@login_required
def send_conversation(request, conversation_id):
    if request.method == "POST":
        conversation = get_object_or_404(Conversation, id=conversation_id)
        form = PersonalMessageForm(request.POST)
        if form.is_valid():
            for user in conversation.users.all():
                if request.user != user:
                    msg_receiver = user
            Message.objects.create(sender=request.user,
                                   receiver=msg_receiver,
                                   conversation=conversation,
                                   content=form.cleaned_data['content'])

    return redirect(conversation.get_absolute_url())


@login_required
def delete_view(request, conversation_id):
    try:
        conversation = request.user.conversations.get(id=conversation_id)
        conversation.users.remove(request.user)
    except Conversation.DoesNotExist:
        pass
    return redirect("message:inbox")


@login_required
def conversation_view(request, conversation_id):
    messageform = PersonalMessageForm()
    try:
        conversation = request.user.conversations.get(id=conversation_id)
        conversation.read_messages(request.user)
    except Conversation.DoesNotExist:
        return redirect("message:inbox")
    return render(request, "final/message.html", {'conversation': conversation, 'messageform': messageform})

