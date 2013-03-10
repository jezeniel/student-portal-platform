from re import match

from django import forms
from django.contrib.auth.models import User

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Fieldset, ButtonHolder, Field, HTML, Div
from crispy_forms.bootstrap import InlineRadios, FormActions

from .widgets import DateSelectorWidget

class AccountForm(forms.Form):

    email = forms.EmailField(required = True, 
                             label = (u""),
                             help_text = "ex. johndoe@domain.com")

    username = forms.CharField(max_length=30, required = True, label = (u""))
    
    password1 = forms.CharField(widget = forms.PasswordInput, 
                    label = (u""),
                    min_length=8,
                    required = True,
                     help_text = "At least 8 characters.",
                )
    
    password2 = forms.CharField(widget = forms.PasswordInput, 
                    label = (u""),
                    min_length=8,
                    required = True,
                )
    
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.html5_required = True
        self.helper.form_tag = False
        self.helper.layout = Layout (
                        Fieldset(
                            "Account Information",
                            Field("username", placeholder = "Username", pattern = "[a-zA-Z0-9]+", css_class = "span11"),
                            Field("email", placeholder = "Email", type = "email", css_class = "span11"),
                            Field("password1", placeholder = "Password", pattern = "(.){8,}", css_class = "span11"),
                            Field("password2", placeholder = "Confirm Password", pattern = "(.){8,}", css_class = "span11"),
                        ),    
                    )
        
        super(AccountForm, self).__init__(*args, **kwargs)
  

    def clean_username(self):
        username = self.cleaned_data['username']
        if not match(r'^[a-zA-Z0-9]+$', username):
            raise forms.ValidationError("Use alphanumeric characters.")
        try:
            user = User.objects.get(username = username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError("User already exists.")
    
    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            user = User.objects.get(email = email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError("Email already used.")
    
    def clean(self):
        cleaned_data = super(AccountForm,self).clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if  password1 and password2:
            if password1 != password2:
                self._errors['password1'] = self.error_class(["Password did not match."])
                
                del cleaned_data['password1']
                del cleaned_data['password2']
                
        return cleaned_data
    

class PersonalForm(forms.Form):
    firstname = forms.CharField(
                    max_length = 100, 
                    label = (u""),
                    required = True,
                )
    
    lastname = forms.CharField(
                    max_length = 100,
                    label = (u""),
                    required = True,
                )
    
    gender = forms.ChoiceField(
                    widget= forms.RadioSelect,
                    choices = (('male', 'Male'), ('memale', 'Female')),
                    required = True,
                    label = (u""),
                )
    
    address = forms.CharField(max_length=255, required = True, label = (u""))
    
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.html5_required = True
        self.helper.layout = Layout (
                        Fieldset(
                            "Personal Information",
                            Field("firstname", placeholder = "First Name", pattern = "[\sa-zA-Z]+", css_class = "span11"),
                            Field("lastname", placeholder = "Last Name", pattern = "[\sa-zA-Z]+", css_class = "span11"),
                            Field("address", placeholder = "Address", css_class = "span11" ),
                            InlineRadios("gender", css_class = "inline"),       
                        ),
                        ButtonHolder(
                            Submit('submit', 'Sign Up!', css_class = 'btn btn-large span11')            
                        
                        )
                            
                    )
        super(PersonalForm, self).__init__(*args, **kwargs)
  
    