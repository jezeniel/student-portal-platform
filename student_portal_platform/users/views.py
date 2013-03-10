from datetime import date, datetime

from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponse

from .models import UserInfo
from .forms import AccountForm, PersonalForm
from login.forms import  LoginForm

def register(request):
    if request.method.upper() == 'GET':
        if not request.user.is_authenticated():
            return render(request, 'official/form.html', {'accountform' : AccountForm(),
                                                          'personalform': PersonalForm()})
        return redirect("home_url")
    
    elif request.method.upper() == 'POST':
        form = AccountForm(request.POST)
        form2 = PersonalForm(request.POST)
        if form.is_valid() and form2.is_valid():
            userdata = {key:value for (key,value) in form.cleaned_data.items()} 
            userdata2 = {key:value for (key,value) in form2.cleaned_data.items()}
            user = User.objects.create_user(username=userdata['username'],
                                            password=userdata['password1'],
                                            email=userdata['email'],
                                            first_name=userdata2['firstname'],
                                            last_name=userdata2['lastname'])
            
            userinfo = UserInfo.objects.create(user=user,
                                               address=userdata2['address'],
                                               )
            
            messages.info(request, "Registered successfully.")
            return redirect("login_url")
        
        else:
            return render(request, 'official/form.html', {'accountform': form, 'personalform': form2})
        