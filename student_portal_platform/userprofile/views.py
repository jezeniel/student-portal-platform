from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from users.models import User, UserInfo
from announcement.models import GlobalAnnouncement
from friends.models import FriendRequest

@login_required
def home_view(request):
    return render(request, "official/dashboard.html", { 'user': request.user })

@login_required
def profile_view(request, user_id):
    owner = User.objects.get(id = user_id)
    respond_to_request = None
    cancel_request = None
    try:
        cancel_request =  FriendRequest.objects.get(from_user = request.user, to_user = owner)
        respond_to_request = FriendRequest.objects.get(from_user = owner, to_user = request.user)
    except FriendRequest.DoesNotExist:
        pass
    return render(request, "official/profile.html", { 'user' : request.user,
                                                      'owner' : owner ,
                                                      'respond_to_request': respond_to_request,
                                                      'cancel_request': cancel_request})
    