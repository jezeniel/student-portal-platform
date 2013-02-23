from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget = forms.PasswordInput)
    remember = forms.BooleanField(required = False, label=(u"Remember Me?"))
    next = forms.CharField(widget = forms.HiddenInput(), 
                           label = '', required = False)
