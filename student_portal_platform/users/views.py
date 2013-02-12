from datetime import date, datetime

from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponse

from .models import UserInfo
from .forms import RegisterForm

def register(request):
    if request.method.upper() == 'GET':
        if not request.user.is_authenticated():
            return render(request, 'development/register.html', { 'registerform' : RegisterForm()})
        return redirect("home_url")
    
    elif request.method.upper() == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            userdata = {key:value for (key,value) in form.cleaned_data.items()} 
            user = User.objects.create_user(username=userdata['username'],
                                            password=userdata['password1'],
                                            email=userdata['email'],
                                            first_name=userdata['firstname'],
                                            last_name=userdata['lastname'])
            
            userinfo = UserInfo.objects.create(user=user,
                                               address=userdata['address'],
                                               course=userdata['course'],
                                               birthday=userdata['birthday'])
            
            messages.info(request, "Registered successfully.")
            return redirect("login_url")
        
        else:
            return render(request, 'development/register.html', {'registerform': form})
        