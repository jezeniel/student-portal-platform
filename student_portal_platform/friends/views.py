from django.contrib.auth.models import User
from friends.models import FriendRequest, Friendship
from django.views.generic import View
from django.shortcuts import render, redirect
from django.http import HttpResponse


class CreateFriendRequest(View):
    pass


def friends(request):
    if request.method == "GET":
        return render(request,"official/friends.html", {'user':request.user})
    elif request.method == "POST":
        fr = FriendRequest.objects.get(id= request.POST['request-id'])
        if request.POST['submit'] == 'accept':
            fr.accept()
        elif request.POST['submit'] == 'decline':
            fr.decline()
        return redirect('friend:list')

def addfriend(request, user_id):
    user = User.objects.get(id = user_id)
    fr, created = FriendRequest.objects.get_or_create(from_user = request.user, to_user = user)
    if created:
        return HttpResponse("ADDED")
    return HttpResponse("Already sent a friend request.")

def unfriend(request, user_id):
    user = User.objects.get(id = user_id)