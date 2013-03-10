from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Fieldset, ButtonHolder, Field, HTML, Div, Hidden
from crispy_forms.bootstrap import InlineRadios, FormActions

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, required =  True, label=("Username"))
    
    password = forms.CharField(widget = forms.PasswordInput, required = True)
    
    remember = forms.BooleanField(required = False, label=(u"Remember Me?"))
    
    next = forms.CharField(widget = forms.HiddenInput(), 
                           label = '', required = False)

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_method = "POST"
        self.helper.form_id = "id-login"
        self.helper.form_class = ""
        self.helper.form_action = "login_url"
        self.helper.layout = Layout (
                            Fieldset(
                                     "Login",
                                     HTML("""
                                         {% if messages %}
                                             {% for message in messages %}
                                                 <div class="alert alert-{{message.tags}}">
                                                     {{message}}
                                                 </div>
                                             {% endfor %}
                                         {% endif %}
                                     """),
                                     Field("username", css_class = "span10", placeholder = "Username"),
                                     Field("password", css_class = "span10", placeholder = "Password"),
                                     Field("remember"),
                                     Field("next")
                            ),
                            ButtonHolder(
                                    Submit('submit', "Log In")
                            ),
                        )
        
        super(LoginForm, self).__init__(*args, **kwargs)