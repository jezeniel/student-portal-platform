from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from users.models import User, UserInfo
from announcement.models import GlobalAnnouncement
from friends.models import FriendRequest
from messaging.forms import PersonalMessageForm
@login_required
def home_view(request):
    return render(request, "official/dashboard.html", { 'user': request.user })

@login_required
def profile_view(request, username):
    owner = User.objects.get(username = username)
    try:
        has_request = FriendRequest.objects.get(Q(from_user = request.user, to_user = owner) |
                                                Q(from_user = owner, to_user = request.user))
    except FriendRequest.DoesNotExist:
        has_request = None

    return render(request, "official/profile.html", { 'user' : request.user,
                                                      'owner' : owner ,
                                                      'has_request': has_request,
                                                      'messageform' : PersonalMessageForm()})

