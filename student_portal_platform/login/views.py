from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from .forms import LoginForm
from announcement.models import Announcement

def login_view(request):
    if request.user.is_authenticated():
        #if user is already logged in go to home page
        return redirect("home_url")
    #if method is GET render login page else authenticate user
    if request.method.upper() == "GET":
        x = Announcement.objects.order_by("-postdate")[0]
        return render(request, 'proto_design/index.html', 
                      {'loginform' : LoginForm(), 'announcement' : x})
    
    elif request.method.upper() == "POST":
        form = LoginForm(request.POST)
        #check if the fields are valid
        if form.is_valid():
            #authenticates user return not if doesn't exist
            user = authenticate(username = form.cleaned_data['username'], 
                                password = form.cleaned_data['password'])
            if user:
                if request.POST.has_key("remember"):
                    request.session.set_expiry(1209600)
                else:
                    request.session.set_expiry(0)
                login(request, user)
                return redirect('home_url')
        messages.error(request, "Invalid Login!")
        return redirect('login_url')

@login_required(login_url="login_url")
def logout_view(request):
    logout(request)
    messages.success(request, "Successfully logged out!")
    return redirect("login_url")

