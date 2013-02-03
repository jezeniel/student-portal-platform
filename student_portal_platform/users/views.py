from datetime import date, datetime

from django.contrib.auth.models import User
from django import forms
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import widgets

from .models import UserInfo

class DateSelectorWidget(widgets.MultiWidget):
    def __init__(self, attrs=None, dt=None, mode=0):  
        months = [(month,month) for month in ["Jan", "Feb", "March"]]
        days = [(day,day) for day in range(1,32)]
        years = [(year, year) for year in range(1900,2013)]

        _widgets = (
            widgets.Select(attrs=attrs, choices=days), 
            widgets.Select(attrs=attrs, choices=months),
            widgets.Select(attrs=attrs, choices=years),
            )
        super(DateSelectorWidget, self).__init__(_widgets, attrs)

    def decompress(self, value):
        if value:
            return [value.day, value.month, value.year]
        return [None, None, None]

    def format_output(self, rendered_widgets):
        return u''.join(rendered_widgets)
    
                         
class RegisterForm(forms.Form):
    firstname = forms.CharField(max_length = 100, 
                                label = (u"First name"))
    lastname = forms.CharField(max_length = 100,
                               label = (u"Last name"))
    course = forms.CharField(max_length = 50)
    birthday = forms.DateField(widget=DateSelectorWidget())
    username = forms.CharField(max_length = 30)
    password1 = forms.CharField(widget = forms.PasswordInput, 
                                label = (u"Password"))
    password2 = forms.CharField(widget = forms.PasswordInput, 
                                label = (u"Retype password"))
    
    
    
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
        