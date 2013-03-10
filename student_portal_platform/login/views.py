from django.http import HttpResponse
from django.views.generic import View
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from .forms import LoginForm
from announcement.models import GlobalAnnouncement

SESSION_TIME = 1209600 #two weeks
BROWSER_CLOSE = 0

def login_view(request):
    #if user is already logged in go to home page
    if request.user.is_authenticated():
        return redirect("home_url")
    
    #if method is GET render login page else authenticate user
    if request.method.upper() == "GET":
        loginform = LoginForm()
        
        #get the next link the have an initial value for it in the login formTWO_WEEKS
        if request.GET.has_key('next'):
            loginform.initial['next'] = request.GET.get("next")
            
        return render(request, 'official/home.html', 
                      {'loginform' : loginform})
        
    elif request.method.upper() == "POST":
        form = LoginForm(request.POST)
        #check if the fields are valid
        if form.is_valid():
            #authenticates user return None if doesn't exist
            user = authenticate(username = form.cleaned_data['username'], 
                                password = form.cleaned_data['password'])
            if user:
                # if the remember checkbox is checked the session will expire after
                # two weeks else it will end the session will expire when browser is closed
                if request.POST.has_key("remember"):
                    request.session.set_expiry(SESSION_TIME)
                else:
                    request.session.set_expiry(BROWSER_CLOSE)
                
                login(request, user)
                # if there is next it will redirect to the link
                # else just go to the homepage
                if request.POST.get("next"):
                    return redirect(request.POST['next'])
                else:
                    return redirect('home_url')
            
        messages.error(request, "Invalid Login!")
        return redirect('login_url')

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "Successfully logged out!")
    return redirect("login_url")

