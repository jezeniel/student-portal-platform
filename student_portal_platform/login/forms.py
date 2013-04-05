from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Fieldset, ButtonHolder, Field, HTML, Button


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, required=True, label=("Username"))
    password = forms.CharField(widget=forms.PasswordInput,
                               required=True)
    remember = forms.BooleanField(required=False, label=(u"Keep me logged in"))
    next = forms.CharField(widget=forms.HiddenInput(),
                           label='', required=False)

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_method = "POST"
        self.helper.form_id = "id-login"
        self.helper.form_tag = False
        self.helper.form_class = ""
        self.helper.layout = Layout(
            Fieldset(
                "Login",
                Field("username", placeholder="Username"),
                Field("password", placeholder="Password"),
                Field("remember"),
                Field("next")
            ),
            ButtonHolder(
                Submit('submit', "Login", css_class="btn-block"),
                HTML("<a href=\"{% url 'register_url' %}\" class='btn btn-block btn-success'>Sign-Up!</a>")
            ),
        )
        super(LoginForm, self).__init__(*args, **kwargs)
