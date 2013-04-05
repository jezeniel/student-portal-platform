from django.shortcuts import render, get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse

from users.models import User
from announcement.models import GlobalAnnouncement
from friends.models import FriendRequest
from messaging.forms import PersonalMessageForm
from .models import ProfileComment

@login_required
def home_view(request):
    announcements = GlobalAnnouncement.objects.all()
    return render(request, "final/dashboard.html", {'user': request.user, 'announcements': announcements})


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

@login_required
def search_user(request):
    if request.method == 'POST':
        keyword = request.POST.get('usersearch')
        results = User.objects.filter(Q(first_name__icontains = keyword) | Q(last_name__icontains=keyword))
        return render(request, "final/user-search.html", {'results': results})
    return redirect('home_url')


@login_required
def profile_comment(request, user_id):
    user = User.objects.get(id=user_id)
    if request.method == "POST":
        comment = request.POST.get('profile_comment')
        profile_comment = ProfileComment.objects.create(content=comment, author=request.user, receiver=user)
    return redirect(user.get_absolute_url())
