from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from friends.models import FriendRequest, Friendship


@login_required
def friends(request):
    if request.method == "GET":
        return render(request, "final/friends.html", {'user': request.user})
    elif request.method == "POST":
        try:
            fr = FriendRequest.objects.get(id=request.POST['request-id'])
            if request.POST['submit'] == 'accept':
                fr.accept()
            elif request.POST['submit'] == 'decline':
                fr.decline()
        except FriendRequest.DoesNotExist:
            pass
    return redirect('friend:list')


@login_required
def addfriend(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if user.friendship in request.user.friendship.friends.all():
        messages.error(request, "This user is already your friend.")
        return redirect("profile_url", username=user.username)

    fr, created = FriendRequest.objects.get_or_create(from_user=request.user, to_user=user)
    if created:
        messages.success(request, "You successfully sent a friend request.")
        return redirect("profile_url", username=user.username)
    messages.error(request, "You already sent a friend request to this user.")
    return redirect("profile_url", username=user.username)


@login_required
def cancelrequest(request, user_id):
    user = get_object_or_404(User, id=user_id)
    try:
        fr = FriendRequest.objects.get(from_user=request.user, to_user=user)
        fr.cancel()
        messages.success(request, "Successfully canceled your friend request.")
    except FriendRequest.DoesNotExist:
        messages.error(request, "You don't have a friend request with this user.")
    return redirect("profile_url", username=user.username)


@login_required
def unfriend(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if user.friendship in request.user.friendship.friends.all():
        Friendship.objects.unfriend(request.user, user)
        messages.success(request, "You unfriended this user.")
    return redirect("profile_url", username=user.username)


@login_required
def acceptrequest(request, user_id):
    user = get_object_or_404(User, id=user_id)
    try:
        fr = FriendRequest.objects.get(from_user=user, to_user=request.user)
        fr.accept()
        messages.success(request, "You are now friends with this user.")
    except FriendRequest.DoesNotExist:
        messages.error(request, "You do not have a friend request from this user.")
    return redirect("profile_url", username=user.username)


@login_required
def declinerequest(request, user_id):
    user = get_object_or_404(User, id=user_id)
    try:
        fr = FriendRequest.objects.get(from_user=user, to_user=request.user)
        fr.decline()
        messages.success(request, "You denied the friend request of this user.")
    except FriendRequest.DoesNotExist:
        messages.error(request, "You do not have a friend request from this user.")
    return redirect("profile_url", username=user.username)
