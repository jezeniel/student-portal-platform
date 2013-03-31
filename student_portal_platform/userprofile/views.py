from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from users.models import User
from announcement.models import GlobalAnnouncement
from friends.models import FriendRequest
from messaging.forms import PersonalMessageForm


@login_required
def home_view(request):
    return render(request, "final/dashboard.html", {'user': request.user})


@login_required
def profile_view(request, username):
    owner = get_object_or_404(User, username=username)
    try:
        has_request = FriendRequest.objects.get(Q(from_user=request.user, to_user=owner) |
                                                Q(from_user=owner, to_user=request.user))
    except FriendRequest.DoesNotExist:
        has_request = None

    return render(request, "final/profile.html", {'user': request.user,
                                                  'owner': owner,
                                                  'has_request': has_request,
                                                  'messageform': PersonalMessageForm()})
