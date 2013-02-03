from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django import forms
from django.contrib import messages


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField()

@login_required(login_url="login_url")
def home_view(request):
    return render(request, "home.html", { 'user': request.user })
    
def login_view(request):
    #if method is GET render login page else authenticate user
    if request.method.upper() == "GET":
        #if user is already logged in go to home page
        if request.user.is_authenticated():
            return redirect("home_url")
        return render(request, 'login/login.html', {'loginform' : LoginForm()})
    
    elif request.method.upper() == "POST":
        form = LoginForm(request.POST)
        #check if the fields are valid
        if form.is_valid():
            #authenticates user return not if doesn't exist
            user = authenticate(username = form.cleaned_data['username'], password = form.cleaned_data['password'])
            if user:
                login(request, user)
                return redirect('home_url')
        messages.error(request, "Invalid Login!")
        return redirect('login_url')

@login_required(login_url="login_url")
def logout_view(request):
    logout(request)
    messages.success(request, "Successfully logged out!")
    return redirect("login_url")
    #return render(request, 'login/login.html', {'error_message' : 'logged out'})

