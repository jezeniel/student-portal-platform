from django import forms
from .widgets import DateSelectorWidget

class RegisterForm(forms.Form):
    firstname = forms.CharField(max_length = 100, 
                                label = (u"First name"))
    lastname = forms.CharField(max_length = 100,
                               label = (u"Last name"))
    course = forms.CharField(max_length = 50)
    address = forms.CharField()
    birthday = forms.DateField(widget=DateSelectorWidget(), required=False)
    username = forms.CharField(max_length = 30)
    password1 = forms.CharField(widget = forms.PasswordInput, 
                                label = (u"Password"))
    password2 = forms.CharField(widget = forms.PasswordInput, 
                                label = (u"Retype password"))
    