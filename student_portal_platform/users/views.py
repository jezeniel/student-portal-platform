from datetime import date, datetime

from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import HttpResponse

from .models import UserInfo
from .forms import RegisterForm

def register(request):
    if request.method.upper() == 'GET':
        if not request.user.is_authenticated():
            return render(request, 'users/register.html', { 'registerform' : RegisterForm()})
        return redirect("home_url")
    
    elif request.method.upper() == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            pass
        else:
            pass
        