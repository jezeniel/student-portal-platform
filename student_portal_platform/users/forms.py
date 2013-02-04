from re import match

from django import forms
from django.contrib.auth.models import User

from .widgets import DateSelectorWidget

class RegisterForm(forms.Form):
    firstname = forms.CharField(max_length = 100, 
                                label = (u"First name"))
    lastname = forms.CharField(max_length = 100,
                               label = (u"Last name"))
    course = forms.CharField(max_length = 50)
    email = forms.EmailField()
    address = forms.CharField()
    birthday = forms.DateField(widget = DateSelectorWidget)
    username = forms.CharField(max_length=30)
    password1 = forms.CharField(widget = forms.PasswordInput, 
                                label = (u"Password"),
                                min_length=8)
    password2 = forms.CharField(widget = forms.PasswordInput, 
                                label = (u"Retype password"),
                                min_length=8)
    
    def clean_username(self):
        username = self.cleaned_data['username']
        if not match(r'^[a-zA-Z0-9]+$', username):
            raise forms.ValidationError("Use alphanumeric characters.")
        try:
            user = User.objects.get(username = username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError("Username already exists.")
    
    def clean(self):
        cleaned_data = super(RegisterForm,self).clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if  password1 and password2:
            if password1 != password2:
                self._errors['password1'] = self.error_class(["Password did not match."])
                
                del cleaned_data['password1']
                del cleaned_data['password2']
                
        return cleaned_data
        