from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from users.models import User, UserInfo

@login_required
def home_view(request):
    return render(request, "official/dashboard.html", { 'user': request.user })

@login_required
def profile_view(request, user_id):
    owner = User.objects.get(id = user_id)
    return render(request, "official/profile.html", { 'user' : request.user,
                                                      'owner' : owner })
    