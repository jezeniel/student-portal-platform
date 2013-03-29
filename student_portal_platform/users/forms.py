from re import match

from django import forms
from django.contrib.auth.models import User

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Fieldset, ButtonHolder, Field, Button
from crispy_forms.bootstrap import InlineRadios, AppendedText


GENDER_CHOICE = (('male', 'Male'), ('female', 'Female'))


class AccountForm(forms.Form):
    email = forms.EmailField(required=True,
                             label=(u""),
                             help_text="ex. johndoe@domain.com")

    username = forms.CharField(max_length=30, required=True, label=(u""))

    password1 = forms.CharField(widget=forms.PasswordInput,
                                label=(u""),
                                min_length=8,
                                required=True,
                                help_text="At least 8 characters.")

    password2 = forms.CharField(widget=forms.PasswordInput,
                                label=(u""),
                                min_length=8,
                                required=True)

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.html5_required = True
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Fieldset(
                "Account Information",
                Field("username", placeholder="Username", pattern="[a-zA-Z0-9]+", css_class="span11"),
                Field("email", placeholder="Email", type="email", css_class="span11"),
                Field("password1", placeholder="Password", pattern="(.){8,}", css_class="span11"),
                Field("password2", placeholder="Confirm Password", pattern="(.){8,}", css_class="span11"),
            ),
        )

        super(AccountForm, self).__init__(*args, **kwargs)

    def clean_username(self):
        username = self.cleaned_data['username']
        if not match(r'^[a-zA-Z0-9]+$', username):
            raise forms.ValidationError("Use alphanumeric characters.")
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError("User already exists.")

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError("Email already used.")

    def clean(self):
        cleaned_data = super(AccountForm, self).clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if password1 and password2:
            if password1 != password2:
                self._errors['password1'] = self.error_class(["Password did not match."])

                del cleaned_data['password1']
                del cleaned_data['password2']

        return cleaned_data


class PersonalForm(forms.Form):
    firstname = forms.CharField(max_length=255,
                                label=(u""),
                                required=True)

    lastname = forms.CharField(max_length=255,
                               label=(u""),
                               required=True)

    gender = forms.ChoiceField(widget=forms.RadioSelect,
                               choices=GENDER_CHOICE,
                               required=True,
                               label=(u""))

    address = forms.CharField(max_length=255,
                              required=True,
                              label=(u""))

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.html5_required = True
        self.helper.layout = Layout(
            Fieldset(
                "Personal Information",
                Field("firstname", placeholder="First Name", pattern="[\sa-zA-Z]+", css_class="span11"),
                Field("lastname", placeholder="Last Name", pattern="[\sa-zA-Z]+", css_class="span11"),
                Field("address", placeholder="Address", css_class="span11"),
                InlineRadios("gender", css_class="inline"),
            ),
            ButtonHolder(
                Submit('submit', 'Sign Up!', css_class='btn btn-large span11', data_loading_text="Signing Up...")
            )
        )
        super(PersonalForm, self).__init__(*args, **kwargs)


class ProfileEdit(PersonalForm):
    primaryphoto = forms.ImageField(required=False, widget=forms.FileInput)
    birthday = forms.DateField(required=False)
    course = forms.CharField(max_length=255, required=False)
    about_me = forms.CharField(widget=forms.Textarea, required=False)

    def __init__(self, *args, **kwargs):
        super(ProfileEdit, self).__init__(*args, **kwargs)
        self.fields['firstname'].label = "First Name"
        self.fields['lastname'].label = "Last Name"
        self.fields['gender'].label = "Gender"
        self.fields['address'].label = "Address"
        self.fields['primaryphoto'].label = "Primary photo"

        self.helper.form_action = "editprofile"
        self.helper.form_class = "form-horizontal"
        self.helper.form_tag = True
        self.helper.layout = Layout(
            Fieldset(
                "Personal Information Settings",
                Field("primaryphoto"),
                Field("firstname", placeholder="First Name", pattern="[\sa-zA-Z]+"),
                Field("lastname", placeholder="Last Name", pattern="[\sa-zA-Z]+"),
                Field("address", placeholder="Address"),
                InlineRadios("gender", css_class="inline"),
                Field("course", placeholder="Course"),
                AppendedText("birthday",
                             "<i class='icon-calendar' data-time-icon='icon-calendar' data-date-icon='icon-calendar'></i>",
                             css_class="datepicker", template="official/crispy/appended_datepicker.html",
                             readonly=True),
                Field("about_me", placeholder="Tell us about yourself.")
            ),
            ButtonHolder(
                Submit('submit', 'Save', css_class='btn btn-large  span2 pull-right', )
            )
        )


class AccountEdit(AccountForm):
    password2 = forms.CharField(widget=forms.PasswordInput,
                                label=(u""),
                                min_length=8,
                                required=True)
    class Meta:
        exclude = ("username")

    def __init__(self, *args, **kwargs):
        super(AccountEdit, self).__init__(*args, **kwargs)
        self.helper.form_tag = True
        self.helper.form_class = "span5 offset1"
        self.helper.layout = Layout(
            Fieldset(
                "Account Information",
                Field("email", placeholder="Email", type="email", css_class="span5"),
                Field("password1", placeholder="Password", pattern="(.){8,}", css_class="span5"),
                Field("password2", placeholder="Confirm Password", pattern="(.){8,}", css_class="span5")
            ),
            ButtonHolder(
                Submit('submit', 'Save', css_class='btn btn-large  span2 pull-right')
            )
        )

